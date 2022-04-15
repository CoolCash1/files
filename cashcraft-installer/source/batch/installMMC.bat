@echo off

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:-------------------------------------- 
    mkdir "%userprofile%\CashCraft Launcher\MultiMC"
    cd "%userprofile%\CashCraft Launcher\MultiMC"
    echo Downloading Files...
    curl -L "https://github.com/CoolCash1/CashCraft/raw/main/MultiMC.zip" --output "multimc-latest.zip"
    curl -L "https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.msi" --output "jdk-16.0.2%2B7/OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.msi"
    echo Extracting Files...
    tar -xf "multimc-latest.zip"
    echo Please install jdk16
    "jdk-16.0.2%2B7/OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.msi"
    echo Finishing...
    ren "jdk-16.0.2+7" "jdk"
    echo Cleaning Up...
    del "multimc-latest.zip"
    del "jdk.zip"

    set "javaexe=%cd%\jdk\bin\javaw.exe"
    echo %javaexe%

    (echo JavaPath=%javaexe% && echo Language=en && echo LastHostname=DESKTOP-ECHRKKE && echo MaxMemAlloc=2048 && echo MinMemAlloc=512) > MultiMC\multimc.cfg

    pause
