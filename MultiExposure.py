import numpy
import pylibapogee.pylibapogee as apg
import pylibapogee.pylibapogee_setup as SetupDevice
import pyfits
import re
import logging
import sys
import traceback
import datetime
import time
from multiprocessing import Pool

def GetCamConnection( ):
	print "Trying to find and connect with camera"
	#look for usb cameras first
	devices = SetupDevice.GetUsbDevices()


	# no usb cameras, then look for ethernet cameras
	if( len(devices) == 0 ):
	    devices = SetupDevice.GetEthernetDevices()
	    
	# exception....no cameras anywhere....
	if( len(devices) == 0 ):
	    raise RuntimeError( "No devices found on usb or ethernet" )
	    
	# connect to the first camera
	cams=map( lambda i: SetupDevice.CreateAndConnectCam( devices[i] ), range(len(devices)))

	return cams


def GetCameraInfo( obj ):
	excludelist = [
		"GetImage", # readout
		"GetInfo", # contains duplicated infomation
		"GetStatus", # contains duplicated infomation
		"GetStatusStr", # contains duplicated infomation
		"GetUsbFirmwareVersion", # 
		]
	wildcard=r"(^Get)|(^Is)"
	p=re.compile(wildcard)
	getmethod = filter(lambda x: True if p.match(x) is not None else False, dir(obj))
	getmethod = filter(lambda x: False if x in excludelist else True, getmethod)
	ccdinfo = []
	for method in getmethod:
		try:
			ret = getattr(obj,method)()
			logging.debug("%s: %s" % ( method, ret ) )
			ccdinfo.append((re.sub(wildcard, "", method),ret))
		except TypeError as e:
			logging.warn(traceback.format_exc())
		except RuntimeError as e:
			logging.warn(traceback.format_exc())
		except ValueError as e:
			logging.warn(traceback.format_exc())
		except:
			raise

	return ccdinfo


def camprocess( camid ):
#	print caminfo
#	(cam, camid) = caminfo
	cam = cams[camid]
	#print some basic info
	print cam, camid
	row = cam.GetMaxImgRows()
	col = cam.GetMaxImgCols()
	print "Imaging rows = %d, columns = %d" % ( row, col )


	cam.SetCooler( True )


	count = 1
	cam.SetImageCount( count )

	exposeTime = float(sys.argv[1])
	print "Starting %f sec light exposure" % (exposeTime) 
	expdatetime = datetime.datetime.utcnow()
	cam.StartExposure( exposeTime, True )
			
	status = None
	while status != apg.Status_ImageReady:
	    status = cam.GetImagingStatus()	
	    if( apg.Status_ConnectionError == status or
		apg.Status_DataError == status or
		apg.Status_PatternError == status ):
		msg = "Run %s: FAILED - error in camera status = %d" % (runStr, status)
		raise RuntimeError( msg )
	    time.sleep(1)
		
	print "Getting image"
	data = cam.GetImage()

	print "Saving image to file"
	imgName = "object"

	header = pyfits.Header(pyfits.Header(GetCameraInfo(cam)))
	for k, v, c in [('DATE-OBS',	expdatetime.strftime("%Y-%m-%d"), 	"") ,
			('UT',		expdatetime.strftime("%H:%M:%S"), 	""),
			('EXPTIME',	exposeTime,				"Exposure Time") ]:
		header.append((k,v,c))

	pyfits.writeto( "%s%s-%d.fits" % (imgName, expdatetime.strftime("%Y%m%d%H%M%S"),camid), \
					data.reshape((row,col)), header=header )
	print data.mean(), data.std()
						
	cam.CloseConnection()

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
			    format='%(asctime)s %(levelname)-8s %(message)s',)
	#                    datefmt='%a, %d %b %Y %H:%M:%S',
	#                    filename='/temp/myapp.log',
	#                    filemode='w')

	cams = GetCamConnection()
	pool=Pool(len(cams))
#	pool.apply(camprocess,zip(cams,range(len(cams))))
	pool.map(camprocess,range(len(cams)))
#	pool.map(test,range(len(cams)))
	pool.close()

