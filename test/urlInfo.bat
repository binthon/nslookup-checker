@echo off
setlocal enabledelayedexpansion

set domains_file=domains.txt
if not exist %domains_file% goto :error

for /f "tokens=*" %%a in (%domains_file%) do (
    set domain=%%a
    echo Tracert dla !domain! na dzien %date% %time% >> tracert_results.txt
    tracert !domain! >> tracert_results.txt
)

goto :end

:error
echo Nie znaleziono pliku z domenami.
exit /b

:end
echo Zakonczono przetwarzanie domen.
exit /b