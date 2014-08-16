#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import time

class CameraServer(Ice.Application):
	def run(self,args):
		self.shutdownOnInterrupt()	# make sure clean up
		adapter = self.communicator().createObjectAdapterWithEndpoints(
                        os.path.basename(__file__), "default -p 10000")

		for i in range(3):
			camera = Camera(i)
			adapter.add(camera, self.communicator().stringToIdentity("ApogeeCam%d" % i))

		adapter.activate()
		self.communicator().waitForShutdown()
		return 0

class Camera(HinOTORI.Camera):
	def __init__(self,idnum):
		HinOTORI.Camera.__init__(self)
		self.idnum = idnum

	def Take(self,expt,filename,shutter,current=None):
		print "Take %lf" % expt
		time.sleep(expt)
		print "finish"
		return

	def Take_async(self,_cb,expt,filename,shutter,current=None):
		try:
			self.Take(expt,filename,shutter,current)
			_cb.ice_response()
		except:
			_cb.ice_exception(HinOTORI.Error("Error test"))

	def GetTemperature(self,current=None):
		print "GetTemperature[%d]: " % self.idnum
		return 0.

if __name__ == "__main__":
	app = CameraServer()
	args = sys.argv
	args.extend( [
		"--Ice.ThreadPool.Server.Size=3"
		])
	
	status = app.main(sys.argv)
	sys.exit(status)
