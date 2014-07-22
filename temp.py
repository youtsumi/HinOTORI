#!/usr/bin/env python
import os
import MultiExposure 
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
			cams = MultiExposure.GetCamConnection()
			for i, cam in enumerate(cams):
				try:
					for method in ["GetTempCcd","GetTempHeatsink","GetCoolerStatus","GetCoolerSetPoint","GetCoolerBackoffPoint","GetFanMode","GetCoolerDrive"]:
						ret = getattr(cam,method)()
						logging.debug("ccd[%d]%s: %s" % ( i, method, ret ) )
				except AttributeError:
					pass
				cam.CloseConnection()
			time.sleep(60)

		except KeyboardInterrupt:
			exit(0)

		except:
			raise
