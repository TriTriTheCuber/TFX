:start
@echo off
TITLE TriTriSim Hub
setlocal enabledelayedexpansion
echo Verifying files...
call :verifyfile "TriTriSim Installer 2020.bat"
call :verifyfile "TriTriSim Installer 2024.bat"

:menu
cls
call :title
echo Welcome to the TriTriSim Hub.
echo.
echo Please select the installer you would like to open:
echo.
echo [1] 2020
echo [2] 2024
echo [3] Check for updates
echo.
set /p choice=">>"
if !choice! EQU 1 (call "TriTriSim Installer 2020.bat")
if !choice! EQU 2 (call "TriTriSim Installer 2024.bat")
if !choice! EQU 3 (
	call :forcefiledownload "TriTriSim Installer 2020.bat"
	call :forcefiledownload "TriTriSim Installer 2024.bat"
goto menu
)
exit /b





:verifyfile
IF NOT EXIST "%~1" (
call :forcefiledownload "%~1" 
)
exit /b 0


:forcefiledownload
 powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/TriTriTheCuber/TFX/main/%~1' -OutFile '%~1' -UseBasicParsing"
exit /b 0









:title
echo.
echo        ================================================
echo                         TriTriSim Hub            
echo             Developed by TriTriTheCuber / TriTriSim     
echo                             v1.0
echo        ================================================
echo.