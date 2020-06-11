#!/usr/bin/env python
import os, subprocess, psutil, signal
import argparse

def find_procs_by_cmd(cmd,exclude=None,Print=True):
        "Return a list of processes matching cmd."
        ls = []
        for p in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
                if cmd == p.info['name'] or \
                   p.info['exe'] and os.path.basename(p.info['exe']) == cmd or \
                   p.info['cmdline'] and p.info['cmdline'][0] == cmd:
                        if cmd in str(p.info['cmdline']) and 'Srv.py' not in str(p.info['cmdline']) :
#                        if cmd in str(p.info['cmdline']) and 'Server.py' not in str(p.info['cmdline']) :
                                if exclude != None and exclude not in str(p.info['cmdline']):
                                        ls.append(p.pid)
                                elif exclude == None:
                                        ls.append(p.pid)
        if Print == True:
                for pid in ls:
                        p = psutil.Process(pid)
                        print(p.cmdline())
        return ls

def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True,
                   timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
    """
    assert pid != os.getpid(), "won't kill myself"
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        p.send_signal(sig)
    gone, alive = psutil.wait_procs(children, timeout=timeout,
                                    callback=on_terminate)
    return (gone, alive)

def CheckServer(Server,Print=True):
        Check = find_procs_by_cmd(Server,Print=Print)
        if len(Check) == 0:
                if Print == True:
                        print("### Do Running %s Server ###\n"%Server)
                        print("%s\n\n"%Server)
                return 0
        elif len(Check) > 0:
                if Print == True:
                        print("### Running %s Server ###\n"%Server)
                return 1

def CheckServerorg(Server,Print=True):
        cmd = "ps -aux | grep %s | grep python | grep -v emacs | grep -v grep | wc -l" %Server
        aa = subprocess.getoutput(cmd)
        if aa == "0":
                if Print == True:
                        print("### Do Running %s Server ###\n"%Server)
                        print("%s\n\n"%Server)
                return 0
        elif aa == "1":
                if Print == True:
                        print("### Running %s Server ###\n"%Server)
                return 1

def StartServer(Server,Print=True):
        Check = CheckServer(Server,Print=False)
        if Check == 0:
                cmd = "%s &"%Server
                os.system(cmd)
                if Print == True:
                        print("### Start %s Server ###\n"%Server)
                return

def StopServer(Server,Print=True):
        Check = CheckServer(Server,Print=False)
        if Check == 1:
                IDs = find_procs_by_cmd(Server,name="python",Print=False)
                exIDs = find_procs_by_cmd("Client",name="python",Print=False)
                if len(exIDs) == 0:
                        for pid in IDs:
                                kill_proc_tree(pid)
                if Print == True:
                        print("### Stop %s Server ###\n"%Server)
                return

#parser = argparse.ArgumentParser(
#        prog="Server Checker",
#        usage="python SrvCheck.py -s MountSrv.py \n or \n python SrvCheck.py",
#        description='HinOTORI Server Checker.',
#        add_help=True)
#parser.add_argument('-s','--server', metavar='server', type=str, nargs=1, default=None,
#		    help='Select Server')

#args = parser.parse_args()


if __name__ == "__main__":
#        if args.server == None:
        #servs = ['CameraSrv.py','DomeSrv.py','MountSrv.py','TelescopeSrv.py']
        servs = ['CameraSrv.py','MountSrv.py']
        for ser in servs:
                CheckServer(ser)
#        else:
#                ser = args.server[0]
#                CheckServer(ser)
#        #print(servs)

