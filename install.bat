@echo off
echo ================================
echo    Instalacja Skanera Bluetooth
echo ================================
echo.

echo Sprawdzanie Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo BLAD: Python nie jest zainstalowany lub nie znajduje sie w PATH
    echo Zainstaluj Python z https://python.org
    pause
    exit /b 1
)

echo Python znaleziony!
echo.

echo Instalowanie wymaganych bibliotek...
pip install pybluez

if errorlevel 1 (
    echo.
    echo UWAGA: Instalacja pybluez nie powiodla sie.
    echo Probuje alternatywna metode...
    pip install pybluez-win10
    
    if errorlevel 1 (
        echo.
        echo BLAD: Nie mozna zainstalowac pybluez
        echo.
        echo Rozwiazania:
        echo 1. Zainstaluj Microsoft Visual C++ Build Tools
        echo 2. Uruchom jako administrator
        echo 3. Uzyj: pip install --user pybluez
        pause
        exit /b 1
    )
)

echo.
echo ================================
echo     Instalacja zakonczona!
echo ================================
echo.
echo Uruchom skaner komenda:
echo python bluetooth_scanner.py
echo.
pause
