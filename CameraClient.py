#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
from optparse import OptionParser
import datetime
import config
import ephem
import math
import pyfits
import pywcs
import numpy


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
		print self.options.focusz
		telescope.SetFocusZ(float(self.options.focusz))
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
		self.cmdra = mount.GetCmdRa()
		self.cmddec= mount.GetCmdDec()
		self.az = mount.GetAz()
		self.el = mount.GetEl()
		print mount.GetRa(), mount.GetDec()

	def _buildwcs(self):
		wcs = pywcs.WCS(naxis=2)
		wcs.wcs.crval = [self.ra, self.dec]
		wcs.wcs.crpix = [1024,1024]
#		wcs.wcs.cd = numpy.array([[-13.5e-6/4080e-3,0],[0,13.5e-6/4080e-3]])
		wcs.wcs.cd = numpy.array([[-0.67/3600,0],[0,0.67/3600]])
#		wcs.wcs.cdelt = numpy.array([-13.5e-6/4080e-3/math.pi*180.,13.5e-6/4080e-3/math.pi*180.])
#		wcs.rotateCD(self.az)
		wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]
		wcs.wcs.fix()
		return wcs.to_header()

	def CameraProcessor(self):
		"""
		A class method to communicate with the cameras
		"""
		if os.path.exists(self.options.path)!=True:
			os.system("mkdir -p %s" % self.options.path)

		expdatetime = datetime.datetime.utcnow()
		cameras = []
		aptr = []	# array for an pointer to the asynchronous method invocation

		try:
			exposuretime = [float(self.options.expt)]*3
		except ValueError:
			exposuretime = map(lambda x: float(x), self.options.expt.split(","))


		for i in range(len(config.camera)):
			filename = "object%s-%d.fits" \
				% ( expdatetime.strftime("%Y%m%d%H%M%S"), config.camera[i]['uid'] )

			header=pyfits.Header([
				("FOC-VAL", self.z, "Focus position in mm"),
				("RA-DEG", (self.ra), "Equatorial mount direction in degree"),
				("DEC-DEG", (self.dec), "Equatorial mount direction in degree"),
				("CRA-DEG", (self.cmdra), "Comannded Target position in degree"),
				("CDE-DEG", (self.cmddec), "Comannded Target position in degree"),

				("RA","%s" % ephem.hours(self.ra/180.*math.pi), "Target position in hour angle"),
				("DEC","%s" % ephem.degrees(self.dec/180.*math.pi), "Target position"),
				("AZ", self.az, "Target position in degree"),
				("EL", self.el, "Target position in degree"),
				("UFNAME", filename, "Original filename" ),
				("FILTER", config.camera[i]['filter'], "Filter name" ),
				("GAIN", config.camera[i]['gain'], "Gain measured by the vendor" ),
				("INSTRUME", "HinOTORI" , "Hiroshima University Operated Tibet Optical Robotic Imager" ),
				("OBSERVER", self.options.user , "Name of observers" ),
				("OBJECT", self.options.objectname , "Name of target object" ),
				("OBSERVAT", config.location["observatory"], "Observatory" ),
				("LONGITUD", config.location["longitude"], "Longitude of Observatory Location" ),
				("LATITUDE", config.location["latitude"] , "Latitude of Observatory Location" ),
				("MOUNTTYP", config.mount["mounttype"] , "Mount type" )
				])

			header.extend(self._buildwcs())

			obj = self.communicator().stringToProxy("ApogeeCam%d:default -h %s -p %d" \
				% ( config.camera[i]['uid'], \
					config.nodesetting['camera']['ip'], \
					config.nodesetting['camera']['port'] ))
			cameras.append( HinOTORI.CameraPrx.checkedCast(obj) )
			aptr.append(cameras[i].begin_Take(exposuretime[i],self.options.path+filename,self.options.shutter,header.tostring()))

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
                  help="set focus z", metavar="FILE",default="3.80")
		parser.add_option("-t", "--exp-t", dest="expt",
                  help="set expxposure time. a float number for all camera or three different number separated by comma without a white space should be given", metavar="FILE",default=1.0)
		parser.add_option("-o", "--object", dest="objectname",
                  help="set object", metavar="FILE",default="TEST")
		parser.add_option("-u", "--observer", dest="user",
                  help="set user", metavar="FILE",default="GOD")
		parser.add_option("-p", "--path", dest="path",
                  help="set target dir", metavar="FILE",default=config.targetdir)
		parser.add_option("-d", "--dark", dest="shutter", action="store_false",
                  default = True, help="set dark if it is specified" )

		(options, myargs) = parser.parse_args(args)
		if options.shutter is False:
		 	options.objectname = "DARK"
		self.options = options

class CameraClientWithoutTelescope(CameraClient):
	def __init__(self):
		self.z=0.0
		CameraClient.__init__(self)

	def TelescopeProcessor(self):
		print "set exposure time"

if __name__ == "__main__":
	status = 0
	app = CameraClient()
	#app = CameraClientWithoutTelescope()
	status = app.main(sys.argv)
	sys.exit(status)

