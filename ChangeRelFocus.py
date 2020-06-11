#!/usr/bin/env python
#import SrvCheck
import sys, os, subprocess
import argparse

parser = argparse.ArgumentParser(
        prog="Focus",
        usage="python ChangeRelFocus.py 0.1 \n",
        description='HinOTORI Telescope Relative Focus Changer.',
        add_help=True)
parser.add_argument('relative', metavar='Focus', type=float,
                    default=None, help='Change relative focus position (mm)')
args = parser.parse_args()

#Srv = "TelescopeSrv.py"
#Check = SrvCheck.CheckServer(Srv)
#if Check == 0:
#    sys.exit(0)
try:
    cmd = "TelescopeClient.py rfocus %s"%args.relative
    os.system(cmd)
except:
    print("WARNING: Telescope cannot communicate")

