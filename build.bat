@echo off
REM Build script for Windows

echo 🚀 Building Bluetooth Scanner for Windows...

REM Install build dependencies
echo 📦 Installing build dependencies...
pip install -r requirements-dev.txt

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

REM Build Windows executable
echo 🏗️  Building Windows executable...
python -m PyInstaller --onefile ^
    --name "bluetooth-scanner-windows" ^
    --add-data "README.md;." ^
    --hidden-import=bleak ^
    --hidden-import=bleak.backends ^
    --hidden-import=bleak.backends.winrt ^
    --hidden-import=bleak.backends.winrt.scanner ^
    --hidden-import=bleak.backends.winrt.client ^
    --hidden-import=bleak.backends.winrt.util ^
    --hidden-import=reportlab ^
    --hidden-import=reportlab.lib ^
    --hidden-import=reportlab.platypus ^
    --hidden-import=reportlab.lib.pagesizes ^
    --hidden-import=asyncio ^
    --hidden-import=winrt ^
    --hidden-import=winrt.windows ^
    --hidden-import=winrt.windows.foundation ^
    --hidden-import=winrt.windows.foundation.collections ^
    --hidden-import=winrt.windows.devices ^
    --hidden-import=winrt.windows.devices.bluetooth ^
    --hidden-import=winrt.windows.devices.bluetooth.advertisement ^
    --hidden-import=winrt.windows.devices.bluetooth.genericattributeprofile ^
    --hidden-import=winrt.windows.devices.enumeration ^
    --hidden-import=winrt.windows.storage ^
    --hidden-import=winrt.windows.storage.streams ^
    --collect-all=bleak ^
    --collect-all=winrt ^
    --console ^
    bluetooth_scanner.py

echo ✅ Build completed!
echo 📁 Binary is in the 'dist/' directory
echo.
echo Windows: dist\bluetooth-scanner-windows.exe

pause
