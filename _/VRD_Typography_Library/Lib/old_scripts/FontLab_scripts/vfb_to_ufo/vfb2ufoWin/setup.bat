@ECHO OFF

SET PRODUCT=FontLab vfb2ufo for Windows
SET PROGRAM=vfb2ufo.exe
SET VERSION=2015-01-23
SET WEBSITE=http://blog.fontlab.com/font-utility/vfb2ufo/
SET USAGE=vfb2ufo.exe [options] inputpath [outputpath]

SET PREFIX=%ProgramFiles%\Fontlab\vfb2ufo
SET SUBPREFIX=%ProgramFiles%\Fontlab

SET BASE=%~dp0
CD %BASE%

ECHO.
ECHO == Welcome to the installation of ==
ECHO == %PRODUCT% build %VERSION% ==
ECHO NOTE: You should run this SETUP.BAT file as Administrator!
ECHO (Right-click / Run as administrator)
ECHO.
ECHO %PRODUCT% will be installed into the following folder:
ECHO %PREFIX%
ECHO.
PAUSE

ECHO.
ECHO Installing %PRODUCT% build %VERSION%...
ECHO.

ECHO Creating folders...
MKDIR "%SUBPREFIX%"
MKDIR "%PREFIX%"

ECHO Installing program...
COPY "exe\%PROGRAM%" "%PREFIX%"

ECHO Modifying the PATH environmental variable...
SET OLDPATH=%PATH%
SET NEWPATH=%OLDPATH%;%PREFIX%
REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%NEWPATH%" /f

ECHO.
ECHO == OK! ==
ECHO Installation complete.
ECHO.
ECHO Thank you for choosing %PRODUCT% build %VERSION%.
ECHO.
ECHO *** To complete the installation, you need to ***
ECHO *** log out from Windows and log in again! ***
ECHO. 
ECHO To convert between VFB and UFO, use:
ECHO %USAGE%
ECHO To get more help, use:
ECHO %PROGRAM% -h
ECHO.
ECHO For updates and development news, visit:
ECHO %WEBSITE%
ECHO.
ECHO Please log out from Windows and log in again. 
PAUSE
