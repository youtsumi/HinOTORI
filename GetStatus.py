#/usr/bin/env python
import SimpleExposure
import logging
import sys

logging.basicConfig(level=logging.INFO,
			format='%(asctime)s %(levelname)-8s %(message)s',
			filename="/dev/null"
			)

if __name__ == "__main__":
	cam = SimpleExposure.GetCamConnection()
	for k, v in SimpleExposure.GetCameraInfo(cam):
		print k, v
	cam.CloseConnection()

