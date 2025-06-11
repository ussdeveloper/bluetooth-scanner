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
pyinstaller --onefile ^
    --name "bluetooth-scanner-windows" ^
    --add-data "README.md;." ^
    --hidden-import=bleak ^
    --hidden-import=reportlab ^
    --hidden-import=asyncio ^
    --console ^
    bluetooth_scanner.py

echo ✅ Build completed!
echo 📁 Binary is in the 'dist/' directory
echo.
echo Windows: dist\bluetooth-scanner-windows.exe

pause
