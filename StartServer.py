#!/usr/bin/env python
import CheckServer
import sys, os
import argparse

parser = argparse.ArgumentParser(
        prog="Server Start",
        usage="python StartServer.py MountSrv.py",
        description='HinOTORI Server Starter.',
        add_help=True)
parser.add_argument('server', metavar='server', type=str, nargs=1,
		    help='Select Server')
args = parser.parse_args()

Srv = args.server[0]
CheckServer.StartServer(Srv)
#Check = CheckServer.CheckServer(Srv)
#if Check == 1:
#    sys.exit(0)
#elif Check == 0:
#    CheckServer.StartServer(Srv)
#else:
#    sys.exit(0)

