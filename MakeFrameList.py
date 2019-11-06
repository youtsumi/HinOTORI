#!/usr/bin/python
from astropy.io import fits as pf
from astropy.time import Time
import sys,os,glob
sys.path.append("/home/utsumi/bin")
import config
import argparse

def ChangeDir(DIR):
    if os.path.exists(DIR): 
        cDIR = os.getcwd()
        os.chdir(DIR)
        return cDIR
    else:
        print("%s does not exist"%DIR)
        return

def ExistKey(Header, KEY, EXCEPT=None):
    try:
        return Header[KEY]
    except:
        return EXCEPT

def Header(Fits):
    hdulist  = pf.open(Fits)
    prihdr   = hdulist[0].header
    EXPID    = ExistKey(prihdr, "EXP-ID")
    FRAMEID  = ExistKey(prihdr, "FRAMEID")
    OBJECT   = ExistKey(prihdr, "OBJECT", "none")
    FILTER   = ExistKey(prihdr, "FILTER")
    EXPTIME  = ExistKey(prihdr, "EXPTIME")
    RA       = ExistKey(prihdr, "RA-DEG")
    DEC      = ExistKey(prihdr, "DEC-DEG")
    CDITH    = ExistKey(prihdr, "CDITHER")
    NDITH    = ExistKey(prihdr, "NDITHER")
    if OBJECT.lower().find("dark") > -1:
        MODE = "DARK"
    elif OBJECT.lower().find("flat") > -1:
        MODE = "FLAT"
    else:
        MODE = "OBJECT"
    TIME     = Time(ExistKey(prihdr, "DATE-OBS", "2018-05-17")+" "+ExistKey(prihdr, "UT", "15:01:02"))
    MJD      = TIME.mjd
    MEAN     = hdulist[0].data.astype("float").mean()
    LINE     = hdulist[0].data.astype("float").flatten()
    LINE.sort()
    MEDIAN   = LINE[int(len(LINE)/2)]
    STD      = hdulist[0].data.astype("float").std()
    MAX      = hdulist[0].data.astype("float").max()
    return [EXPID,FRAMEID,MODE,EXPTIME,FILTER,RA,DEC,OBJECT,CDITH,NDITH,MJD,MEAN,MEDIAN,STD,MAX]

parser = argparse.ArgumentParser(
        prog="Make Frame List",
        usage="MakeFrameList.py -d directory \n",
        description='Print Header info to log file.',
        add_help=True)
parser.add_argument('-d', '--directory', metavar='directory', type=str,
                    default=config.targetdir, help='Directory to save log file')
args = parser.parse_args()


if __name__ == '__main__':
    import glob
    import pandas as pd
    currentdir = ChangeDir(args.directory)
    LIST   = glob.glob("*-?.fits")
    Column = ["EXPID","FRAMEID","MODE","EXPTIME","FILTER","RA","DEC","OBJECT","CDITH","NDITH","MJD","MEAN","MEDIAN","STD","MAX"]
    aa     = {}
    for F1 in LIST:
        aa[F1] = Header(F1)

    outf = "header.log"
    data = pd.DataFrame(aa,index=Column).T
    data = data.sort_values('MJD', ascending=False)
    data = data.sort_index()
    data.to_csv(outf,sep="\t")
    currentdir = ChangeDir(currentdir)
    print("Saved log file is : \n%s" % os.path.join(currentdir, outf))


