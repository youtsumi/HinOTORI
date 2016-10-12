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
		elif config.mount["mounttype"] == "HinOTORI":
			mount = HinOTORIMount()
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

class HinOTORIMount(HinOTORI.Mount):
        def __init__(self):
		import mount
		focusmodel=mount.FocusModel(0.,0.,0.,0.,0.,mount.FocusModel.TWO_LINES)
		weatherstatus="./log/log.$date.txt"     # need to define before passing below methods
		weatherstatusfile= "./weather.out"
		telstatus="./log/telescope_$date.status"
		rainstatusfile="./rain.out"
		status= mount.TelescopeStatus(telstatus,rainstatusfile)
		weather=mount.WeatherStatus(weatherstatus, weatherstatusfile )
		self.mount=mount.Telescope(config.mount["ip"],config.mount["port"],config.mount["t_point.txt"],status,weather,focusmodel,mount.Telescope.AUTO)
                HinOTORI.Mount.__init__(self)

        def GetRa(self,current=None):
		return self.mount.getRA()

        def GetDec(self,current=None):
		return self.mount.getDec()

        def GetAz(self,current=None):
		return self.mount.getAz()

        def GetEl(self,current=None):
		return self.mount.getElv()

	def SetRa(self,radeg,current=None):
		self.radeg=radeg

	def SetDec(self,decdeg,current=None):
		self.decdeg=decdeg

	def Goto(self,current=None):
		return self.mount.slew(self.radeg,self.self.radeg)

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
