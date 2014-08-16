#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
from optparse import OptionParser

status = 0
camnum = 3

class CameraClient(Ice.Application):
	def run(self,args):
		self.shutdownOnInterrupt()
		self.parseoptions(args)
		self.TelescopeProcessor()
		self.MountProcessor()
		self.CameraProcessor()

	def TelescopeProcessor(self):
		"""
		A class method to communicate with the telescope.
		"""
		obj = self.communicator().stringToProxy("telescope:default -h 192.168.0.40 -p 10001")
		telescope=HinOTORI.TelescopePrx.checkedCast(obj)
		if self.options.focusz!=None:
			telescope.SetFocusZ(float(self.options.focusz)*10000)
		self.z=telescope.GetFocusZ()
		print "Focus z = %lf [mm]" % self.z

	def MountProcessor(self):
		"""
		A class method to communicate with the mount.
		"""
		obj = self.communicator().stringToProxy("Mount:default -p 10002")
		mount=HinOTORI.MountPrx.checkedCast(obj)
		print mount.GetRa(), mount.GetDec()

	def CameraProcessor(self):
		"""
		A class method to communicate with the cameras
		"""

		cameras = []
		aptr = []	# array for an pointer to the asynchronous method invocation

		for i in range(camnum):
			obj = self.communicator().stringToProxy("ApogeeCam%d:default -p 10000" % i)
			cameras.append( HinOTORI.CameraPrx.checkedCast(obj) )
			cameras[i].GetTemperature()
			aptr.append(cameras[i].begin_Take(10.,"test",True))

		for i in range(camnum):
			if aptr[i] == None:
				continue
			cameras[i].end_Take(aptr[i])

	def parseoptions(self,args):
		"""
		A class method to parse the argument
		"""
		parser = OptionParser()
		parser.add_option("-z", "--focus-z", dest="focusz",
                  help="set focus z", metavar="FILE")

		(options, myargs) = parser.parse_args(args)
		self.options = options


if __name__ == "__main__":
	app = CameraClient()
	status = app.main(sys.argv)
	sys.exit(status)

