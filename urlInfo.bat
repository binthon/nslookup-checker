@echo off
setlocal enabledelayedexpansion

if "%~1"=="" goto :error
set address=%1

echo Tracert dla %address% na dzien %date% %time% >> tracert_results.txt
for /f "delims=" %%a in ('tracert %address%') do (
    echo %%a >> tracert_results.txt
    echo %%a
    echo %%a | find "Request timed out" > nul
    if not errorlevel 1 goto :end
)

:end
echo Zakonczono tracert dla %address%
exit /b

:error
echo Nie podano adresu URL.
exit /b
