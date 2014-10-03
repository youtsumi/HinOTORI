"""
A pyhton script to control the GUI application named "TCS" developed by Alluna.
TCS supports the ASCOM interface to provide a kind of APIs to handle itself,
however, ASCOM does not have dustcover capability,
there is no way to control dust cover from CUI.
That is the reason to develop this script.

2014.5.8 Yousuke Utsumi
"""
from pywinauto import application, controls
import time
import config
import threading
import logging

pathtoapp = "C:\Program Files\ALLUNA Optics\Telescope Control System\TCS.exe"
windowname = u'TCS V11.0T'

logging.basicConfig(format=config.FORMAT, level=config.loglevel)
logger=logging.getLogger(__name__)

class AlarmException(Exception):
    def __init__(self,msg):
	Exception.__init__(self,msg)
    

def timerhandler():
    raise AlarmException("Maybe connection is lost")

class Telescope:
    def __init__(self):
        pass

    def __del__(self):
        self.app.kill_()

    def __checkconnection(self):
	if u"Connect" in self.buttonconnect.Texts():
            logger.info("Connecting to the telescope...")
            self.buttonconnect.Click()
        else:
	    pass
 
    def Connect(self):
        """Try to connect to the TCS software"""
        try:
            self.app = application.Application()
            self.app.connect_(path=pathtoapp)
            logger.info("TCS is already running... Try to fetch the handle.")
        except application.ProcessNotFoundError:
            logger.info("Try to run TCS application")
            self.app = application.Application.start(pathtoapp)
        
        self.app_form = self.app[windowname]
        self.buttonconnect = controls.win32_controls.ButtonWrapper(self.app_form[u"Connect"])
        
	self.__checkconnection()
    
            
        logger.info("Get tab content to handle tabs")
        self.tabcontrol=controls.common_controls.TabControlWrapper(self.app_form[u"TTabControl"])
        self.tabdict = dict( \
            [ (self.tabcontrol.GetTabText(i), i) for i in range(self.tabcontrol.TabCount())])

        logger.info("Get tab content in Settings to handle tabs")
        self._MoveTab("Settings") # need to move to get labels before do it
        self.settingstabcontrol=controls.common_controls.TabControlWrapper(self.app_form[u"TTabControl2"])
        self.settingstabdict = dict( \
            [ (self.settingstabcontrol.GetTabText(i), i) for i in range(self.settingstabcontrol.TabCount())])

        self._WaitCompletion()

    def _MoveTab(self,dst):
        """Internal method to handle the top-layere tabs"""
        if self.tabcontrol.GetSelectedTab() == self.tabdict[u"%s" % dst]:
            return
        logger.info("Then move to %s control tab" % dst)
        self.tabcontrol.Select(self.tabdict[u"%s" % dst])

    def _MoveSettingTab(self,dst):
        """Internal method to handle the tabs in the setting tab"""
        if self.settingstabcontrol.GetSelectedTab() \
	    == self.settingstabdict[u"%s" % dst]:
            return
        logger.info("Then move to %s control tab" % dst)
        self.settingstabcontrol.Select(self.settingstabdict[u"%s" % dst])

    def _DustcoverControl(self,cmd):
        """Internal method to control the mirror cover"""
        self._MoveTab("Dustcover")

        logger.info("Try to %s dust cover" % cmd)
        if cmd in self.DustcoverStatus():
            logger.info("Now %sing" % cmd)
            if self.app_form["Button2"].IsEnabled():
                self.app_form["Button2"].Click()
                while "Wait ..." in self.DustcoverStatus():
                    logger.info("Wait completion for 1 seconds.")
                    time.sleep(1)
            else:
                logger.error("Seems lost the handle to the telescope")
        else:
            logger.info("Seems already %sed" % cmd)

    def DustcoverStatus(self):
        """Try to retrieve the mirror cover"""
        self._MoveTab("Dustcover")
	self._WaitCompletion()
        return self.app_form["Button2"].Texts()
    
    def DustcoverOpen(self):
        """Try to open the mirror cover"""
        self._DustcoverControl("Open")

    def DustcoverClose(self):
        """Try to close the mirror cover"""
        self._DustcoverControl("Close")

    def _WaitCompletion(self):
        """Waits to completion of something to do"""
	try:
	    t=threading.Timer(60,timerhandler)
	    t.start()
	    while self.buttonconnect.IsEnabled() != True:
		logger.info("wait for 1 seconds")
		time.sleep(1)
		self.CheckAppStatus()
	    t.cancel()
	finally:
	    del t
        
    def FocusingTargetPosition(self,target):
        """Try to make the focuser to be at desired position in terms of the counter"""
        self._MoveTab("Focus")
        
        zpos=controls.win32_controls.EditWrapper(self.app_form["TJvSpinEdit17"])
 #       zpos.SetText("%d" % int(target/config.focusconv))
        zpos.SetText("%d" % target)

        gotobutton=controls.win32_controls.EditWrapper(self.app_form["GoToButton2"])
        gotobutton.Click()
        self._WaitCompletion()

    def FocusingHomePosition(self):
        """Try to make the focuser to be at the home position"""
        self._MoveTab("Focus")
        self.app_form["GoToStatic"]
        nominalbutton = controls.win32_controls.ButtonWrapper(self.app_form["GoToStatic"])
        nominalbutton.Click(coords=(26,0))
        self._WaitCompletion()

        # There was no key to describe "Homerun" button.
        # So I decited to use a "coords" extraoption to shift mouse click. 


    def FocusingPosition(self):
        """Returns the current focuser's position"""
        self._MoveTab("Settings")
        self._MoveSettingTab("Focuser")
#        return float(self.app_form["TJvSpinEdit4"].GetProperties()["Texts"][0])/1000.
        return float(self.app_form["TJvSpinEdit4"].GetProperties()["Texts"][0])*config.focusconv
        

    def InspectClass(self):
#        self._MoveTab("Focus")
        self._MoveTab("Climate")
        for i, child in enumerate(self.app_form.Children()):
	    if child.IsVisible() is not True:
		continue
            child.CaptureAsImage().save("%s%d.jpg" \
		% (child.FriendlyClassName(),i) )

    def CheckAppStatus(self):
	"""ControlNotEnalbed or ControlNotVisible"""
	try:
	    t=threading.Timer(config.apptimeout,timerhandler)
	    t.start()
	    while self.buttonconnect.IsVisible() != True:
		self.app_form.TypeKeys("\e")
		time.sleep(1)
	    t.cancel()
	    self.__checkconnection()

	except AlarmException as e:
	    self.app_form.TypeKeys("\e")
	    raise e

	except controls.HwndWrapper.ControlNotEnabled as e :
	    raise e

	except controls.HwndWrapper.ControlNotVisible as e :
	    raise e

	finally:
	    del t

if __name__ == "__main__":
    import time, sys, traceback
    try:
        telescope = Telescope()
        telescope.Connect()
        telescope.InspectClass()
#        print telescope.DustcoverStatus()
#        telescope.DustcoverOpen()
#        print telescope.DustcoverStatus()
#        telescope.DustcoverClose()
#        telescope.FocusingTargetPosition(9884)
#        print telescope.FocusingPosition()
        
    except:
        traceback.print_exc(file=sys.stdout)
        pass
#        del telescope

