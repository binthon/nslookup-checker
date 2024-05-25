@echo off
setlocal

if "%~1"=="" (
    echo Please provide an IP address or domain name.
    exit /b 1
)

set INPUT=%~1

echo Input parameter: %INPUT%
set "VALID_IP=1"

for /f "tokens=1-4 delims=." %%a in ("%INPUT%") do (
    if %%a LSS 0 set "VALID_IP=0"
    if %%a GTR 255 set "VALID_IP=0"
    if %%b LSS 0 set "VALID_IP=0"
    if %%b GTR 255 set "VALID_IP=0"
    if %%c LSS 0 set "VALID_IP=0"
    if %%c GTR 255 set "VALID_IP=0"
    if %%d LSS 0 set "VALID_IP=0"
    if %%d GTR 255 set "VALID_IP=0"
)

if %VALID_IP%==1 (
    echo Looking up details for IP address %INPUT%
    nslookup -debug %INPUT%
) else (
    for %%T in (A AAAA MX TXT NS CNAME) do (
        echo Looking up %%T records for %INPUT%
        nslookup -type=%%T %INPUT%
        echo.
    )
)

endlocal
