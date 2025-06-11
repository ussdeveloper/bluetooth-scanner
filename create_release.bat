@echo off
echo 🚀 Creating GitHub Release v2.1.0...
echo.

REM Check if the executable exists
if not exist "dist\bluetooth-scanner-windows.exe" (
    echo ❌ Error: bluetooth-scanner-windows.exe not found in dist folder
    echo Please run build.bat first
    pause
    exit /b 1
)

echo ✅ Found executable: dist\bluetooth-scanner-windows.exe
echo 📏 Size: 14.1 MB
echo.

echo 📝 Release Information:
echo Tag: v2.1.0
echo Title: Bluetooth Scanner v2.1.0 - Enhanced PDF Reports
echo Binary: bluetooth-scanner-windows.exe
echo.

echo 🔧 To complete the release, please:
echo 1. Go to: https://github.com/ussdeveloper/bluetooth-scanner/releases
echo 2. Click "Create a new release"
echo 3. Select tag: v2.1.0
echo 4. Title: Bluetooth Scanner v2.1.0 - Enhanced PDF Reports
echo 5. Upload the binary: dist\bluetooth-scanner-windows.exe
echo.

echo 📋 Release Description Template:
echo.
echo ## 🚀 Major Release: Professional Landscape PDF Reports
echo.
echo ### ✨ Key Features
echo - 📄 **Landscape PDF Reports** - Professional A4 landscape format
echo - 📊 **Comprehensive Statistics** - Signal strength, manufacturer, device analysis  
echo - 🎯 **Fixed Table Pagination** - Table starts on first page
echo - 📶 **Visual Signal Indicators** - Emoji-based signal strength
echo - 📋 **Enhanced 12-Column Table** - Complete device information
echo.
echo ### 🔧 Technical Improvements
echo - ✅ Fully functional Windows executable with all dependencies
echo - ✅ Enhanced PDF layout and professional typography
echo - ✅ Comprehensive statistical analysis with percentages
echo - ✅ Optimized space utilization and improved readability
echo.
echo ### 📦 Downloads
echo - **Windows**: bluetooth-scanner-windows.exe (14.1 MB)
echo - **Source**: Available via Git clone or ZIP download
echo.
echo Perfect for network analysis, security auditing, and IoT device discovery.
echo.

echo 📂 Opening Windows Explorer to show the executable...
explorer "dist"

echo.
echo 🌐 Opening GitHub releases page...
start "" "https://github.com/ussdeveloper/bluetooth-scanner/releases/new?tag=v2.1.0"

echo.
echo ✅ Ready to create release!
echo Upload the file: dist\bluetooth-scanner-windows.exe
pause
