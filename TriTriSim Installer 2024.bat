@echo off

:start
TITLE TriTriSim Installer

setlocal enabledelayedexpansion 
call :page 0

set selection=0

IF NOT EXIST "temp" (
	mkdir temp
)
IF NOT EXIST "state2024" (
	mkdir state2024
)

call :verifyfile "printmulti.ps1"
call :verifyfile "detect_community2024.ps1"
call :verifyfile "zipdownloadmanager.ps1"

call :buildstate
call :prebuildcs
call :getCommunityPath
call :buildcommunitystate
echo Using Community path: %COMMUNITY_PATH%

set FILES=772.txt 320CFM.txt 320IAE.txt 320N.txt 380.txt 77f.txt
set BASEURL=https://raw.githubusercontent.com/TriTriTheCuber/TFX/main/2024/
set FILEPATH=%%~dp0
set TARGET=Installerinserts2024

call :getstate devmode
IF %state% EQU 1 (
set DEVMODE=1
) else (
call :getupdatedfiles
set DEVMODE=0
)

::77f filepath:           pmdg-aircraft-77f\SimObjects\Airplanes\PMDG 777F\attachments\pmdg\Function_Exterior_77F\model\77F_Exterior.xml

:f
call :prompt
goto f




:verifyfile
IF NOT EXIST %~1 (
    	powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/TriTriTheCuber/TFX/main/%~1' -OutFile '%~1' -UseBasicParsing"
)
exit /b 0






:prompt


call :getstate devmode
IF %state% EQU 1 (
set DEVMODE=1
) else (
set DEVMODE=0
)

cls
color 7
call :title
call :getpage

If %DEVMODE% EQU 1 (
call :fastprint "Devmode enabled|White"
call :fastprint "Page %cpage%|White"
)


call :getcommunitystate communitypath
set "COMMUNITY_PATH=%state%"

IF %cpage% EQU 1 (
    call :TFXprompt
) else (
    IF %cpage%==s (
    call :Settings
    ) else (
    call :SelMenu
    )
)
exit /b 0



:print
powershell -Command "Write-Host '%~1' -ForegroundColor %~2"
EXIT /B 0

:fastprint
:: %* contains all args as one space-separated list
:: We’ll pass them along to PowerShell as individual string[] parameters
powershell -ExecutionPolicy Bypass -File "printmulti.ps1" %*
exit /b 0




::TFX Prompt

:TFXprompt
IF EXIST "Installerinserts2024" (
call :fastprint "TFX Installer - Please select a compatible aircraft|Green" "---------------------------------------------------------------------|White" 
call :planecheck "pmdg-aircraft-77er\" , "[1] PMDG 777-200ER" , "pmdg-aircraft-77er\SimObjects\Airplanes\PMDG 777-200ER\attachments\pmdg\Function_Exterior_772\model\772_Exterior_Behavior.xml" , "InstallerInserts2024/772.txt"
call :planecheck "pmdg-aircraft-77f\" , "[2] PMDG 777F" , "pmdg-aircraft-77f\SimObjects\Airplanes\PMDG 777F\attachments\pmdg\Function_Exterior_77F\model\77F_Exterior_Behavior.xml" , "InstallerInserts2024/772.txt"
call :planecheck "fnx-aircraft-320\" , "[3] Fenix A320" , "fnx-aircraft-320\SimObjects\Airplanes\FNX_320_CFM\Model\FNX320_Exterior_CFM.xml" , "InstallerInserts2024/320CFM.txt"
call :planecheck "flybywire-aircraft-a320-neo\" , "[4] Flybywire A320 Neo" , "flybywire-aircraft-a320-neo\SimObjects\AirPlanes\FlyByWire_A320_NEO\model\A320_NEO.xml"  ,"InstallerInserts2024/320N.txt"
call :planecheck "flybywire-aircraft-a380-842\" , "[5] Flybywire A380" , "flybywire-aircraft-a380-842\SimObjects\AirPlanes\FlyByWire_A380_842\model\A380_EXTERIOR.xml"  ,"InstallerInserts2024/380.txt"
call :fastprint "---------------------------------------------------------------------|White" 
call :uplanecheck "pmdg-aircraft-77er\" "[U1] Uninstall PMDG 777-200ER" "pmdg-aircraft-77er\SimObjects\Airplanes\PMDG 777-200ER\attachments\pmdg\Function_Exterior_772\model\772_Exterior_Behavior.xml"
call :uplanecheck "pmdg-aircraft-77f\" , "[U2] Uninstall PMDG 777F" , "pmdg-aircraft-77f\SimObjects\Airplanes\PMDG 777F\attachments\pmdg\Function_Exterior_77F\model\77F_Exterior_Behavior.xml"
call :uplanecheck "fnx-aircraft-320\" , "[U3] Uninstall Fenix A320" , "fnx-aircraft-320\SimObjects\Airplanes\FNX_320_CFM\Model\FNX320_Exterior_CFM.xml"
call :uplanecheck "flybywire-aircraft-a320-neo\" , "[U4] Uninstall Flybywire A320 Neo" , "flybywire-aircraft-a320-neo\SimObjects\AirPlanes\FlyByWire_A320_NEO\model\A320_NEO.xml"
call :uplanecheck "flybywire-aircraft-a380-842\" , "[U5] Uninstall Flybywire A380" , "flybywire-aircraft-a380-842\SimObjects\AirPlanes\FlyByWire_A380_842\model\A380_EXTERIOR.xml"
call :fastprint "---------------------------------------------------------------------|White" "[F] Update all|White" "[C] Check for updates|White" "---------------------------------------------------------------------|White" "[A] Install All|Green" "[U] Uninstall All|Red" "---------------------------------------------------------------------|White" "[S] Settings|White" "---------------------------------------------------------------------|White"
If EXIST "%COMMUNITY_PATH%/TFX-fxlib" (call :fastprint "[B] Uninstall base package|Red") else (call :fastprint "[B] Install base package|Green") 
If EXIST "%COMMUNITY_PATH%/gf-material-lib" (call :fastprint "[M] Material package already installed.|White") else (call :fastprint "[M] Install material package|Green") 
call :fastprint "---------------------------------------------------------------------|White" 
If %DEVMODE% EQU 1 (call :fastprint "[D] Disable devmode|Red" "---------------------------------------------------------------------|White") else (call :fastprint "[D] Enable devmode|Green" "---------------------------------------------------------------------|White") 
echo.
call :fastprint "[Q] Back"
echo.
setlocal enabledelayedexpansion
set /p choice=Enter your selection: 
if /i "!choice!"=="Q" CALL :page 0
if /i "!choice!"=="1" CALL :Install772
if /i "!choice!"=="2" CALL :Install77F
if /i "!choice!"=="3" CALL :Install320
if /i "!choice!"=="4" CALL :Install320N
if /i "!choice!"=="5" CALL :Install380

if /i "!choice!"=="U1" CALL :Uninstall772
if /i "!choice!"=="U2" CALL :Uninstall77F
if /i "!choice!"=="U3" CALL :Uninstall320
if /i "!choice!"=="U4" CALL :Uninstall320N
if /i "!choice!"=="U5" CALL :Uninstall380

if /i "!choice!"=="A" CALL :InstallAll
if /i "!choice!"=="U" CALL :UninstallAllPrompt
if /i "!choice!"=="F" CALL :Reinstall
if /i "!choice!"=="C" CALL :getupdatedfiles
if /i "!choice!"=="D" CALL :toggledevmode
if /i "!choice!"=="B" (If EXIST "%COMMUNITY_PATH%/TFX-fxlib" (call :uninstallbasepackageprompt) else (call :installbasepackage))
if /i "!choice!"=="M" call :installmaterialpackage
if /i "!choice!"=="S" call :page s
pause
) else (
call :print "It seems it is your first time using this application." "White"
set /p choice="Would you like to install the dependencies from github? (quit to cancel, enter to continue): "
echo.
CALL :installdependencies
echo.
set /p choice="Installation done. Press enter to continue."
)
exit /b 0


:SelMenu
call :fastprint "Welcome to the TriTriSim Installer.|White" "Please select a category:|Gray" 
echo.
call :fastprint "[1] TFX|White" "----------------------------|White" "[S] Settings|White"
echo.
call :fastprint "[H] Return to hub|White"
echo.
setlocal enabledelayedexpansion
set /p choice="Enter your selection:  "
if /i "!choice!"=="H" (
call "TriTriSim Hub.bat"
) else (
call :page !choice!
)
exit /b 0

:Settings
call :fastprint "Settings|White"
echo.
call :getcommunitystate manualcommunity
if %state% EQU 0 (
    setlocal enabledelayedexpansion
    call :getcommunitystate communitypath
    call :fastprint "[C] Set community folder manually (current is !state!)|White"
    endlocal
    ) else (
    setlocal enabledelayedexpansion
    call :getcommunitystate communitypath
    call :fastprint "[C] Use auto community folder (!state! was manually selected.)|White"
    endlocal
    )


If %DEVMODE% EQU 1 (call :fastprint "[D] Disable devmode|Red") else (call :fastprint "[D] Enable devmode|Green")
echo.
call :fastprint "[Q] Back"
echo.
setlocal enabledelayedexpansion
call :getcommunitystate manualcommunity
set /p choice="Enter your selection:  "
if /i "!choice!"=="D" CALL :toggledevmode
if /i "!choice!"=="Q" CALL :page 0
if /i "!choice!"=="C" (

    if %state% EQU 0 (
        
    echo.

    set /p choice="Enter new community folder:  "
    call :setcommunitystate manualcommunity 1
    call :setcommunitystate communitypath "!choice!"

    ) else (
    call :setcommunitystate manualcommunity 0
    call :getCommunityPath
    call :setcommunitystate communitypath "!COMMUNITY_PATH!"
    )
)
endlocal
exit /b 0















::Planecheck




:planecheck
setlocal enabledelayedexpansion
set RPath="%COMMUNITY_PATH%\%~1"
set RPath3='"%COMMUNITY_PATH%\%~3"'
setlocal disabledelayedexpansion
IF EXIST %RPath% (
	powershell -Command ^
	"$file = %RPath3%;" ^
	"$marker = '<!-- TFX INSTALLED -->';" ^
	"if ((Get-Content $file) -notcontains $marker) {" ^
	" Write-Host '%~2' -ForegroundColor White " ^
	"} else {" ^
	"  $lines = Get-Content %~4;" ^
	"  $index = $lines.IndexOf('<!-- TFX END -->');" ^
	"  $marker = $lines[$index-1];" ^
 	"	if ((Get-Content $file) -notcontains $marker) {" ^
	"	 Write-Host '%~2' -ForegroundColor Yellow " ^
	"	} else {" ^
	"	 Write-Host '%~2' -ForegroundColor DarkGray " ^
	"	}" ^
	"}"
) ELSE (
    call :fastprint "%~2 .......................this plane is not installed|DarkGray"
)
setlocal enabledelayedexpansion 
EXIT /B 0


:uplanecheck
setlocal enabledelayedexpansion 
set RPath="%COMMUNITY_PATH%\%~1"
set RPath3='"%COMMUNITY_PATH%\%~3"'
setlocal disabledelayedexpansion 
IF EXIST %RPath% (
	powershell -Command ^
 	"$file = %RPath3%;" ^
 	"$marker = '<!-- TFX INSTALLED -->';" ^
 	"if ((Get-Content $file) -contains $marker) {" ^
	" Write-Host '%~2' -ForegroundColor White " ^
	"} else {" ^
	" Write-Host '%~2' -ForegroundColor DarkGray " ^
	"}"
) ELSE (
    call :fastprint "%~2 .......................this plane is not installed|DarkGray"
)
setlocal enabledelayedexpansion 
EXIT /B 0




::Install/uninstall TFX




:InstallTFX
setlocal enabledelayedexpansion 
set RPath3="%COMMUNITY_PATH%\%~1"
setlocal disabledelayedexpansion
call :quietunins "%~1" , "%~2" , "%~3"
setlocal disabledelayedexpansion
if defined "%~4" (

    powershell -Command ^
  "$file = '%RPath3%';" ^
  "$insert = Get-Content %~2;" ^
  "$marker = '<!-- TFX INSTALLED -->';" ^
  "  $lines = Get-Content $file;" ^
  "  $index = $lines.Count - %~4;" ^
  "  $newLines = $lines[0..($index-1)] + $insert + $lines[$index..($lines.Count-1)];" ^
  "  $newLines | Set-Content $file;" 

) else (

powershell -Command ^
  "$file = '%RPath3%';" ^
  "$insert = Get-Content %~2;" ^
  "$marker = '<!-- TFX INSTALLED -->';" ^
  "$lines = Get-Content $file;" ^
  "$match = $lines | Select-String '</Behaviors>';" ^
  "if ($match) {" ^
  "  $index = $match.LineNumber - 1;" ^
  "  $newLines = $lines[0..($index-1)] + $insert + $lines[$index..($lines.Count-1)];" ^
  "  $newLines | Set-Content $file" ^
  "} else {" ^
  "  Write-Host 'Critical error: </Behaviors> tag not found!' -ForegroundColor Red" ^
  "}"
  
)
setlocal enabledelayedexpansion 
EXIT /B 0



:quietunins
setlocal enabledelayedexpansion 
set RPath3="%COMMUNITY_PATH%\%~1"
setlocal disabledelayedexpansion
powershell -Command ^
  "$file = '%RPath3%';" ^
  "$lines = Get-Content $file;" ^
  "$start = $lines.IndexOf('<!-- TFX INSTALLED -->');" ^
  "$end = $lines.IndexOf('<!-- TFX END -->');" ^
  "if ($start -ge 0 -and $end -ge 0) {" ^
  "  $newLines = $lines[0..($start - 1)] + $lines[($end + 1)..($lines.Count - 1)];" ^
  "  $newLines | Set-Content $file;" ^
  "  Write-Host 'TFX update / reinstall for the %~3 completed sucessfully.' -ForegroundColor Green" ^
  "} else {" ^
  "  Write-Host 'TFX installation for the %~3 completed sucessfully.' -ForegroundColor Green" ^
  "}"
setlocal enabledelayedexpansion 
EXIT /B 0


:UninstallTFX
setlocal enabledelayedexpansion 
set RPath3="%COMMUNITY_PATH%\%~1"
setlocal disabledelayedexpansion
powershell -Command ^
  "$file = '%RPath3%';" ^
  "$lines = Get-Content $file;" ^
  "$start = $lines.IndexOf('<!-- TFX INSTALLED -->');" ^
  "$end = $lines.IndexOf('<!-- TFX END -->');" ^
  "if ($start -ge 0 -and $end -ge 0) {" ^
  "  $newLines = $lines[0..($start - 1)] + $lines[($end + 1)..($lines.Count - 1)];" ^
  "  $newLines | Set-Content $file;" ^
  "  Write-Host 'TFX uninstalled from the %~3.' -ForegroundColor Red" ^
  "} else {" ^
  "  Write-Host 'Uninstall skipped for the %~3 - TFX is not installed.' -ForegroundColor Yellow" ^
  "}"
setlocal enabledelayedexpansion 
EXIT /B 0


:updateLayout
MSFSLayoutGenerator.exe "%COMMUNITY_PATH%\%~1\layout.json"
exit /b 0




:: End of individual installs











:InstallAll
CALL :Install772
CALL :Install77F
CALL :Install320
CALL :Install320N
CALL :Install380
EXIT /B 0

:Install772
CALL :InstallTFX "pmdg-aircraft-77er\SimObjects\Airplanes\PMDG 777-200ER\attachments\pmdg\Function_Exterior_772\model\772_Exterior_Behavior.xml" , 'Installerinserts2024\772.txt' , "PMDG 777-200ER"
CALL :updateLayout "pmdg-aircraft-77er"
EXIT /B 0

:Install77F
CALL :InstallTFX "pmdg-aircraft-77f\SimObjects\Airplanes\PMDG 777F\attachments\pmdg\Function_Exterior_77F\model\77F_Exterior_Behavior.xml" , 'Installerinserts2024\77f.txt' , "PMDG 777F"
CALL :updateLayout "pmdg-aircraft-77f"
EXIT /B 0


:Install320
CALL :InstallTFX "fnx-aircraft-320\SimObjects\Airplanes\FNX_320_CFM\Model\FNX320_Exterior_CFM.xml" , 'Installerinserts2024\320CFM.txt' , "Fenix A320 (CFM)"
CALL :InstallTFX "fnx-aircraft-320\SimObjects\Airplanes\FNX_320_IAE\Model\FNX320_Exterior_IAE.xml" , 'Installerinserts2024\320IAE.txt' , "Fenix A320 (IAE)"
CALL :updateLayout "fnx-aircraft-320"
EXIT /B 0

:Install380
CALL :InstallTFX "flybywire-aircraft-a380-842\SimObjects\AirPlanes\FlyByWire_A380_842\model\A380_EXTERIOR.xml" , 'Installerinserts2024\380.txt' , "Flybywire A380"
CALL :updateLayout "flybywire-aircraft-a380-842"
EXIT /B 0

:Install320N
CALL :InstallTFX "flybywire-aircraft-a320-neo\SimObjects\AirPlanes\FlyByWire_A320_NEO\model\A320_NEO.xml" , 'Installerinserts2024\320N.txt' , "Flybywire A320 Neo"
CALL :updateLayout "flybywire-aircraft-a320-neo"
exit /b 0


:UninstallAllPrompt
cls
color 4
setlocal enabledelayedexpansion
set /p choice=Are you sure? (y/n): 
if /i "!choice!"=="y" CALL :UninstallAll
setlocal disabledelayedexpansion
EXIT /B 0



:UninstallAll
setlocal disabledelayedexpansion
CALL :Uninstall772
CALL :Uninstall77F
CALL :Uninstal320
CALL :Unistall320N
CALL :Uninstall380
setlocal enabledelayedexpansion
EXIT /B 0


:Uninstall772
CALL :UninstallTFX "pmdg-aircraft-77er\SimObjects\Airplanes\PMDG 777-200ER\attachments\pmdg\Function_Exterior_772\model\772_Exterior_Behavior.xml" , 'Installerinserts2024\772.txt' , "PMDG 777-200ER"
CALL :updateLayout "pmdg-aircraft-77er"
EXIT /B 0

:Uninstall77F
CALL :UninstallTFX "pmdg-aircraft-77f\SimObjects\Airplanes\PMDG 777F\attachments\pmdg\Function_Exterior_77F\model\77F_Exterior_Behavior.xml" , 'Installerinserts2024\77f.txt' , "PMDG 777F"
CALL :updateLayout "pmdg-aircraft-77f"
EXIT /B 0


:Uninstall320
CALL :UninstallTFX "fnx-aircraft-320\SimObjects\Airplanes\FNX_320_CFM\Model\FNX320_Exterior_CFM.xml" , 'Installerinserts2024\320CFM.txt' , "Fenix A320 (CFM)"
CALL :UninstallTFX "fnx-aircraft-320\SimObjects\Airplanes\FNX_320_IAE\Model\FNX320_Exterior_IAE.xml" , 'Installerinserts2024\320IAE.txt' , "Fenix A320 (IAE)"
CALL :updateLayout "fnx-aircraft-320"
EXIT /B 0

:Uninstall380
CALL :UninstallTFX "flybywire-aircraft-a380-842\SimObjects\AirPlanes\FlyByWire_A380_842\model\A380_EXTERIOR.xml" , 'Installerinserts2024\380.txt' , "Flybywire A380"
CALL :updateLayout "flybywire-aircraft-a380-842"
EXIT /B 0

:Uninstall320N
CALL :UninstallTFX "flybywire-aircraft-a320-neo\SimObjects\AirPlanes\FlyByWire_A320_NEO\model\A320_NEO.xml" , 'Installerinserts2024\320N.txt' , "Flybywire A320 Neo"
CALL :updateLayout "flybywire-aircraft-a320-neo"
exit /b 0


:Reinstall
call :InstallAll
EXIT /B 0




:getupdatedfiles
setlocal disabledelayedexpansion 
IF EXIST "Installerinserts2024" (
set BASEURL=https://raw.githubusercontent.com/TriTriTheCuber/TFX/main/2024/
set FILES=772.txt 320CFM.txt 320IAE.txt 320N.txt 380.txt 77f.txt
REM Local target folder (change if needed)
set TARGET=Installerinserts2024
del Installerinserts2024\*.txt
	REM Loop through each file and download it
	for %%F in (%FILES%) do (
    	REM Create local folder structure if needed
    	for %%D in ("%%F") do (
    	    set FILEPATH=%%~dp0
    	    if not "!FILEPATH!"=="" (
    	        mkdir "%TARGET%\!FILEPATH!" 2>nul
    	    )
    	)
    	REM Download the file
    	powershell -Command "Invoke-WebRequest -Uri '%BASEURL%/%%F' -OutFile '%TARGET%\%%F' -UseBasicParsing"
    		if errorlevel 1 (
		echo Failed to download %%F. Check your internet connection.
    		) else (
		echo %%F fetched successfully.
		)
	)

)
setlocal enabledelayedexpansion 
EXIT /B 0

:installdependencies
setlocal disabledelayedexpansion
md Installerinserts2024
echo Main folder created.
call :getupdatedfiles
echo Dependency installation done.
setlocal enabledelayedexpansion 

EXIT /b 0

:toggledevmode
call :getstate devmode
If %state% EQU 1 (call :setstate devmode 0) else (call :setstate devmode 1) 
exit /b 0


:getCommunityPath
call :getcommunitystate manualcommunity
echo %state%
if %state%==0 (

set "COMMUNITY_PATH="
powershell -ExecutionPolicy Bypass -File detect_community2024.ps1
:: Read result
set /p COMMUNITY_PATH=<_community_path.txt
:: Check result
if "%COMMUNITY_PATH%"=="NOT_FOUND" (
    echo UserCfg.opt not found at expected location.
    set "COMMUNITY_PATH=C:\MSFSFallback\Community"
) else if "%COMMUNITY_PATH%"=="NO_INSTALLED_PATH" (
    echo InstalledPackagesPath line not found.
    set "COMMUNITY_PATH=C:\MSFSFallback\Community"
) else (
    echo Community folder detected:
    echo %COMMUNITY_PATH%
)
del _community_path.txt >nul 2>&1

)
exit /b 0










:fetchzip
:: Args: %1 = ZIP URL, %2 = COMMUNITY_PATH

set "ZIPTEMP=%TEMP%\_tfx_dl.zip"
set "ZIPURL=%~1"
set "COMMUNITY=%~2"
set "TEMP_UNZIP=%TEMP\tfx_unzip"

:: Clean temp folder if it exists
rmdir /s /q "%TEMP_UNZIP%" >nul 2>&1
mkdir "%TEMP_UNZIP%"

echo.
echo Downloading zip...
powershell -ExecutionPolicy Bypass -File "zipdownloadmanager.ps1" "%ZIPURL%" "%ZIPTEMP%"
if not exist "%ZIPTEMP%" (
	call :fastprint "Download failed.|Red"
    exit /b 1
)

echo Extracting zip...
powershell -Command ^
  "Expand-Archive -LiteralPath '%ZIPTEMP%' -DestinationPath '%TEMP_UNZIP%' -Force"

:: Find the single root folder inside the zip
for /f "delims=" %%D in ('dir /b /ad "%TEMP_UNZIP%"') do set "ZIPROOT=%TEMP_UNZIP%\%%D" & goto moveFiles

:moveFiles
echo Merging contents from %ZIPROOT% to %COMMUNITY%
xcopy "%ZIPROOT%\*" "%COMMUNITY%\" /E /H /Y >nul

echo Cleaning up...
del "%ZIPTEMP%" >nul
rmdir /s /q "%TEMP_UNZIP%" >nul
call :fastprint "Download and extraction sucessful.|Green"
exit /b 0
















:installbasepackage
echo Attempting to install base package...
call :fetchzip "https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2024.zip" , "%COMMUNITY_PATH%"
exit /b 0

:installmaterialpackage
echo Attempting to install material package...
call :fetchzip "https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/materiallibs.zip" , "%COMMUNITY_PATH%"
exit /b 0

:uninstallbasepackageprompt
cls
color 4
setlocal enabledelayedexpansion
set /p choice=Are you sure? (y/n): 
if /i "!choice!"=="y" CALL :uninstallbasepackage
setlocal disabledelayedexpansion
EXIT /B 0


:uninstallbasepackage
@RD /S /Q "%COMMUNITY_PATH%/TFX-fxlib"
exit /b 0

:page
echo %~1 > temp\currentpage.tmp
exit /b 0



:getpage
set /p cpage=<temp\currentpage.tmp
exit /b 0







:buildstate
if not exist "state2024/state.txt" (
    (
        echo devmode=0
        echo version=1
    ) > state2024\state.txt
)
exit /b 0

:buildcommunitystate
if not exist "state2024/community.txt" (
    (
        echo communitypath=%COMMUNITY_PATH%
        echo manualcommunity=0
    ) > state2024\community.txt
)
call :getcommunitystate manualcommunity

if %state%==1 (
    call :getcommunitystate communitypath
    set "COMMUNITY_PATH=%state%"
) else (
    call :setcommunitystate communitypath "%COMMUNITY_PATH%"
)
exit /b 0







:setstate
:: Usage: call :setstate key value
:: Writes or updates `key=value` in state\state.txt

setlocal enabledelayedexpansion
set "KEY=%~1"
set "VALUE=%~2"

set "STATEFILE=state2024\state.txt"
set "TMPFILE=temp\state2024_tmp.txt"

if not exist "%STATEFILE%" (
    echo %KEY%=%VALUE%>"%STATEFILE%"
    exit /b
)
> "%TMPFILE%" (
    set "found=0"
    for /f "usebackq tokens=1,* delims==" %%A in ("%STATEFILE%") do (
        set "line=%%A=%%B"
        if /i "%%A"=="%KEY%" (
            echo %KEY%=%VALUE%
            set "found=1"
        ) else (
            echo !line!
        )
    )
    if "!found!"=="0" echo %KEY%=%VALUE%
)

move /y "%TMPFILE%" "%STATEFILE%" >nul
endlocal
exit /b 0







:setcommunitystate
:: Usage: call :secommunitystate key value
:: Writes or updates `key=value` in state\community.txt

setlocal enabledelayedexpansion
set "KEY=%~1"
set "VALUE=%~2"

set "STATEFILE=state2024\community.txt"
set "TMPFILE=temp\community2024_tmp.txt"

if not exist "%STATEFILE%" (
    echo %KEY%=%VALUE%>"%STATEFILE%"
    exit /b
)
> "%TMPFILE%" (
    set "found=0"
    for /f "usebackq tokens=1,* delims==" %%A in ("%STATEFILE%") do (
        set "line=%%A=%%B"
        if /i "%%A"=="%KEY%" (
            echo %KEY%=%VALUE%
            set "found=1"
        ) else (
            echo !line!
        )
    )
    if "!found!"=="0" echo %KEY%=%VALUE%
)
move /y "%TMPFILE%" "%STATEFILE%" >nul
endlocal
exit /b 0







:getstate
:: Usage: call :getstate key → sets variable "state"
setlocal enabledelayedexpansion
set "state="
for /f "usebackq tokens=1,* delims==" %%A in ("state2024\state.txt") do (
    if /i "%%A"=="%~1" set "state=%%B"
)
endlocal & set "state=%state%"
exit /b 0


:getcommunitystate
:: Usage: call :getstate key → sets variable "state"
setlocal enabledelayedexpansion
set "state="
for /f "usebackq tokens=1,* delims==" %%A in ("state2024\community.txt") do (
    if /i "%%A"=="%~1" set "state=%%B"
)
endlocal & set "state=%state%"
exit /b 0

:prebuildcs
if not exist "state2024/community.txt" (
    (
        echo communitypath=%COMMUNITY_PATH%
        echo manualcommunity=0
    ) > state2024\community.txt
)
exit /b 0


:prebuildcs
if not exist "state2024/community.txt" (
    (
        echo communitypath=%COMMUNITY_PATH%
        echo manualcommunity=0
    ) > state2024\community.txt
)
exit /b 0






:title
echo.
echo        ================================================
echo                     TriTriSim Installer v1.1            
echo             Developed by TriTriTheCuber / TriTriSim     
echo                            2024 ver
echo        ================================================
echo.
