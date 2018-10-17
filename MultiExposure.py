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

def GetCamConnections( ):
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

	for cam in cams:
		print cam.GetSerialNumber()

	return cams

def GetCamConnection( num ):
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

	return SetupDevice.CreateAndConnectCam( devices[num] )



def GetCameraInfo( obj ):
	excludelist = [
		"GetImage", # readout
		"GetInfo", # contains duplicated infomation
		"GetStatus", # contains duplicated infomation
		"GetStatusStr", # contains duplicated infomation
		"GetUsbFirmwareVersion", # 
		"GetMacAddress", # 
		"GetUsbVendorInfo", # 
		"GetAdcGain", # 
		"GetAdcOffset", # 
		"GetSerialBaudRate", # 
		"GetSerialFlowControl", # 
		"GetSerialParity", # 
		"GetUsbVendorInfo", # 
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


def camprocess( camid, filename, exposeTime, extraheader, shutter ):
#	print caminfo
#	(cam, camid) = caminfo
	cam = camid
	#print some basic info
	print cam, camid
	row = cam.GetMaxImgRows()
#	col = cam.GetMaxImgCols()
	col = cam.GetMaxImgCols() + cam.GetNumOverscanCols()
	cam.SetRoiNumCols(cam.GetMaxImgCols() + cam.GetNumOverscanCols())
	print "Imaging rows = %d, columns = %d" % ( row, col )

	count = 1
	cam.SetImageCount( count )
	print "Starting %f sec light exposure" % (exposeTime) 
	expdatetime = datetime.datetime.utcnow()
	cam.StartExposure( exposeTime, shutter )
#	cam.StartExposure( exposeTime, False )
			
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

	header = pyfits.Header( [('DATE-OBS',	expdatetime.strftime("%Y-%m-%d"), 	"") ,
				 ('UT',		expdatetime.strftime("%H:%M:%S"), 	""),
				 ('EXPTIME',	exposeTime,				"Exposure Time") ] ) 

	if extraheader is not None:
		header.extend(extraheader)

	header.extend(GetCameraInfo(cam))

	pyfits.writeto( filename, data.reshape((row,col)), header=header )
	print data.mean(), data.std()
						

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
			    format='%(asctime)s %(levelname)-8s %(message)s',)
	#                    datefmt='%a, %d %b %Y %H:%M:%S',
	#                    filename='/temp/myapp.log',
	#                    filemode='w')

	cams = GetCamConnections()
	for i in range(3):
		time.sleep(5)
		pool=Pool(len(cams))
	#	pool.apply(camprocess,zip(cams,range(len(cams))))
		pool.map(camprocess,range(len(cams)))
	#	pool.map(test,range(len(cams)))
	pool.close()

	for i in range(3):
		cams[i].CloseConnection()

