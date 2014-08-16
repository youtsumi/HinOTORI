?@echo off
rem
rem A batch file to support AllunaToolKit
rem

rem Settings
set PATH=%PATH%;"c:\Python27"
set PYTHONPATH=%PYTHONPATH%;"C:\Program Files\ZeroC\Ice-3.5.1\python"

rem Change the directory to the current directory.
pushd %0\..
cls

python TelescopeSrv.py

exit
