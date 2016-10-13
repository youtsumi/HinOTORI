### This configuration file is written in python2 format
### Camera configuration
### Note that the serial number should be written by user when one have new one
camera=[
	{
		'serial': 131741,
		'filter': 'u',
		'uid': 0,
		'gain': 1.7	# from the spec sheet
	}
#	{
#		'serial': 121430,
#		'filter': 'Rc',
#		'uid':	1,
#		'gain': 1.3
#	},
#	{
#		'serial': 121431,
#		'filter': 'Ic',
#		'uid': 2,
#		'gain': 1.2
#	}
]

### Server configuration
nodesetting={
	'camera': { 
#		'ip': "192.168.0.38",
		'ip': "127.0.0.1",
		'port': 10000
		},
	'mount' : {
		'ip': "127.0.0.1",
		'port': 10002
		},
	'telescope': {
                'ip': "192.168.0.248",
		'port': 10001
		},
	'dome': {
                'ip': "192.168.0.248",
                'port': 10002      
		}

}

### Observatory location
location = {
	'observatory': "Ali Observatory",
	'longitude': 80.030018,
	'latitude':32.31373 
}

### configuration for the mount
mount = {
#	'mounttype': 'KanataAzEl',
#	'mounttype': 'Simulator',
	'mounttype': 'HinOTORI',
	'status': '/dev/shm/TELstatus',
	'ip': '192.168.1.106',
	'port': 4676,
	't_point.txt': 't_point.txt'
}

### A directory to be stored
import datetime
targetdir = "/home/utsumi/data/%s/" % datetime.datetime.utcnow().strftime("%Y%m%d") 

### focuser conversion factor
focusconv = 0.254e-3    # in mm/step
apptimeout = 60		# sec
ntrial = 3		# sec

### log config
import logging
FORMAT = "%(asctime)-15s[%(levelname)s] %(name)s:%(funcName)s %(process)s:%(thread)s -- %(message)s"
loglevel = logging.DEBUG

### dome ###
domeport = "COM6"
