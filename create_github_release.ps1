# GitHub Release Creation Script for Bluetooth Scanner v2.1.0
# This script creates a GitHub release using the REST API

param(
    [string]$GitHubToken = $env:GITHUB_TOKEN,
    [string]$Owner = "ussdeveloper", 
    [string]$Repo = "bluetooth-scanner",
    [string]$Tag = "v2.1.0",
    [string]$ReleaseName = "Bluetooth Scanner v2.1.0 - Enhanced PDF Reports",
    [string]$ExecutablePath = "dist\bluetooth-scanner-windows.exe"
)

Write-Host "🚀 Creating GitHub Release v2.1.0..." -ForegroundColor Green
Write-Host ""

# Check if executable exists
if (-Not (Test-Path $ExecutablePath)) {
    Write-Host "❌ Error: $ExecutablePath not found" -ForegroundColor Red
    Write-Host "Please run build.bat first" -ForegroundColor Yellow
    exit 1
}

$fileInfo = Get-Item $ExecutablePath
Write-Host "✅ Found executable: $ExecutablePath" -ForegroundColor Green
Write-Host "📏 Size: $([math]::Round($fileInfo.Length / 1MB, 1)) MB" -ForegroundColor Cyan

# Release body content
$releaseBody = @"
## Major Release: Professional Landscape PDF Reports

### Key Features
* Landscape PDF Reports - Professional A4 landscape format for optimal data presentation
* Comprehensive Statistics - Signal strength distribution, manufacturer breakdown, device type analysis
* Fixed Table Pagination - Table now starts on first page instead of second page
* Visual Signal Indicators - Emoji-based signal strength visualization
* Enhanced 12-Column Table - Complete device information with additional data fields

### Technical Improvements
* Fully functional Windows executable with all dependencies resolved
* Enhanced PDF layout and professional typography
* Comprehensive statistical analysis with percentages
* Optimized space utilization and improved readability

### Downloads
* Windows: bluetooth-scanner-windows.exe ($([math]::Round($fileInfo.Length / 1MB, 1)) MB) - Standalone executable, no Python required
* Source: Available via Git clone or ZIP download

### Usage
1. Download bluetooth-scanner-windows.exe
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

Full Changelog: https://github.com/$Owner/$Repo/blob/main/CHANGELOG.md
"@

if ([string]::IsNullOrEmpty($GitHubToken)) {
    Write-Host "⚠️  GitHub token not found in environment variable GITHUB_TOKEN" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔧 Manual Release Instructions:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://github.com/$Owner/$Repo/releases/new" -ForegroundColor White
    Write-Host "2. Tag: $Tag" -ForegroundColor White
    Write-Host "3. Title: $ReleaseName" -ForegroundColor White
    Write-Host "4. Upload: $ExecutablePath" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Release Description (copy this):" -ForegroundColor Cyan
    Write-Host $releaseBody -ForegroundColor Gray
    
    # Open browser to GitHub releases page
    Start-Process "https://github.com/$Owner/$Repo/releases/new?tag=$Tag"
    
    # Open file explorer to show the executable
    Start-Process "explorer" -ArgumentList "/select,`"$(Resolve-Path $ExecutablePath)`""
    
} else {
    Write-Host "🔑 Using GitHub token for automated release creation..." -ForegroundColor Green
    
    try {
        # Create release using GitHub API
        $headers = @{
            "Authorization" = "token $GitHubToken"
            "Accept" = "application/vnd.github.v3+json"
            "Content-Type" = "application/json"
        }
        
        $releaseData = @{
            "tag_name" = $Tag
            "name" = $ReleaseName
            "body" = $releaseBody
            "draft" = $false
            "prerelease" = $false
        } | ConvertTo-Json
        
        Write-Host "📤 Creating release..." -ForegroundColor Yellow
        $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/releases" -Method POST -Headers $headers -Body $releaseData
        
        Write-Host "✅ Release created successfully!" -ForegroundColor Green
        Write-Host "📎 Release URL: $($release.html_url)" -ForegroundColor Cyan
        
        # Upload asset
        Write-Host "📤 Uploading executable..." -ForegroundColor Yellow
        $uploadUrl = $release.upload_url -replace '\{\?name,label\}', "?name=bluetooth-scanner-windows.exe"
        
        $uploadHeaders = @{
            "Authorization" = "token $GitHubToken"
            "Content-Type" = "application/octet-stream"
        }
        
        $fileBytes = [System.IO.File]::ReadAllBytes((Resolve-Path $ExecutablePath))
        $uploadResponse = Invoke-RestMethod -Uri $uploadUrl -Method POST -Headers $uploadHeaders -Body $fileBytes
        
        Write-Host "✅ Executable uploaded successfully!" -ForegroundColor Green
        Write-Host "🎉 Release v2.1.0 is now live!" -ForegroundColor Green
        Write-Host "🌐 View release: $($release.html_url)" -ForegroundColor Cyan
        
        # Open the release page
        Start-Process $release.html_url
        
    } catch {
        Write-Host "❌ Error creating release: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "💡 Try the manual process instead" -ForegroundColor Yellow
        Start-Process "https://github.com/$Owner/$Repo/releases/new?tag=$Tag"
    }
}

Write-Host ""
Write-Host "🎉 Bluetooth Scanner v2.1.0 release process completed!" -ForegroundColor Green
