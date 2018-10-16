#!/usr/bin/env python
import serial
import time
import re
from multiprocessing import Manager, Process
import datetime
import config
import logging
logging.basicConfig(format=config.FORMAT, level=config.loglevel)
logger=logging.getLogger(__name__)

length=22
p=re.compile(r"FB_.*")
grammer={
        "FB_DOME_RIGHT":            ( 3,  5,   0x8),
        "FB_DOME_LEFT":             ( 3,  5,   0x4),
        "FB_DOME_STOP":             ( 3,  5,   0x2),
        "FB_SLIT_OPEN":             ( 3,  5,   0x1),
        "FB_SLIT_CLOSE":            ( 3,  6,   0x8),
        "FB_SLIT_STOP":             ( 3,  6,   0x4),
        "FB_DOME_AUTO":             ( 3,  6,   0x2),
        "FB_SLIT_AUTO_CLOSE":       ( 3,  6,   0x1),
        "SLIT_OPENED":              ( 3,  7,   0x8),
        "SLIT_CLOSED":              ( 3,  7,   0x4),
        "ALARM1":                   ( 3,  7,   0x2),
        "ALARM2":                   ( 3,  7,   0x1),
        "ALARM3":                   ( 3,  8,   0x8),
        "FB_DOME_EMG_STOP":         ( 3,  8,   0x4),
        "ORIGIN":                   ( 3,  8,   0x2),
        "FB_LATCH":                 ( 3,  8,   0x1),
        "LST.hh":                   ( 5,  5,  0xff),
        "LST.mm":                   ( 5,  7,  0xff),
        "LST.ss":                   ( 5,  9,  0xff),
        "LST.t":                    ( 5, 10,   0xf),
        "RA.hh":                    ( 6,  5,  0xff),
        "RA.mm":                    ( 6,  7,  0xff),
        "RA.ss":                    ( 6,  9,  0xff),
        "RA.t":                     ( 6, 11,   0xf),
        "DEC.sign":                 ( 6, 12,   0xf),
        "DEC.hh":                   ( 6, 13,  0xff),
        "DEC.mm":                   ( 6, 15,  0xff),
        "DEC.ss":                   ( 6, 17,  0xff),
        "JST.YY":                   ( 7,  5,  0xff),
        "JST.MM":                   ( 7,  7,  0xff),
        "JST.DD":                   ( 7,  9,  0xff),
        "JST.hh":                   ( 7, 11,  0xff),
        "JST.mm":                   ( 7, 13,  0xff),
        "JST.ss":                   ( 7, 15,  0xff),
        "TARGETDIR":                ( 8,  5, 0xfff),
        "CURRENTDIR":               ( 8,  8, 0xfff),
        "TELESCOPE":                ( 9,  5,  0xff),
        "LATCHTIMER":               (10,  5, 0xfff),
    }


def MakeNormalMessage( address ):
    return ":WR%02d"%address+"F"*14+"01#"


def PressButton( key ):
    normal = MakeNormalMessage(3)
    msg =  normal
    register, offset, mask=grammer[key]
    if register != 3:
        raise Exception("Invalid key was specified")
    msg=msg[:offset]+'%X' % ( int(msg[offset],16)^mask )+msg[offset+1:]
    return msg

def OneCommand(line):

    status = {}
    for k, v in grammer.iteritems():
        register, offset, mask = v
        if register!=int(line[3:5],16):
            continue
        if mask>=0xf:
            value=line[offset:offset+mask.bit_length()/4]
        else:
            value=0 if int(line[offset],16)&mask==0 else 1
#	print k, offset, mask, value
        status.update({k:value})

    return status


def SocketManager( port, status, sendbuf):
    ser=serial.Serial(port,38400,timeout=0,parity=serial.PARITY_ODD, stopbits=1)
    ser.flushInput()
    ser.flushOutput()

#    for older pyserial
#    ser.reset_input_buffer() 
#    ser.reset_output_buffer()
    
    time.sleep(1)
    msg=""
    while True:
	msg+=ser.read(100)
	idx1 = msg.find(":AS03")
	if idx1 == -1:
	    continue
	idx2 = msg.find(":AS03",idx1+1)
	if idx2 == -1:
	    continue
	line=msg[idx1:idx2]

	stx=0
	result = {}
	while len(line)>length:
	    line=line[stx:]
	    stx=line.index(":")
	    etx=line.index("#",stx)
	    status.update(OneCommand(line[stx:etx+1]))
	    stx=etx+1                

	logger.debug(status)

	# clear buffer if the queue is too long
	if len(msg)>1024:
	    msg = ""
	else:
	    msg = msg[idx2:]

	# send message
	if len(sendbuf)==0:
	    continue

	sendmsg=sendbuf.pop(0)
	logger.debug("Send this message: "+ sendmsg)
	ser.write(sendmsg)
        
class DomeToolKit:
    def __init__(self,port):
        manager = Manager()
        self.status=manager.dict()
        self.sendbuf=manager.list()
        self.p = Process(target=SocketManager, args=(port,self.status,self.sendbuf) )
	self.p.daemon=True
        self.p.start()

    def __com(self,msg):
	self.sendbuf.append(msg)
	self.sendbuf.append(MakeNormalMessage(3))

    def __ToggleButton(self,key,state):
        if state==True:
            if self.status[key]==1:
                return
            self.__com(PressButton(key))
        else:
            if self.status[key]==0:
                return
            self.__com(PressButton(key))

    def SetDateTime(self):
	logger.info("Set datetime")
	self.sendbuf.append(":WR07%s#" % datetime.datetime.now().strftime("%y%m%d%H%M%S"))

    def SetTelescopeNumber(self,telescopenumber):
	if telescopenumber < 0 or telescopenumber > 6:
	    raise Exception("Invalid value is given for telescopenumber")
	logger.info("Set telescope number as %d" % telescopenumber)
	self.sendbuf.append(":WR09%02d#" % int(telescopenumber) )

    def SetLatchTimer(self,latchtimer):
	if latchtimer < 0 or latchtimer > 999:
	    raise Exception("Invalid value is given for latchtimer")
	logger.info("Set latchtimer as %d" % latchtimer)
	self.sendbuf.append(":WR0a%03d#" % int(latchtimer) )

    def SlitAutoCloseOff(self,state):
	logger.info("SlitAutoCloseOff")
        self.__ToggleButton("FB_SLIT_AUTO_CLOSE",state)

    def SlitOpen(self,state=False):
    	"""Note that low (False) is active"""
        if self.status["SLIT_OPENED"]==0:
            return
	logger.info("SlitOpen")
        self.__ToggleButton("FB_SLIT_OPEN",state)

    def SlitClose(self,state=False):
    	"""Note that low (False) is active"""
        if self.status["SLIT_CLOSED"]==0:
            return
	logger.info("SlitClose")
        self.__ToggleButton("FB_SLIT_CLOSE",state)

    def DomeAuto(self,state):
	logger.info("DomeAuto")
        self.__ToggleButton("FB_DOME_AUTO",state)

    def DomeLatchEnable(self,state):
	logger.info("DomeLatchEnable")
        self.__ToggleButton("FB_LATCH",state)

if __name__ == "__main__":
#    Dome = DomeToolKitSimulator()
#    SocketReceiver({})
    Dome = DomeToolKit(config.domeport)
##    for i in range(1000):
##        time.sleep(0.5)
##        print "current: ", Dome.status
    Dome.SetDateTime()
    Dome.SetLatchTimer(60)
    Dome.SetTelescopeNumber(5)
    time.sleep(2)
#    print Dome.status["FB_SLIT_AUTO_CLOSE"]
#    Dome.SlitAutoCloseOff(False)
#    time.sleep(2)
#    print Dome.status["FB_SLIT_AUTO_CLOSE"]
#    time.sleep(5)
#    Dome.SlitAutoCloseOff(True)
#    time.sleep(2)
#    print Dome.status["FB_SLIT_AUTO_CLOSE"]
#    time.sleep(5)
#    Dome.SlitAutoCloseOff(False)
#    print Dome.status["FB_SLIT_AUTO_CLOSE"]
#    time.sleep(5)
#    time.sleep(5)
#    Dome.DomeAuto(True)
#    time.sleep(5)
#    Dome.DomeAuto(False)
#    time.sleep(5)
#    Dome.DomeAuto(True)
#    time.sleep(5)
#    print Dome.status["FB_LATCH"]
#    Dome.DomeLatchDisable(False)
#    time.sleep(5)
#    print Dome.status["FB_LATCH"]
#    Dome.DomeLatchDisable(True)
#    time.sleep(5)
#    print Dome.status["FB_LATCH"]
#    Dome.DomeLatchDisable(False)
#    time.sleep(5)
#    print Dome.status["FB_LATCH"]
#    
#        
    Dome.SlitOpen()
    time.sleep(5)
#    Dome.SlitClose()
