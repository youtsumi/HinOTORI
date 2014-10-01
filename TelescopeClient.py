#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
from optparse import OptionParser
import config

status = 0

class TelescopeClient(Ice.Application):
	def run(self,args):
		self.args=args
		self.shutdownOnInterrupt()
		self.TelescopeProcessor()

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

		if self.args[1] == "open":
			print "open"
			telescope.OpenMirror()
		elif self.args[1] == "close":
			print "close"
			telescope.CloseMirror()
		elif self.args[1] == "focus":
			telescope.SetFocusZ(int(self.args[2]))
			print telescope.GetFocusZ()

		else:
			print "no such command %s" % self.args[1]


if __name__ == "__main__":
	app = TelescopeClient()
	status = app.main(sys.argv)
	sys.exit(status)

