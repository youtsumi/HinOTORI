#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import AllunaToolKit
import time
import config
import logging

logging.basicConfig(format=config.FORMAT, level=config.loglevel)
logger=logging.getLogger(__name__)

class TelescopeServer(Ice.Application):
	def run(self,args):
		self.shutdownOnInterrupt()	# make sure clean up
		adapter = self.communicator().createObjectAdapterWithEndpoints(
                        os.path.basename(__file__), "default -h %s -p %d"
				 % ( \
                                        config.nodesetting["telescope"]['ip'], \
                                        config.nodesetting["telescope"]['port'] \
                                ))

		telescope = Telescope()
		adapter.add(telescope, self.communicator().stringToIdentity("telescope"))

		adapter.activate()
		self.communicator().waitForShutdown()
		return 0

class Telescope(HinOTORI.Telescope,AllunaToolKit.Telescope):
	def __init__(self):
		self.z=0.
		HinOTORI.Telescope.__init__(self)
		AllunaToolKit.Telescope.__init__(self)
		self.Connect()
		self.FocusingHomePosition()

	def __check(self):
		for i in range(config.ntrial):
		    try:
			    self.CheckAppStatus()
			    break # if success, go next
		    except:
			    if i == config.ntrial-1:
				raise
			    logger.error(traceback.format_exc())
			    logger.error("Try to reconnect")
			    self.app.kill_()
			    self.Connect()
			    self.FocusingPosition()

	def GetFocusZ(self,current=None):
		self.__check()
		self.z = self.FocusingPosition()
		logger.info("Telescope: z= %lf, %d" % (self.z, int(self.z/config.focusconv)))
		return self.z

	def SetFocusZ(self,targetz,current=None):
		self.__check()
		self.z=int(targetz/config.focusconv)
		for i in range(config.ntrial):
		    self.FocusingTargetPosition(self.z)
		    if self.z != int(self.GetFocusZ()/config.focusconv):
			if i==config.ntrial-1:
			    raise HinOTORI.Error("Focus seems not to be right position")
			else:
			    logger.error("Focus seems not to be right position, try again")
		    break

	def OpenMirror(self,current=None):
		self.__check()
		self.DustcoverOpen()

	def CloseMirror(self,current=None):
		self.__check()
		self.DustcoverClose()


if __name__ == "__main__":
	app = TelescopeServer()
	status = app.main(sys.argv)
	sys.exit(status)
