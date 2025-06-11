# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-06-12

### Added
- **Enhanced PDF Reports with Landscape Orientation** - Professional landscape-oriented reports for better data presentation
- **Comprehensive Statistical Analysis** - Detailed statistics including signal strength distribution, manufacturer breakdown, and device type analysis
- **Advanced Device Recognition** - Improved manufacturer and device type detection with more comprehensive databases
- **Enhanced Table Format** - 12-column table with additional data fields including manufacturer data size and service data size
- **Visual Signal Strength Indicators** - Emoji-based signal strength visualization (📶📶📶 Strong, 📶📶 Medium, etc.)
- **Compact Summary Layout** - Optimized summary to prevent table pagination issues
- **Percentage-based Analytics** - Signal strength and manufacturer distribution shown as percentages
- **RSSI Range Analysis** - Average, minimum, and maximum RSSI values with detailed breakdown
- **Service Analysis** - Enhanced Bluetooth service discovery and categorization
- **Professional Footer** - Technical information including scan methodology and system details

### Enhanced
- **PDF Report Quality** - Improved layout, typography, and data presentation
- **Table Styling** - Enhanced colors, fonts, and cell formatting for better readability
- **Statistical Accuracy** - More precise calculations and data analysis
- **Data Density** - More information packed efficiently into reports
- **Cross-platform Compatibility** - Improved Windows binary with all dependencies resolved

### Fixed
- **Table Pagination Issue** - Table now starts on first page instead of second page
- **WinRT Dependencies** - Resolved all Windows Runtime dependency issues in executable builds
- **Layout Optimization** - Better space utilization preventing unnecessary page breaks
- **Data Formatting** - Improved text truncation and field sizing for landscape format

### Technical Improvements
- **Build Process** - Enhanced PyInstaller configuration with comprehensive hidden imports
- **Code Quality** - Improved error handling and data validation
- **Performance** - Optimized scanning and report generation processes
- **Documentation** - Updated README with new features and enhanced examples

## [2.0.0] - 2025-06-11

### Added
- **Professional BLE Scanner** - Complete rewrite with professional-grade Bluetooth Low Energy scanning
- **PDF Report Generation** - Automated PDF reports with comprehensive device data
- **English Interface** - Full English language support throughout the application
- **Device Type Detection** - Automatic classification of smartphones, headphones, smartwatches, etc.
- **Manufacturer Recognition** - Extensive database of Bluetooth manufacturer IDs
- **Signal Strength Analysis** - RSSI-based signal strength categorization
- **Service Discovery** - Bluetooth service UUID recognition and naming
- **Cross-platform Binaries** - Windows and Linux standalone executables
- **Comprehensive Testing** - Full pytest-based test suite with mocking
- **CI/CD Ready** - Automated build and test scripts

### Technical Features
- **Modern Python Stack** - Python 3.8+ with asyncio-based scanning
- **Robust Dependencies** - bleak for Bluetooth, reportlab for PDF generation
- **Professional Structure** - Proper project organization with requirements, tests, docs
- **Git Integration** - Full version control with GitHub repository
- **Documentation** - Complete README, CONTRIBUTING, and LICENSE files
- **Helper Scripts** - Automated install, build, test, and run scripts

### Infrastructure
- **PyInstaller Builds** - Optimized executable generation with dependency bundling
- **GitHub Repository** - https://github.com/ussdeveloper/bluetooth-scanner
- **MIT License** - Open source licensing for broad compatibility
- **Multi-platform Support** - Windows, Linux, and macOS compatibility

## [1.0.0] - Initial Version

### Initial Features
- Basic Bluetooth device scanning
- Console output in multiple languages
- Simple device listing functionality

---

## Release Notes

### Version 2.1.0 Release Notes

This major update introduces professional-grade PDF reporting with landscape orientation and comprehensive statistical analysis. The enhanced reports provide detailed insights into discovered Bluetooth devices with visual indicators, percentage-based analytics, and professional formatting.

Key highlights:
- **Landscape PDF Reports** - Better utilization of page space for comprehensive data tables
- **Enhanced Statistics** - Signal strength distribution, manufacturer breakdown, and device type analysis
- **Visual Improvements** - Professional styling with emoji indicators and improved typography
- **Fixed Pagination** - Table now properly fits on the first page
- **Windows Compatibility** - Resolved all dependency issues for standalone executables

The application is now ready for professional use in network analysis, security auditing, and IoT device discovery scenarios.

### Upgrade Instructions

**From Source:**
```bash
git pull origin main
pip install -r requirements.txt
python bluetooth_scanner.py
```

**Binary Users:**
Download the latest `bluetooth-scanner-windows.exe` from the [releases page](https://github.com/ussdeveloper/bluetooth-scanner/releases).

### Breaking Changes
- PDF report format has been enhanced (previous reports remain compatible)
- Some internal API changes for developers extending the codebase

### Migration Guide
No migration steps required for end users. All existing functionality is preserved with enhancements.
