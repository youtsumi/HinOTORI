#coding: utf-8
"""
A python script to handle ERDE TRDC2 Software.
2015.9.1 Yousuke Utsumi
"""
from pywinauto import application, controls
import time
import config
import threading
import logging
import tesseract

pathtoapp = "C:\ERDE\TRDC2.exe"
windowname = u'ERDE.+'

logging.basicConfig(format=config.FORMAT, level=config.loglevel)
logger=logging.getLogger(__name__)

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
#        raise Exception("RS232C port is not avialable")
        
    def GetStatus(self):
	for item in  [ u"RAStatic2",
		 u"DECStatic2",
		 u"Button9", # rotate auto
		 u"Button11", # slit close
		 u"Button12", # latch auto
		 u"アラーム１", # alarm 1
		 u"アラーム２", # alarm 2
		 u"アラーム３", # alarm 3
		 u"Static10", # target angle
		 u"Static13" ] : # current angle
	    print item, self.CheckState(item)

    def MakeAllRemote(self):
	logger.error("Make all remote")
	for item in [
		 u"Button9", # rotate auto
		 u"Button11", # slit close
		 u"Button12", # latch auto
		    ]:
	    button=self.app_form[item]
	    if button.CaptureAsImage().getcolors() == (255,0,0):
		button.Click()

    def SlitOpen(self):
	logger.info("Try to open the dome slit")
	button=self.app_form[u"Button4"] # left button for what? maybe slit close
	button.Click()

    def SlitClose(self):
	logger.info("Try to close the dome slit close")
	button=self.app_form[u"Button2"] # left button for what? maybe slit close
	button.Click()

    def CheckState(self,item):
	button=self.app_form[item]
	for i, v in button.CaptureAsImage().getcolors():
	    if v == ( 255, 0, 0 ) :
		return False
	    elif v == ( 0, 255, 0 ):
		return True
	    else:
		pass
	return None

    def InspectItem(self,item):
	"""This method is prepared for developing purpose"""
#    self.app_form.PrintControlIdentifiers()
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


    def readcontent(self):
	import tesseract
	api = tesseract.TessBaseAPI()
    #    api.SetOutputName("outputName");
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetPageSegMode(tesseract.PSM_AUTO)
	mImgFile = "eurotext.jpg"
	pixImage=tesseract.pixRead(mImgFile)
	api.SetImage(pixImage)
	outText=api.GetUTF8Text()
	print("OCR output:\n%s"%outText);
	api.End()

if __name__ == "__main__":
    import time, sys, traceback
    try:
	dome = Dome()
	dome.Connect()
	dome.GetStatus()
	dome.MakeAllRemote()
	dome.SlitOpen()
	time.sleep(10)
	dome.SlitClose()
	time.sleep(10)
	exit(0)
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
	dome.InspectItem(u"Static10")
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

