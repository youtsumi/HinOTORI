#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
from optparse import OptionParser
import datetime
import config
import ephem
import math

status = 0

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
		obj = self.communicator().stringToProxy("telescope:default -h %s -p %d" 
				% ( \
					config.nodesetting["telescope"]['ip'], \
					config.nodesetting["telescope"]['port'] \
				))
		telescope=HinOTORI.TelescopePrx.checkedCast(obj)
		if self.options.focusz!=None:
			telescope.SetFocusZ(float(self.options.focusz)*1000)
		self.z=telescope.GetFocusZ()
		print "Focus z = %lf [mm]" % self.z

	def MountProcessor(self):
		"""
		A class method to communicate with the mount.
		"""
		obj = self.communicator().stringToProxy("Mount:default -h %s -p %d"
				% ( \
					config.nodesetting["mount"]['ip'], \
					config.nodesetting["mount"]['port'] \
				))
		mount=HinOTORI.MountPrx.checkedCast(obj)
		self.ra = mount.GetRa()
		self.dec = mount.GetDec()
		self.az = mount.GetAz()
		self.el = mount.GetEl()
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

		for i in range(len(config.camera)):
			filename = "object%s-%d.fits" \
				% ( expdatetime.strftime("%Y%m%d%H%M%S"), config.camera[i]['uid'] )

			header=[
				("FOCUS","%lf" % self.z, "Focus position in mm"),
				("RA-DEG","%lf" % (self.ra/math.pi*180.), "Target position"),
				("DEC-DEG","%lf" % (self.dec/math.pi*180.), "Target position"),
				("RA","%s" % ephem.hours(self.ra), "Target position"),
				("DEC","%s" % ephem.degrees(self.dec), "Target position"),
				("AZ","%lf" % self.az, "Target position"),
				("EL","%lf" % self.el, "Target position"),
				("UFNAME", filename, "Original filename" ),
				("FILTER", config.camera[i]['filter'], "Filter name" ),
				("INSTRUME", "HinOTORI" , "Hiroshima University Operated Tibet Optical Robotic Imager" ),
				("OBSERVER", self.options.user , "Name of observers" ),
				("OBJECT", self.options.objectname , "Name of target object" ),
				("LONGITUD", "%lf" % config.location["longitude"], "Observatory Location" ),
				("LATITUDE", "%lf" % config.location["latitude"] , "Observatory Location" ),
				("MOUNTTYP", config.mount["mounttype"] , "Mount type" )
				]

			obj = self.communicator().stringToProxy("ApogeeCam%d:default -h %s -p %d" \
				% ( config.camera[i]['uid'], \
					config.nodesetting['camera']['ip'], \
					config.nodesetting['camera']['port'] ))
			cameras.append( HinOTORI.CameraPrx.checkedCast(obj) )
			aptr.append(cameras[i].begin_Take(exposuretime,filename,True,header))

		for i in range(len(config.camera)):
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
                  help="set expxposure time", metavar="FILE")
		parser.add_option("-o", "--object", dest="objectname",
                  help="set object", metavar="FILE")
		parser.add_option("-u", "--observer", dest="user",
                  help="set user", metavar="FILE",default="GOD")


		(options, myargs) = parser.parse_args(args)
		self.options = options


if __name__ == "__main__":
	app = CameraClient()
	status = app.main(sys.argv)
	sys.exit(status)

