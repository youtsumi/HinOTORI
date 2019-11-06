#!/anaconda3/bin/python
#!/usr/bin/python
from astropy.io import fits as pf
from astropy.time import Time
import sys,os,glob
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
        prog="Print Header",
        usage="PrintHeaderHinOTORI.py -f file \n",
        description='Print Header info to log file.',
        add_help=True)
parser.add_argument('file', metavar='file', type=str,
                    help='Fits file to show header info')
args = parser.parse_args()


if __name__ == '__main__':
    F1     = args.file
    print("File: %s" % F1)
    Column = ["EXPID","FRAMEID","MODE","EXPTIME","FILTER","RA","DEC","OBJECT","CDITH","NDITH","MJD","MEAN","MEDIAN","STD","MAX"]
    header = Header(F1)
    for i in range(len(Column)):
        print("%s\t %s"%(Column[i],header[i])) 

