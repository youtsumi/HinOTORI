#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
from optparse import OptionParser
import config


class CameraClient(Ice.Application):
	def run(self,args):
		self.shutdownOnInterrupt()
		self.parseoptions(args)
		if self.options.setp is not None:
			self.SetTemperature()
		else:
			self.GetTemperature()


	def SetTemperature(self):
		"""
		A class method to communicate with the cameras
		"""
		
		for i in range(len(config.camera)):
			obj = self.communicator().stringToProxy("ApogeeCam%d:default -h %s -p %d" \
				% ( config.camera[i]['uid'], \
					config.nodesetting['camera']['ip'], \
					config.nodesetting['camera']['port'] ))
			ptr = HinOTORI.CameraPrx.checkedCast(obj)
			setp =float(self.options.setp)
			print("self.options.setp %lf" % setp)
			ptr.SetTemperature(setp)

	def GetTemperature(self):
		"""
		A class method to communicate with the cameras
		"""
		for i in range(len(config.camera)):
			obj = self.communicator().stringToProxy("ApogeeCam%d:default -h %s -p %d" \
				% ( config.camera[i]['uid'], \
					config.nodesetting['camera']['ip'], \
					config.nodesetting['camera']['port'] ))
			ptr = HinOTORI.CameraPrx.checkedCast(obj)
			print("CCD temperature is %lf" % ptr.GetTemperature())


	def parseoptions(self,args):
		"""
		A class method to parse the argument
		"""
		parser = OptionParser()
		parser.add_option("-t", "--temp", dest="setp",
                  help="set target temperature", metavar="FILE",default=None)

		(options, myargs) = parser.parse_args(args)
		self.options = options

if __name__ == "__main__":
	status = 0
	app = CameraClient()
	status = app.main(sys.argv)
	sys.exit(status)

