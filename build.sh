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
    --hidden-import=reportlab \
    --hidden-import=asyncio \
    --console \
    bluetooth_scanner.py

# For Linux/macOS
echo "🏗️  Building Linux executable..."
python -m PyInstaller --onefile \
    --name "bluetooth-scanner-linux" \
    --add-data "README.md:." \
    --hidden-import=bleak \
    --hidden-import=reportlab \
    --hidden-import=asyncio \
    --console \
    bluetooth_scanner.py

echo "✅ Build completed!"
echo "📁 Binaries are in the 'dist/' directory"
echo ""
echo "Windows: dist/bluetooth-scanner-windows.exe"
echo "Linux:   dist/bluetooth-scanner-linux"
