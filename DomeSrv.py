#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import DomeToolKit
import time
import config
import logging

logging.basicConfig(format=config.FORMAT, level=config.loglevel)
logger=logging.getLogger(__name__)

class DomeServer(Ice.Application):
	def run(self,args):
		self.shutdownOnInterrupt()	# make sure clean up
		adapter = self.communicator().createObjectAdapterWithEndpoints(
                        os.path.basename(__file__), "default -h %s -p %d"
				 % ( \
                                        config.nodesetting["dome"]['ip'], \
                                        config.nodesetting["dome"]['port'] \
                                ))

		dome = Dome()
		adapter.add(dome , self.communicator().stringToIdentity("dome"))

		adapter.activate()
		self.communicator().waitForShutdown()
		return 0

class Dome(HinOTORI.Dome,DomeToolKit.DomeToolKit):
	def __init__(self):
		HinOTORI.Dome.__init__(self)
		DomeToolKit.DomeToolKit.__init__(self,config.domeport)
		self.SetDateTime()
		self.SetLatchTimer(23)
		self.SetTelescopeNumber(1)
		time.sleep(5)
		self.DomeLatchEnable(True)
		self.DomeAuto(True)
		self.SlitAutoCloseOff(False)

	def __del__(self):
		self.DomeLatchEnable(False)
		self.DomeAuto(False)
		self.SlitAutoCloseOff(True)

	def slitOpen(self,current=None):
		self.SlitOpen()

	def slitClose(self,current=None):
		self.SlitClose()

	def CurrentDirection(self,current=None):
		return int(self.status["CURRENTDIR"])

	def TargetDirection(self,current=None):
		return int(self.status["TARGETDIR"])

	def Alarm1(self,current=None):
		return True if int(self.status["ALARM1"]) == 1 else False

	def Alarm2(self,current=None):
		return True if int(self.status["ALARM2"]) == 1 else False

	def Alarm3(self,current=None):
		return True if int(self.status["ALARM3"]) == 1 else False

	def isSlitOpened(self,current=None):
		return True if int(self.status["SLIT_OPENED"]) == 1 else False

	def isSlitClosed(self,current=None):
		return True if int(self.status["SLIT_CLOSED"]) == 1 else False

	def isDomeOrigin(self,current=None):
		return True if int(self.status["ORIGIN"]) == 1 else False

if __name__ == "__main__":
	app = DomeServer()
	status = app.main(sys.argv)
	sys.exit(status)
