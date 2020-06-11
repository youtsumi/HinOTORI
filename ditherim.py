#!/usr/bin/python
import sys,os,math
#sys.path.append("/home/utsumi/bin")
import config
import argparse

Command = True

def CombDither(ndith,Sep):
    if ndith % 2 == 0:
        oddeven = 0
        N = ndith - 1
    else:
        oddeven = 1
        N = ndith
    comb = []
    theta = 2.0*math.pi / N
    if oddeven == 0: comb.append([0.0,0.0])
    for i in range(N):
        comb.append([float(Sep)*math.cos(i*theta),float(Sep)*math.sin(i*theta)])
    return comb

def DitherExposure(u,R,I,dither,Delta,focus=None,OBJECT="test",user=None,Path=None):
    Coord = CombDither(dither,Delta)
    for i in range(len(Coord)):
        print("\ndither %s / %s \n"%(i+1,dither))
        Dra,Ddec = str(Coord[i][0]),str(Coord[i][1])
        cmd = './MountOffsetClient.py --offset %s %s'%(Dra,Ddec)
        print(cmd)
        if Command == True: os.system(cmd)
        #os.system("IsTelReady")
        if focus != None:
            cmd = 'ChangeAbsFocus.py %s' % focus
	    print(cmd)
	    if Command == True: os.system(cmd)
        cmd = './CameraClient.py -o %s -t %s,%s,%s -n %s %s'%(OBJECT,u,R,I,i,(len(Coord)-1))
        if user != None: cmd = cmd + " -u %s"%user
        if Path != None: cmd = cmd + " -p %s"%Path
        print cmd
        if Command == True: os.system(cmd)
        #os.system("IsTelReady")
        print("\nFinish dithering observation")
    return

parser = argparse.ArgumentParser(
    prog="Dithering script",
    usage="ditherim.py -t 10.0 2.0 2.0 -n 5 -d 60.0",
    description="Do dithering observation for HinOTORI system", 
    add_help = True
)

parser.add_argument('-t', '--texp',  help='u-, R-, and I-band exposures',
                    type=float, required=True, nargs=3)
#                    metavar = "Exposure times for u, R, and I bands: exp-u exp-R exp-I")
parser.add_argument('-n', help='Number of dithering',
                    type=int, required=True)
#parser.add_argument('-c','--coord', help='Coordinate RA and Dec of object in degree',
#                    type=float, nargs=2, metavar = 'Coordinate; RA Dec')
parser.add_argument('-d', '--delta', help='Delta position for dithering in arcsec unit',
                    type=float, default=60.0)
parser.add_argument('-z', '--focus', help='Focus position',
                    type=float, default=None)
parser.add_argument('-o', '--object', help='Object name',
                    type=str, default="TEST")
parser.add_argument('-u', '--observer',help='Observer', type=str)
parser.add_argument('-p', '--path', help='Saved directory', type=str)
args = parser.parse_args()



if __name__ == "__main__":
    exp    = args.texp
    u      = exp[0]
    R      = exp[1]
    I      = exp[2]
    dither = args.n
    Delta  = args.delta
    focus  = args.focus
    OBJECT = args.object
    user   = args.observer
    Path   = args.path
    
    DitherExposure(u,R,I,dither,Delta,focus=focus,OBJECT=OBJECT,user=user,Path=Path)

    sys.exit(0)
