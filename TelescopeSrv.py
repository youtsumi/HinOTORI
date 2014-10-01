#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import AllunaToolKit
import time
import config

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

	def GetFocusZ(self,current=None):
		self.z = self.FocusingPosition()
		print "Telescope: z= %lf, %d" % (self.z, int(self.z/config.focusconv))
#		return int(self.z/config.focusconv)
		return self.z

	def SetFocusZ(self,targetz,current=None):
		self.z=int(targetz/config.focusconv)
		self.FocusingTargetPosition(self.z)
		if self.z != int(self.GetFocusZ()/config.focusconv):
			print self.z,int(self.GetFocusZ()/config.focusconv)
			raise HinOTORI.Error("Focus seems not to be right position")

	def OpenMirror(self,current=None):
		self.DustcoverOpen()

	def CloseMirror(self,current=None):
		self.DustcoverClose()


if __name__ == "__main__":
	app = TelescopeServer()
	status = app.main(sys.argv)
	sys.exit(status)
