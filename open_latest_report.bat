@echo off
echo Otwieranie najnowszego raportu Bluetooth PDF...
echo.

:: Znajdz najnowszy plik PDF z raportem
for /f "delims=" %%i in ('dir /b /o-d bluetooth_scan_report_*.pdf 2^>nul') do (
    set "newest=%%i"
    goto :found
)

echo Nie znaleziono zadnych raportow PDF w tym folderze.
echo Uruchom najpierw skaner: python bluetooth_scanner.py
pause
exit /b 1

:found
echo Najnowszy raport: %newest%
echo Otwieranie w domyslnej przegladarce PDF...
start "" "%newest%"

if errorlevel 1 (
    echo.
    echo Nie mozna otworzyc pliku PDF.
    echo Otwieranie folderu z plikiem...
    explorer .
)

echo.
echo Raport zostal otwarty!
pause
