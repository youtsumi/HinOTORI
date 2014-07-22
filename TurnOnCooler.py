#/usr/bin/env python
import MultiExposure
import logging
import sys

logging.basicConfig(level=logging.CRITICAL,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        filename="/dev/null"
                        )

if __name__ == "__main__":
        cams = MultiExposure.GetCamConnection()
	for cam in cams:
		cam.SetCoolerSetPoint( -20. )
		cam.SetCooler( True )
		cam.CloseConnection()

