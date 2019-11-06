#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import argparse
import config
import astropy.units as u
from astropy.coordinates import SkyCoord

status = 0

class MountClient(Ice.Application):
	def run(self,args):
		self.args=args
		self.shutdownOnInterrupt()
		self.parseoptions(args)
		self.MountProcessor()

	def MountProcessor(self):
		"""
		A class method to communicate with the telescope.
		"""
		obj = self.communicator().stringToProxy("Mount:default -h %s -p %d" 
                         % ( \
                                        config.nodesetting["mount"]['ip'], \
                                        config.nodesetting["mount"]['port'] \
                                ))
		mount=HinOTORI.MountPrx.checkedCast(obj)

		try:
			ra=self.options.coordinate[0]
			dec=self.options.coordinate[1]
			dra=self.options.offset[0]
			ddec=self.options.offset[1]
			if ra != None or dec != None:
				print("Telescope will be moved to %lf %lf" % ( ra, dec ))
				mount.SetRa(ra)
				mount.SetDec(dec)
				mount.Goto()
			if dra != 0 or ddec != 0:
				print("Offset %lf %lf" % ( dra, ddec ))
				mount.Move(dra,ddec)

		except:
			coord=SkyCoord(mount.GetRa(), mount.GetDec(),unit=u.degree)
			print("Current telescope position in instrument coordinate")
			print(coord.ra.degree, coord.dec.degree)
			print(coord.to_string("hmsdms"))
			return

	def parseoptions(self,args):
		"""
		A class method to parse the argument
		"""

		parser = argparse.ArgumentParser(description='HinOTORI mount controller')
		parser.add_argument('-c','--coordinate', dest='coordinate', type=float, nargs=2, 
				    default = [None, None],help='specify a coordinate to be visited')
		parser.add_argument("--offset", dest="offset", type=float, 
				    default = [0,0], nargs=2, help="dithering offset in arcsec")

		try:
			options = parser.parse_args(args[1:])
			self.options = options
		except:
			options = None
			self.options = options

if __name__ == "__main__":
	app = MountClient()
	status = app.main(sys.argv)
	#os.system("IsTelReadly.py")
	sys.exit(status)

