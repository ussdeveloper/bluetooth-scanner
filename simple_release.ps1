# Simple GitHub Release Creation Script
Write-Host "Creating GitHub Release v2.1.0..." -ForegroundColor Green
Write-Host ""

# Check if executable exists
$executablePath = "dist\bluetooth-scanner-windows.exe"
if (-Not (Test-Path $executablePath)) {
    Write-Host "Error: $executablePath not found" -ForegroundColor Red
    Write-Host "Please run build.bat first" -ForegroundColor Yellow
    exit 1
}

$fileInfo = Get-Item $executablePath
$sizeInMB = [math]::Round($fileInfo.Length / 1MB, 1)

Write-Host "Found executable: $executablePath" -ForegroundColor Green
Write-Host "Size: $sizeInMB MB" -ForegroundColor Cyan
Write-Host ""

Write-Host "Release Information:" -ForegroundColor Yellow
Write-Host "Tag: v2.1.0"
Write-Host "Title: Bluetooth Scanner v2.1.0 - Enhanced PDF Reports"
Write-Host "Binary: bluetooth-scanner-windows.exe ($sizeInMB MB)"
Write-Host ""

Write-Host "Opening GitHub releases page..." -ForegroundColor Cyan
Start-Process "https://github.com/ussdeveloper/bluetooth-scanner/releases/new?tag=v2.1.0&title=Bluetooth%20Scanner%20v2.1.0%20-%20Enhanced%20PDF%20Reports"

Write-Host "Opening file explorer to show executable..." -ForegroundColor Cyan
Start-Process "explorer" -ArgumentList "/select,$((Resolve-Path $executablePath).Path)"

Write-Host ""
Write-Host "Release Description (copy and paste):" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Gray

$releaseDescription = @"
## Major Release: Professional Landscape PDF Reports

### Key Features
* **Landscape PDF Reports** - Professional A4 landscape format for optimal data presentation
* **Comprehensive Statistics** - Signal strength distribution, manufacturer breakdown, device type analysis
* **Fixed Table Pagination** - Table now starts on first page instead of second page
* **Visual Signal Indicators** - Emoji-based signal strength visualization
* **Enhanced 12-Column Table** - Complete device information with additional data fields

### Technical Improvements
* Fully functional Windows executable with all dependencies resolved
* Enhanced PDF layout and professional typography
* Comprehensive statistical analysis with percentages
* Optimized space utilization and improved readability

### Downloads
* **Windows**: ``bluetooth-scanner-windows.exe`` ($sizeInMB MB) - Standalone executable, no Python required
* **Source**: Available via Git clone or ZIP download

### Usage
1. Download ``bluetooth-scanner-windows.exe``
2. Run directly - no installation needed
3. Professional PDF reports generated automatically in current directory

Perfect for network analysis, security auditing, and IoT device discovery.

### What's New in v2.1.0
* Professional landscape-oriented PDF reports
* Comprehensive statistical analysis with percentages
* Enhanced 12-column data table with additional fields
* Visual signal strength indicators with emojis
* Fixed table pagination issue
* Optimized layout and professional styling

**Full Changelog**: [CHANGELOG.md](https://github.com/ussdeveloper/bluetooth-scanner/blob/main/CHANGELOG.md)
"@

Write-Host $releaseDescription -ForegroundColor Gray
Write-Host "=================================" -ForegroundColor Gray
Write-Host ""

Write-Host "Manual Steps:" -ForegroundColor Yellow
Write-Host "1. Fill in the release title and description (copied above)"
Write-Host "2. Upload the file: $executablePath"
Write-Host "3. Set as latest release"
Write-Host "4. Publish release"
Write-Host ""

Write-Host "Release ready to publish!" -ForegroundColor Green
