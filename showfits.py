#! /usr/bin/env python
#
#   show FLI camera images on ds9
#      showfits.py
#
#     Ver 1.0 2018/06/13   H. Akitaya
#     Ver 1.1 2019/11/05   M. Sasada

import sys,os,re,tempfile, time, shutil
import astropy.io.fits as fits
import datetime
from subprocess import Popen, PIPE
import config

IntPattern = re.compile('\d+')
TMPIMGDIR=config.DATADIR
#RECENTFN_RECORD_COMMON_FN="recent.log"

imginfo=[['0', 0.0], ['1', 0.0], ['2', 0.0]]

def showFitsImage(fn, frame_n):
    #cmd0 = "xpaget xpans"
    os.system("xpaset -p ds9 frame %s"%str(int(frame_n)+1))
    os.system("cat %s | xpaset ds9 fits"%fn)
    os.system("xpaset -p ds9 frame center")
    os.system("xpaset -p ds9 zoom to fit")
    os.system("xpaset -p ds9 scale mode zscale")
    if int(Frame) == 0 or int(Frame) == 2:
        os.system("xpaset -p ds9 orient X")

def getRecentFn(info):
    File = "recent." + info[0] + ".log"
    FILE = os.path.join(TMPIMGDIR,File)
    return FILE
    #return ('%s%s%s' % (TMPIMGDIR, info[1], RECENTFN_RECORD_COMMON_FN))

def checkFileUpdate():
    for info in imginfo:
        fn = getRecentFn(info)
        if not os.path.isfile(fn):
            continue
        try:
            f = open(fn, 'r')
            fitsfn=f.readline().strip()
            f.close()
        except:
            continue
        if os.path.isfile(fitsfn):
            tms = os.stat(fitsfn).st_mtime
            if (tms > info[2]):
                showFitsImage(fitsfn, info[0])
#                showFitsImage(d, fitsfn, info[0])
                info[2] = tms
                dt = datetime.datetime.fromtimestamp(tms)
                print("%s: %s" % (dt.strftime('%Y/%m/%d %H:%M:%S'), os.path.basename(fitsfn)))

def loopChkFile():
    while(True):
        try:
            checkFileUpdate()
            time.sleep(1)
        except KeyboardInterrupt:
            sys.stderr.write('Ctrl+C Interruption\n')
            exit(1)

if __name__ == "__main__":
    loopChkFile()
