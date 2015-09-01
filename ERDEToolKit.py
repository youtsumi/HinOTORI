#coding: utf-8
"""
"""
from pywinauto import application, controls
import time
import config
import threading
import logging

pathtoapp = "C:\ERDE\TRDC2.exe"
windowname = u'ERDE.+'

logging.basicConfig(format=config.FORMAT, level=config.loglevel)
logger=logging.getLogger(__name__)


class AlarmException(Exception):
    def __init__(self,msg):
	Exception.__init__(self,msg)
    
def timerhandler():
    raise AlarmException("Maybe connection is lost")

class Dome:
    def __init__(self):
        pass

    def __del__(self):
        self.app.kill_()
 
    def Connect(self):
        """Try to connect to the TRDC software"""
        try:
            self.app = application.Application()
            self.app.connect_(path=pathtoapp)
            logger.info("TRDC is already running... Try to fetch the handle.")
        except application.ProcessNotFoundError:
            logger.info("Try to run TRDC application")
            self.app = application.Application.start(pathtoapp)
        
        self.app_form = self.app.window_(title_re=windowname)
        if self.app.window_(title_re="RS232.+"):
            logger.error("RS232C port is not avialable")
	    self.app.window_(title_re="RS232.+")["OK"].Click()
#	    raise Exception("RS232C port is not avialable")
        
    def GetStatus(self):
        self.InspectItem(u"RAStatic2")
        self.InspectItem(u"DECStatic2")
        self.InspectItem(u"Button9") # rotate auto
        self.InspectItem(u"Button11") # slit close
        self.InspectItem(u"Button12") # latch auto
        self.InspectItem(u"アラーム１") # alarm 1
        self.InspectItem(u"アラーム２") # alarm 2
        self.InspectItem(u"アラーム３") # alarm 3
        self.InspectItem(u"Static10") # target angle
        self.InspectItem(u"Static13") # current angle

    def SlitOpen(self):
	logger.info("Try to open the dome slit")
	button=self.app_form[u"Button4"] # left button for what? maybe slit close
	button.Click()

    def SlitClose(self):
	logger.info("Try to close the dome slit close")
	button=self.app_form[u"Button2"] # left button for what? maybe slit close
	button.Click()

    def InspectClass(self):
        for i, child in enumerate(self.app_form.Children()):
	    if child.IsVisible() is not True:
		continue
            child.CaptureAsImage().save("%s-%d.jpg" \
		% (child.FriendlyClassName(),i) )

    def InspectItem(self,item):
#	self.app_form.PrintControlIdentifiers()
	button=self.app_form[item]
	print item, 
	for i, v in button.CaptureAsImage().getcolors():
	    if v == ( 255, 0, 0 ) :
		print "RED",
	    elif v == ( 0, 255, 0 ):
		print "GREEN",
	    else:
		pass
	print

	button.CaptureAsImage().save("%s.jpg" % item)



if __name__ == "__main__":
    import time, sys, traceback
    try:
        dome = Dome()
        dome.Connect()
	dome.GetStatus()
	dome.SlitOpen()
	time.sleep(10)
	dome.SlitClose()
	time.sleep(10)
	exit(0)
        dome.InspectClass()
        dome.InspectItem(u"Button1") # submit time
        dome.InspectItem(u"Button2") # left button for what? maybe slit close
        dome.InspectItem(u"Button3") # stop button maybe slit close
        dome.InspectItem(u"Button4") # right button for what? maybe slit close
        dome.InspectItem(u"Button5") # submit button same as 10
        dome.InspectItem(u"Button6") # left button for the rotation
        dome.InspectItem(u"Button7") # stop button for the rotation
        dome.InspectItem(u"Button8") # right button for the rotation
        dome.InspectItem(u"Button10") # submit 
        dome.InspectItem(u"Static5")
        dome.InspectItem(u"Static6") # telescope ra
        dome.InspectItem(u"Static7")
        dome.InspectItem(u"Static8") # telescope dec
        dome.InspectItem(u"Static9")
        dome.InspectItem(u"Static11")
        dome.InspectItem(u"Static12")
        dome.InspectItem(u"Static14")
        dome.InspectItem(u"Static15")
        dome.InspectItem(u"Static16")
        dome.InspectItem(u"Static17")
        dome.InspectItem(u"Static18")
        dome.InspectItem(u"Static19")
        dome.InspectItem(u"Static20")
        dome.InspectItem(u"Static21")
        dome.InspectItem(u"Static22")
        dome.InspectItem(u"Static23")
        dome.InspectItem(u"Static24")
        dome.InspectItem(u"Static25")
        dome.InspectItem(u"Static26")
        dome.InspectItem(u"Static27") # dome origin
        dome.InspectItem(u"Static28")
        dome.InspectItem(u"ドーム基準")
	dome.app_form.PrintControlIdentifiers()


    except:
        traceback.print_exc(file=sys.stdout)
        pass
#        del dome

