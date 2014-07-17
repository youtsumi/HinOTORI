#!/usr/bin/env python
import os
import SimpleExposure
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
        #                    datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='./temp.log',
                            filemode='a')


if __name__ == "__main__":
	while True:
		try:
			cam = SimpleExposure.GetCamConnection()
			for method in ["GetTempCcd","GetTempHeatsink"]:
				ret = getattr(cam,method)()
				logging.debug("%s: %s" % ( method, ret ) )
			cam.CloseConnection()
			time.sleep(60)

		except KeyboardInterrupt:
			exit(0)

		except:
			pass
