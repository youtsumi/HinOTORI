#!/usr/bin/env python
import sys, traceback, Ice, os, time, math
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
		#self.parseoptions(args)
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
		def CheckMove(ra0,ra1,dec0,dec1,Distance):
                        ra0, ra1, dec0, dec1 = float(ra0), float(ra1), float(dec0), float(dec1)
                        Dist = (ra1 - ra0)**2 + (dec1 - dec0)**2
                        if Dist > Distance**2:
                                print("Moving")
                                return 0
                        else:
                                print("Pointing")
                                return 1
		def Simulation(Distance,n=10):
                        while True:
                                ra0 = 1.0
                                dec0 = 1.0
                                time.sleep(1)
                                ra1 = 1.0 + n * Distance
                                dec1 = 1.0 + n * Distance
                                n = n - 1
                                Dist = math.sqrt((ra1 - ra0)**2 + (dec1 - dec0)**2)
                                print("%s %s %s %s %s %s"%(ra0,dec0,ra1,dec1,Distance,Dist))
                                if CheckMove(ra0,ra1,dec0,dec1,Distance) == 1:
                                        break
                        return
		def Wait(Distance):
                        while True:
                                ra0 = mount.GetRa()
                                dec0 = mount.GetDec()
                                time.sleep(1)
                                ra1 = mount.GetRa()
                                dec1 = mount.GetDec()
                                Dist = math.sqrt((ra1 - ra0)**2 + (dec1 - dec0)**2)
                                print("%s %s %s %s %s %s"%(ra0,dec0,ra1,dec1,Distance,Dist))
                                if CheckMove(ra0,ra1,dec0,dec1,Distance) == 1:
                                        break
                        return

		try:
                        Distance = 1.0 / 3600
                        Wait(Distance)
                        #Simulation(Distance,n=10)
			#print "Telescope will be moved to %lf %lf" % ( ra, dec )
			#mount.SetRa(ra)
			#mount.SetDec(dec)
			#mount.Goto()
                        #print "End"

		except:
			coord=SkyCoord(mount.GetRa(), mount.GetDec(),unit=u.degree)
			print("Current telescope position in instrument coordinate")
			print(coord.ra.degree, coord.dec.degree)
			print(coord.to_string("hmsdms"))
			return

	#def parseoptions(self,args):
	#	"""
	#	A class method to parse the argument
	#	"""

	#	parser = argparse.ArgumentParser(description='HinOTORI mount controller')
	#	parser.add_argument('ra', metavar='ra', type=float, nargs=1,
	#			    help='specify a coordinate to be visited')
	#	parser.add_argument('dec', metavar='dec', type=float, nargs=1,
	#			    help='specify a coordinate to be visited')
	#	#parser.add_argument('dec', metavar='dec', type=float, nargs=1,
	#	#		    help='specify a coordinate to be visited')

	#	try:
	#		options = parser.parse_args(args[1:])
	#		self.options = options
	#	except:
	#		options = None
	#		self.options = options

if __name__ == "__main__":
	app = MountClient()
	status = app.main(sys.argv)
	sys.exit(status)

