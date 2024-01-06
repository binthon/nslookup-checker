@echo off
setlocal enabledelayedexpansion

set domains_file=domains.txt
set results_file=tracert_results.txt
set last_processed_file=last_processed.txt

if not exist %domains_file% goto error

:: Odczytaj ostatnio przetworzony adres
set last_processed=
if exist %last_processed_file% (
    set /p last_processed=<%last_processed_file%
    if "!last_processed!"=="" (
        echo Plik %last_processed_file% jest pusty.
        goto end
    )
) else (
    echo Plik %last_processed_file% nie istnieje.
    goto end
)

set found_last_processed=0
set start_processing=0
for /f "tokens=*" %%a in (%domains_file%) do (
    set "current_domain=%%a"
    
    if !start_processing! equ 1 (
        echo Tracert dla !current_domain! na dzien %date% %time% >> %results_file%
        set fail_count=0
        for /f "delims=" %%l in ('tracert !current_domain! 2^>^&1') do (
            set line=%%l
            echo !line! | findstr /C:"Request timed out" >nul
            if !errorlevel! equ 0 (
                set /a fail_count+=1
            ) else (
                set fail_count=0
            )
            echo !line! >> %results_file%
            if !fail_count! geq 3 (
                goto skip_domain_outside
            )
        )

        echo !current_domain! > %last_processed_file%
    )

    if "!current_domain!"=="!last_processed!" set start_processing=1
)

:skip_domain_outside

if !found_last_processed! equ 0 (
    echo Ostatnio przetworzona domena nie została znaleziona.
) else if !start_processing! equ 0 (
    echo Ostatnio przetworzona domena jest ostatnią w liście.
)

:end
echo Zakonczono przetwarzanie domen.
exit /b
