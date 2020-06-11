#!/usr/bin/env python
#import SrvCheck
import sys, os
#import argparse

#Srv = "TelescopeSrv.py"
#Check = SrvCheck.CheckServer(Srv)
#if Check == 0:
#    sys.exit(0)
try:
    cmd = "TelescopeClient.py cfocus"
    os.system(cmd)
except:
    print("WARNING: Telescope cannot communicate")
