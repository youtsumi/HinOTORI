#!/usr/bin/env python
import CheckServer
import sys, os
import argparse

Parser = argparse.ArgumentParser(
        prog="Server Stop",
        usage="python StopServer.py MountSrv.py",
        description='HinOTORI Server Starter.',
        add_help=True)
Parser.add_argument('server', metavar='server', type=str, nargs=1,
		    help='Select Server')
args = Parser.parse_args()

Srv = args.server[0]
CheckServer.StopServer(Srv)
#Check = CheckServer.CheckServer(Srv)
#if Check == 0:
#    sys.exit(0)
#elif Check == 1:
#    CheckServer.StopServer(Srv)
#else:
#    sys.exit(0)

