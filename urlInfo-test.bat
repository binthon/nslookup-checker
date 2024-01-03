@echo off
setlocal enabledelayedexpansion

set domains_file=domains.txt
set results_file=tracert_results.txt

if not exist %domains_file% goto error

set /a idx=0
for /f "delims=" %%a in (%domains_file%) do (
    set /a idx+=1
    set domains_array[!idx!]=%%a
)


set /a count=1
:next_domain
if !count! gtr !idx! goto end

set domain=!domains_array[%count%]!
echo Tracert dla !domain! na dzien %date% %time% >> %results_file%

set fail_count=0
for /f "delims=" %%l in ('tracert /4 !domain! 2^>^&1') do (
    set line=%%l

    echo !line! | findstr /C:"Request timed out" >nul
    if !errorlevel! equ 0 (
        set /a fail_count+=1
    ) else (
        set fail_count=0
    )

    echo !line! >> %results_file%
    if !fail_count! geq 3 (
        goto skip_domain
    )
)

:skip_domain
set /a count+=1
goto next_domain

:error
echo Nie znaleziono pliku z domenami.
exit /b

:end
echo Zakonczono przetwarzanie domen.
exit /b
