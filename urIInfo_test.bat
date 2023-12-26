@echo off
setlocal enabledelayedexpansion

set domains_file=domains.txt
set results_file=tracert_results.txt

if not exist %domains_file% goto :error

for /f "tokens=*" %%a in (%domains_file%) do (
    set domain=%%a
    echo Tracert dla !domain! na dzien %date% %time% >> %results_file%

    set fail_count=0
    for /f "delims=" %%l in ('tracert !domain! 2^>^&1') do (
        set line=%%l

        rem Sprawdzenie, czy linia zawiera tylko gwiazdki
        echo !line! | findstr /C:"* * *" > nul
        if !errorlevel! equ 0 (
            set /a fail_count+=1
        ) else (
            set fail_count=0
        )

        rem Zapisanie linii do pliku wynikowego
        echo !line! >> %results_file%

        rem Przerwanie pętli po trzech nieudanych próbach
        if !fail_count! geq 3 goto :next_domain
    )

    :next_domain
)

goto :end

:error
echo Nie znaleziono pliku z domenami.
exit /b

:end
echo Zakonczono przetwarzanie domen.
exit /b