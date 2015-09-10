?@echo off
rem
rem A batch file to support AllunaToolKit
rem

rem Settings
set PATH=%PATH%;"c:\Python27"
set PYTHONPATH=%PYTHONPATH%;"C:\Program Files\ZeroC\Ice-3.5.1\python"
set today_YYYYMMDD=%date:~0,4%%date:~5,2%%date:~8,2%


rem Change the directory to the current directory.
pushd %0\..
cls

python TelescopeSrv.py >> %0\..\Telescope%today_YYYYMMDD%.log 2>&1 &

exit
