#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI

class MountServer(Ice.Application):
        def run(self,args):
                self.shutdownOnInterrupt()      # make sure clean up
                adapter = self.communicator().createObjectAdapterWithEndpoints(
                        os.path.basename(__file__), "default -p 10002")

                mount = Mount()
                adapter.add(mount, self.communicator().stringToIdentity("Mount"))

                adapter.activate()
                self.communicator().waitForShutdown()
                return 0

class Mount(HinOTORI.Mount):
        def __init__(self):
                HinOTORI.Mount.__init__(self)

        def GetRa(self,current=None):
		return 0.

        def GetDec(self,current=None):
		return 0.

	def SetRa(self,radeg,current=None):
		pass

	def SetDec(self,decdeg,current=None):
		pass

	def Goto(self,current=None):
		pass

if __name__ == "__main__":
        app = MountServer()
        status = app.main(sys.argv)
        sys.exit(status)
