#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("/home/utsumi/bin/HinOTORI.ice")
import HinOTORI
from optparse import OptionParser
sys.path.append("/home/utsumi/bin")
import config

status = 0

class TelescopeClient(Ice.Application):
	def run(self,args):
		self.args=args
		self.shutdownOnInterrupt()
		return self.TelescopeProcessor()

	def TelescopeProcessor(self):
		"""
		A class method to communicate with the telescope.
		"""
		try:
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
			elif self.args[1] == "cfocus":
				print telescope.GetFocusZ()
			elif self.args[1] == "afocus":
				telescope.SetFocusZ(float(self.args[2]))
				print telescope.GetFocusZ()
			elif self.args[1] == "rfocus":
				Pos = telescope.GetFocusZ()
				telescope.SetFocusZ(float(Pos)+float(self.args[2]))
				print telescope.GetFocusZ()

			else:
				print "no such command %s" % self.args[1]

			return 0
		except:
			raise


if __name__ == "__main__":
	app = TelescopeClient()
	status = app.main(sys.argv)
	sys.exit(status)

