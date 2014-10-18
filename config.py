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
		'serial': 121430,
		'filter': 'Rc',
		'uid':	1,
		'gain': 1.3
	},
	{
		'serial': 121431,
		'filter': 'Ic',
		'uid': 2,
		'gain': 1.2
	}
]

### Server configuration
nodesetting={
	'camera': { 
		'ip': "127.0.0.1",
		'port': 10000
		},
	'mount' : {
		'ip': "127.0.0.1",
		'port': 10002
		},
	'telescope': {
		'ip': "192.168.0.40",
		'port': 10001
		}
}

### Observatory location
location = {
	'observatory': "Higashi-Hiroshima Observatory",
	'longitude': 132.7767,
	'latitude': 34.3775
}

### configuration for the mount
mount = {
	'mounttype': 'KanataAzEl',
#	'mounttype': 'Simulator',
	'status': '/dev/shm/TELstatus'
}

### A directory to be stored
import datetime
targetdir = "/storage/HinOTORI/%s/" % datetime.datetime.utcnow().strftime("%Y%m%d") 

### focuser conversion factor
focusconv = 0.254e-3    # in mm/step
apptimeout = 20		# sec
ntrial = 3		# sec
