#!/usr/bin/env python
#import SrvCheck
import sys, os
import argparse

parser = argparse.ArgumentParser(
        prog="Focus",
        usage="ChangeAbsFocus.py 3.9 \n",
        description='HinOTORI Telescope Absolute Focus Changer.',
        add_help=True)
parser.add_argument('absolute', metavar='Focus', type=float,
                    default=None, help='Change absolute focus position (mm)')
args = parser.parse_args()

#Srv = "TelescopeSrv.py"
#Check = SrvCheck.CheckServer(Srv)
#if Check == 0:
#    sys.exit(0)
try:
    cmd = "TelescopeClient.py afocus %s"%args.absolute
    os.system(cmd)
except:
    print("WARNING: Telescope cannot communicate")
