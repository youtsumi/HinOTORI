#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import MultiExposure
import time
import config
import git
import pyfits

camnum=len(config.camera)

class CameraServer(Ice.Application):
	def run(self,args):
		self.shutdownOnInterrupt()	# make sure clean up
		adapter = self.communicator().createObjectAdapterWithEndpoints(
                        os.path.basename(__file__), 
			"default -h %s -p %d" % ( config.nodesetting['camera']['ip'], \
						config.nodesetting['camera']['port']))

		try:
			cams=MultiExposure.GetCamConnections()
		except:
			cams=[None]*camnum
			print traceback.format_exc()

		for i in range(camnum):
			try:
				print int(cams[i].GetSerialNumber())
				cfg=filter(lambda x: x['serial']==int(cams[i].GetSerialNumber()), config.camera)[0]
			except AttributeError:
				print traceback.format_exc()
				cfg=config.camera[i]
			except:
				print traceback.format_exc()
				raise HinOTORI.Error("Camera may not have appropriate serial number or it is not included in configration file")
			camera = Camera(cfg['uid'],cams[i])
			adapter.add(camera, \
				self.communicator().stringToIdentity("ApogeeCam%d" % cfg['uid']))

		adapter.activate()
		self.communicator().waitForShutdown()
		return 0

class Camera(HinOTORI.Camera):
	def __init__(self,idnum,cam):
		self.idnum = idnum
		self.cam = cam
		repo = git.Repo(os.path.abspath(os.path.dirname(__file__))) 
		headcommit = repo.head.commit
		self.hexsha=headcommit.hexsha
		self.author=headcommit.author.name
		HinOTORI.Camera.__init__(self)

	def __del__(self):
		if self.cam is not None:
			self.cam.CloseConnection()

	def Take(self,expt,filename,shutter,fitsheader,current=None):
		fitsheader=pyfits.Header.fromstring(fitsheader)
		fitsheader.extend([ 
			("GITHASH",self.hexsha,"A Git hash key"),
			("GITAUTHO",self.author,"Last commiter name"),
		 ])
		print repr(fitsheader)
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
		print "GetTemperature[%d]: %lf" % (self.idnum, self.cam.GetTempCcd())
		return self.cam.GetTempCcd()

	def SetTemperature(self,setp,current=None):
		print "Trying to set temperature[%d] to %lf" % (self.idnum, setp)
		self.cam.SetCoolerSetPoint( setp )
		

if __name__ == "__main__":
	app = CameraServer()
	args = sys.argv
	args.extend( [
		"--Ice.ThreadPool.Server.Size=%d" % camnum
		])
	
	status = app.main(sys.argv)
	sys.exit(status)
