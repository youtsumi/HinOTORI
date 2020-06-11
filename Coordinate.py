#!/usr/bin/env python
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
import datetime
import argparse

def Object(obj):
	Cor = SkyCoord.from_name(obj)
	return Cor

def Transform(Cor):
	utc = datetime.datetime.utcnow()
	return Cor.transform_to(FK5(equinox=utc))

def ShowCoord(Cor):
	return Cor.ra.deg, Cor.dec.deg

def CalcCoord(obj):
	Cor = Object(obj)
	Cor1 = Transform(Cor)
	ra, dec = ShowCoord(Cor)
	ra1, dec1 = ShowCoord(Cor1)
	return obj,Cor,Cor1,ra,dec,ra1,dec1

#def AddTarget2List(FLIST):
#	if os.path.exits(FLIST):
#		with open(FLIST,"r") as f:
			

def main(obj):
	obj,Cor,Cor1,ra,dec,ra1,dec1 = CalcCoord(obj)
	print("Object: %s"%obj)
	print("J2000\n%s %s\n%s"%(ra,dec,Cor.to_string('hmsdms')))
	print("current equinox\n%s %s\n%s"%(ra1,dec1,Cor1.to_string('hmsdms')))

parser = argparse.ArgumentParser(
        prog="Convert Coordinate from Object",
        usage="Coordinate.py object \n",
        description='Convert to J2000 and current equinox.',
        add_help=True)
parser.add_argument('object', metavar='object', type=str,
                    help='Object Name')
args = parser.parse_args()

if __name__ == '__main__':
	main(args.object)

