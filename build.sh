#!/bin/bash
# Build script for creating standalone binaries

set -e

echo "🚀 Building Bluetooth Scanner binaries..."

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install -r requirements-dev.txt

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Build Windows executable
echo "🏗️  Building Windows executable..."
python -m PyInstaller --onefile \
    --name "bluetooth-scanner-windows" \
    --icon=icon.ico \
    --add-data "README.md:." \
    --hidden-import=bleak \
    --hidden-import=bleak.backends \
    --hidden-import=bleak.backends.winrt \
    --hidden-import=bleak.backends.winrt.scanner \
    --hidden-import=bleak.backends.winrt.client \
    --hidden-import=bleak.backends.winrt.util \
    --hidden-import=reportlab \
    --hidden-import=reportlab.lib \
    --hidden-import=reportlab.platypus \
    --hidden-import=reportlab.lib.pagesizes \
    --hidden-import=asyncio \
    --hidden-import=winrt \
    --hidden-import=winrt.windows \
    --hidden-import=winrt.windows.foundation \
    --hidden-import=winrt.windows.foundation.collections \
    --hidden-import=winrt.windows.devices \
    --hidden-import=winrt.windows.devices.bluetooth \
    --hidden-import=winrt.windows.devices.bluetooth.advertisement \
    --hidden-import=winrt.windows.devices.bluetooth.genericattributeprofile \
    --hidden-import=winrt.windows.devices.enumeration \
    --hidden-import=winrt.windows.storage \
    --hidden-import=winrt.windows.storage.streams \
    --collect-all=bleak \
    --collect-all=winrt \
    --console \
    bluetooth_scanner.py

# For Linux/macOS
echo "🏗️  Building Linux executable..."
python -m PyInstaller --onefile \
    --name "bluetooth-scanner-linux" \
    --add-data "README.md:." \
    --hidden-import=bleak \
    --hidden-import=bleak.backends \
    --hidden-import=bleak.backends.bluezdbus \
    --hidden-import=reportlab \
    --hidden-import=reportlab.lib \
    --hidden-import=reportlab.platypus \
    --hidden-import=reportlab.lib.pagesizes \
    --hidden-import=asyncio \
    --collect-all=bleak \
    --console \
    bluetooth_scanner.py

echo "✅ Build completed!"
echo "📁 Binaries are in the 'dist/' directory"
echo ""
echo "Windows: dist/bluetooth-scanner-windows.exe"
echo "Linux:   dist/bluetooth-scanner-linux"
