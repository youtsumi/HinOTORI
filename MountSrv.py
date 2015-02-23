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
		os.system("/home/utsumi/src/kanata/a.out &")

	def _getstatus(self):
		import re
		p=re.compile("TelPos_current")
		s=re.compile("[\s]+")
		fh=open(config.mount['status'])
		pos=filter(lambda x: p.match(x) is not None, fh.readlines())
		print s.split(pos[0][16:-1])
		d1,ra,d2,dec,epoch=s.split(pos[0][16:-1])
		self.ra=ra
		self.dec=dec

		d1,az,d2,el=s.split(pos[1][16:-1])
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
