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
			ra=self.options.ra[0]
			dec=self.options.dec[0]
			print "Telescope will be moved to %lf %lf" % ( ra, dec )
			mount.SetRa(ra)
			mount.SetDec(dec)
#			mount.Goto(dec)

		except:
			coord=SkyCoord(mount.GetRa(), mount.GetDec(),unit=u.degree)
			print "Current telescope position in instrument coordinate"
			print coord.ra.degree, coord.dec.degree
			print coord.to_string("hmsdms")
			return

	def parseoptions(self,args):
		"""
		A class method to parse the argument
		"""

		parser = argparse.ArgumentParser(description='HinOTORI mount controller')
		parser.add_argument('ra', metavar='ra', type=float, nargs=1,
				    help='specify a coordinate to be visited')
		parser.add_argument('dec', metavar='dec', type=float, nargs=1,
				    help='specify a coordinate to be visited')

		try:
			options = parser.parse_args(args[1:])
			self.options = options
		except:
			options = None
			self.options = options

if __name__ == "__main__":
	app = MountClient()
	status = app.main(sys.argv)
	sys.exit(status)

