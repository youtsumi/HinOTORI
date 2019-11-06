#!/usr/bin/env python
import subprocess,glob,os,time,sys
import config
def DS9Find():
    cmd   = "ps -aef"
    tasks = subprocess.check_output(cmd.strip().split(" ")).split("\n")
    flag  = False
    for task in tasks:
        if task.find("ds9") > -1 and task.find("grep") == -1 and task.find("emacs") == -1:
            flag = True
    return flag

def ReadImage(File,Frame):
    os.system("xpaset -p ds9 frame %s"%str(int(Frame)+1))
    os.system("cat %s | xpaset ds9 fits"%File)
    os.system("xpaset -p ds9 frame center")
    os.system("xpaset -p ds9 zoom to fit")
    if int(Frame) == 0 or int(Frame) == 2:
        os.system("xpaset -p ds9 orient X")

def ShowDS9():
#    os.system("open -a /Applications/SAOImage\ DS9.app")
    os.system('ds9 -geometry 720x1200 &')
    time.sleep(4)
    os.system("xpaget xpans")
    os.system("xpaset -p ds9 frame 1")
    os.system("xpaset -p ds9 cmap bb")
    os.system("xpaset -p ds9 preserve scale")
    os.system("xpaset -p ds9 preserve pan")
    os.system("xpaset -p ds9 frame 2")
    os.system("xpaset -p ds9 cmap bb")
    os.system("xpaset -p ds9 preserve scale")
    os.system("xpaset -p ds9 preserve pan")
    os.system("xpaset -p ds9 frame 3")
    os.system("xpaset -p ds9 cmap bb")
    os.system("xpaset -p ds9 preserve scale")
    os.system("xpaset -p ds9 preserve pan")
    os.system("xpaset -p ds9 tile mode column")
    os.system("xpaset -p ds9 tile")
    os.system("xpaset -p ds9 frame 1") 


if __name__ == "__main__":
    #argvs = sys.argv  
    #argc = len(argvs) 

    #PWD = os.getcwd()
    #os.chdir(config.targetdir)

    if not DS9Find():
        ShowDS9()

    #try:
    #    if argc == 1:
    #        files = glob.glob("*-?.fits")
    #        files.sort(key=os.path.getmtime, reverse=True)
    #        ID    = files[0].split("-")[0]
    #    else:
    #        ID    = str(argvs[1]).split("-")[0]
    #except:
    #    print("Can not find FITS files.")
    #    sys.exit(0)
    #for i in range(3):
    #    if os.path.exists(ID+"-" + str(i) + ".fits"):
    #        FITS = ID+"-" + str(i) + ".fits"
    #        ReadImage(FITS,str(i))

    #os.chdir(PWD)

