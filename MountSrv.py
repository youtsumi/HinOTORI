#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
import config

class MountServer(Ice.Application):
        def run(self,args):
                self.shutdownOnInterrupt()      # make sure clean up
                adapter = self.communicator().createObjectAdapterWithEndpoints(
                        os.path.basename(__file__), "default -h %s -p %d"
				 % ( \
                                        config.nodesetting["mount"]['ip'], \
                                        config.nodesetting["mount"]['port'] \
                                ))

		if config.mount["mounttype"] == "KanataAzEl":
			mount = KanataMount()
		else:
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

        def GetAz(self,current=None):
		return 0.

        def GetEl(self,current=None):
		return 0.

	def SetRa(self,radeg,current=None):
		pass

	def SetDec(self,decdeg,current=None):
		pass

	def Goto(self,current=None):
		pass

class KanataMount(HinOTORI.Mount):
        def __init__(self):
                HinOTORI.Mount.__init__(self)
		os.system("/home/utsumi/kanata/a.out &")

	def _getstatus(self):
		import re
		p=re.compile("TelPos_current")
		fh=open(config.mount['status'])
		pos=filter(lambda x: p.match(x) is not None, fh.readlines())
		ra,dec,epoch=pos[0][16:-1].split("  ")
		self.ra=ra[3:]
		self.dec=dec[4:]

		d1,az,d2,el=pos[1][16:-1].split("  ")
		print az, el
		self.az=az
		self.el=el
		fh.close()

        def GetRa(self,current=None):
		import ephem
		self._getstatus()
		return ephem.hours(self.ra)

        def GetDec(self,current=None):
		import ephem
		self._getstatus()
		return ephem.degrees(self.dec)

        def GetAz(self,current=None):
		self._getstatus()
		return float(self.az)

        def GetEl(self,current=None):
		self._getstatus()
		return float(self.el)

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
