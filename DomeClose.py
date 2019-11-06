#!/usr/bin/env python
#import SrvCheck
import sys, os

#Srv = "DomeSrv.py"
#Check = SrvCheck.CheckServer(Srv)
#if Check == 0:
#    sys.exit(0)
cmd = "./DomeClient.py close"
os.system(cmd)

