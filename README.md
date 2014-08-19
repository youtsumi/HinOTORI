HinOTORI Control softwares
==========================
HinOTORI is a project to develop a new robotic telescope with 3 colours simultaneous imaging system in Tibet. This software package enables the telescope system to be robotic.

The process communication is established by Internet Communication Engine (Ice). This is a very convenient middleware to establish communications over nodes using the Sun Remote Procedure Call.

You should copy this softwares on your related machines. Also you should setup Ice on each node.

Once you run "LaunchAlluna.bat" on a windows machine, then you can control TCS, cameras with client softwares outside if you make network connections appropriately. If you hate windows screen, you should prepare Ice with ptyhon cabability and Alluna TCS, and then just put this batch file on the "start up" menu.n

This software assumes for the camera control that the cameras (Apogee) are connected to one Linux machine.

Requirement
-----------
- Ice 3.5.1 with python2.7(32bit)
- pywinauto -- This only supports 32bit python from my understanding. If it's wrong, you can go 64bit.
- Alluna Telescope Control System 10.6
- libapogee with a ``tweak''
- pyephem

Links
-----
- http://www.alluna-optics.com
- http://www.zeroc.com/ice.html
- http://hinotori.hiroshima-u.ac.jp

AUTHOR
------
Yousuke Utsumi (youtsumi@hiroshima-u.ac.jp)

![logo](http://hinotori.hiroshima-u.ac.jp/logo.jpg)

