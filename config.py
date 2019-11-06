### This configuration file is written in python2 format
### Camera configuration
### Note that the serial number should be written by user when one have new one
camera=[
	{
		'serial': 131741,
		'filter': 'u',
		'uid': 0,
		'gain': 1.7	# from the spec sheet
	},
	{
		'serial': 121431,
		'filter': 'Rc',
		'uid':	1,
		'gain': 1.3
	},
	{
		'serial': 121430,
		'filter': 'Ic',
		'uid': 2,
		'gain': 1.50
	}
]

### Server configuration
nodesetting={
	'camera': { 
#		'ip': "192.168.0.38",
		'ip': "127.0.0.1",
		'port': 10009
		},
	'mount' : {
#		'ip': "124.31.254.16",
		'ip': "127.0.0.1",
		'port': 10002
		},
	'telescope': {
#                'ip': "192.168.0.248",
                'ip': "192.168.154.1",
#		'ip': "124.31.254.16",
#		'ip': "127.0.0.1",
		'port': 10001
#		'port': 51111
		},
	'dome': {
#                'ip': "192.168.1.116",
#		'ip': "124.31.254.16",
		'ip': "192.168.154.1",
#		'ip': "127.0.0.1",
                'port': 10003      
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
#	'ip': '192.168.1.116',
#	'ip': '124.31.254.16',
	'ip': '192.168.154.1',
	'port': 4676,
	't_point.txt': 't_point.txt'
}

### A directory to be stored
import datetime,os
#DATADIR = "/mnt/disk1/data/"
DATADIR = "/home/utsumi/Data/"
DATE    = datetime.datetime.utcnow().strftime("%Y%m%d") + "/"
if os.path.isdir(DATADIR):
	targetdir = os.path.join(DATADIR,DATE)
else:
	targetdir = os.path.join("/home/utsumi/data/",DATE)

### Stored Number of Obtained Data Frame
EXPFile = os.path.join(DATADIR,"CurrentEXPID")
FrameNCol = 7

### Stored Today's observational infomation
ObsFile = os.path.join(DATADIR,"CurrentObsInfo")

### focuser conversion factor
focusconv = 0.254e-3    # in mm/step
apptimeout = 60		# sec
ntrial = 3		# sec

### log config
import logging
FORMAT = "%(asctime)-15s[%(levelname)s] %(name)s:%(funcName)s %(process)s:%(thread)s -- %(message)s"
loglevel = logging.DEBUG

### dome ###
domeport = "COM2"
