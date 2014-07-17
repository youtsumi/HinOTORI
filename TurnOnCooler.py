#/usr/bin/env python
import SimpleExposure
import logging
import sys

logging.basicConfig(level=logging.CRITICAL,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        filename="/dev/null"
                        )

if __name__ == "__main__":
        cam = SimpleExposure.GetCamConnection()
	cam.SetCoolerSetPoint( -20. )
	cam.SetCooler( True )
        cam.CloseConnection()

