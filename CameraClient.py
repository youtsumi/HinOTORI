#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
from optparse import OptionParser
import datetime

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
		self.ra = mount.GetRa()
		self.dec = mount.GetDec()
		print mount.GetRa(), mount.GetDec()

	def CameraProcessor(self):
		"""
		A class method to communicate with the cameras
		"""

		expdatetime = datetime.datetime.utcnow()
		cameras = []
		aptr = []	# array for an pointer to the asynchronous method invocation
		if self.options.expt!=None:
			exposuretime = float(self.options.expt)
		else:
			exposuretime = 1.0

		for i in range(camnum):
			filename = "object%s-%d.fits" % ( expdatetime.strftime("%Y%m%d%H%M%S"), i )
			header=[
				("Focus","%lf" % self.z, "Focus position in mm"),
				("RA","%lf" % self.ra, "Target position"),
				("Dec","%lf" % self.dec, "Target position"),
				("UFNAME", filename, "Original filename" )
				]

			obj = self.communicator().stringToProxy("ApogeeCam%d:default -p 10000" % i)
			cameras.append( HinOTORI.CameraPrx.checkedCast(obj) )
			aptr.append(cameras[i].begin_Take(exposuretime,filename,True,header))

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
		parser.add_option("-t", "--exp-t", dest="expt",
                  help="set exp t", metavar="FILE")

		(options, myargs) = parser.parse_args(args)
		self.options = options


if __name__ == "__main__":
	app = CameraClient()
	status = app.main(sys.argv)
	sys.exit(status)

