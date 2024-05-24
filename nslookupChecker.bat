@echo off
setlocal

if "%~1"=="" (
    exit /b 1
)

set DOMAIN=%~1

for %%T in (A AAAA MX TXT NS CNAME) do (
    nslookup -type=%%T %DOMAIN%
    echo.
)

endlocal
