#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import MultiExposure
import time

camnum=3
class CameraServer(Ice.Application):
	def run(self,args):
		self.shutdownOnInterrupt()	# make sure clean up
		adapter = self.communicator().createObjectAdapterWithEndpoints(
                        os.path.basename(__file__), "default -p 10000")

		try:
			cams=MultiExposure.GetCamConnections()
		except:
			cams=[None]*camnum
			print traceback.format_exc()

		for i in range(camnum):
			camera = Camera(i,cams[i])
			adapter.add(camera, self.communicator().stringToIdentity("ApogeeCam%d" % i))

		adapter.activate()
		self.communicator().waitForShutdown()
		return 0

class Camera(HinOTORI.Camera):
	def __init__(self,idnum,cam):
		HinOTORI.Camera.__init__(self)
		self.idnum = idnum
		self.cam = cam

	def __del__(self):
		if self.cam is not None:
			self.cam.closeConnection()

	def Take(self,expt,filename,shutter,fitsheader,current=None):
		for fitsitem in fitsheader:
			print fitsitem
		print "Take %lf" % expt
		if self.cam is not None:
			MultiExposure.camprocess(self.cam,filename,expt,fitsheader)
		else:
			time.sleep(expt)
		print "finish"
		return

	def Take_async(self,_cb,expt,filename,shutter,fitsheader,current=None):
		try:
			self.Take(expt,filename,shutter,fitsheader,current)
			_cb.ice_response()
		except:
			_cb.ice_exception(HinOTORI.Error(traceback.format_exc()))

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
