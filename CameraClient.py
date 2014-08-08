#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI

status = 0

camnum = 3

class CameraClient(Ice.Application):
	def run(self,args):
		cameras = []
		aptr = []	# array for an pointer to the asynchronous method invocation
		for i in range(camnum):
			obj = self.communicator().stringToProxy("ApogeeCam%d:default -p 10000" % i)
			cameras.append( HinOTORI.CameraPrx.checkedCast(obj) )
			cameras[i].GetTemperature()
			aptr.append(cameras[i].begin_Take(10.,"test",True))

		for i in range(camnum):
			print i
			if aptr[i] == None:
				continue
			print aptr[i]
			print "here"
			cameras[i].end_Take(aptr[i])


if __name__ == "__main__":
	app = CameraClient()
	status = app.main(sys.argv)
	sys.exit(status)

