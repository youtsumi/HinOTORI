#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
from optparse import OptionParser
import config

status = 0

class CameraClient(Ice.Application):
	def run(self,args):
		self.args=args
		self.shutdownOnInterrupt()
		self.TelescopeProcessor()

	def TelescopeProcessor(self):
		"""
		A class method to communicate with the telescope.
		"""
		obj = self.communicator().stringToProxy("telescope:default -h 192.168.0.40 -p 10001")
		telescope=HinOTORI.TelescopePrx.checkedCast(obj)

		if self.args[1] == "open":
			print "open"
			telescope.OpenMirror()
		elif self.args[1] == "close":
			print "close"
			telescope.CloseMirror()
		else:
			print "no such command %s" % self.args[1]


if __name__ == "__main__":
	app = CameraClient()
	status = app.main(sys.argv)
	sys.exit(status)

