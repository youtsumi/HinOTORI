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
		self.SetLatchTimer(10)
		self.SetTelescopeNumber(1)
		self.DomeLatchDisable(False)
		self.DomeManual(False)
		self.SlitAutoCloseOff(False)

	def __del__(self):
		self.DomeLatchDisable(True)
		self.DomeManual(True)
		self.SlitAutoCloseOff(False)

	def SlitOpen(self,current=None):
		self.SlitOpen()

	def SlitClose(self,current=None):
		self.SlitClose()

	def CurrentDirection(self,current=None):
		return self.status["CURRENTDIR"]

	def TargetDirection(self,current=None):
		return self.status["TARGETDIR"]

	def Alarm1(self,current=None):
		return True if self.status["ALARM3"] == 1 else False

	def Alarm2(self,current=None):
		return True if self.status["ALARM3"] == 1 else False

	def Alarm3(self,current=None):
		return True if self.status["ALARM3"] == 1 else False

	def isSlitOpened(self,current=None):
		return True if self.status["SLIT_OPENED"] == 1 else False

	def isSlitClosed(self,current=None):
		return True if self.status["SLIT_CLOSED"] == 1 else False

	def isDomeOrigin(self,current=None):
		return True if self.status["ORIGIN"] == 1 else False

if __name__ == "__main__":
	app = DomeServer()
	status = app.main(sys.argv)
	sys.exit(status)
