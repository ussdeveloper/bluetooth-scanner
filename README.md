# Bluetooth Scanner v2.1.1

Professional Bluetooth Low Energy (BLE) scanner that discovers nearby devices and generates comprehensive PDF reports with detailed statistics and analysis.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Pytest-orange.svg)](tests/)
[![Version](https://img.shields.io/badge/Version-2.1.1-brightgreen.svg)](https://github.com/ussdeveloper/bluetooth-scanner/releases)

## Features

- 🔍 **Professional BLE Scanning** - Comprehensive Bluetooth Low Energy device discovery
- 📱 **Advanced Device Recognition** - Automatic manufacturer and device type detection with detailed analysis
- 📄 **Enhanced PDF Reports** - Professional landscape-oriented reports with comprehensive statistics
- 📊 **Detailed Statistics** - Signal strength analysis, manufacturer distribution, device type breakdown
- 🚀 **Cross-Platform Binaries** - Standalone Windows and Linux executables (no Python required)
- 🧪 **Fully Tested** - Comprehensive test suite with automated testing
- 🌍 **English Interface** - Complete English language support with professional output
- � **Rich Analytics** - RSSI distribution, service analysis, and comprehensive device metrics

## Enhanced PDF Report Features

- **Landscape Layout** - Optimized for better data presentation
- **Comprehensive Statistics** - Device count, manufacturer distribution, signal strength analysis
- **RSSI Analysis** - Signal strength categorization with percentages
- **Manufacturer Breakdown** - Top manufacturers with device counts and percentages
- **Device Type Analysis** - Classification of discovered devices
- **Service Information** - Detailed Bluetooth service discovery and analysis
- **Technical Details** - Scan metadata, timestamps, and system information

## Requirements

- Python 3.8 or newer
- Windows or Linux with Bluetooth support
- Bluetooth adapter enabled in system

## Quick Start

### Option 1: Use Pre-built Binaries (Recommended)

Download the latest release from [GitHub Releases](https://github.com/ussdeveloper/bluetooth-scanner/releases):

- **Windows**: `bluetooth-scanner-windows.exe`
- **Linux**: `bluetooth-scanner-linux`

Run directly without Python installation required.

### Option 2: Install from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ussdeveloper/bluetooth-scanner.git
   cd bluetooth-scanner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scanner:**
   ```bash
   python bluetooth_scanner.py
   ```

### Windows Quick Setup

Use the provided batch files:
```bash
# Install dependencies
install.bat

# Run scanner
run_scanner.bat

# Open latest PDF report
open_latest_report.bat
```

## Usage

### Command Line
```bash
python bluetooth_scanner.py
```

### Available Options
- Scan duration: Default 10 seconds (configurable in code)
- Automatic PDF report generation
- Real-time device discovery output

## Development

### Setting up Development Environment

1. **Clone and setup:**
   ```bash
   git clone https://github.com/ussdeveloper/bluetooth-scanner.git
   cd bluetooth-scanner
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

### Running Tests

```bash
# Windows
test.bat

# Linux/macOS
./test.sh

# Or manually
pytest tests/ -v --cov=bluetooth_scanner
```

### Building Binaries

```bash
# Windows
build.bat

# Linux/macOS
./build.sh
```

### Code Quality

```bash
# Format code
black bluetooth_scanner.py tests/

# Lint code
flake8 bluetooth_scanner.py tests/ --max-line-length=100

# Type checking
mypy bluetooth_scanner.py --ignore-missing-imports
```

## Features

- 🔍 **Device Scanning** - finds all Bluetooth Low Energy (BLE) devices nearby
- 📱 **Device Information** - device name, MAC address, signal strength (RSSI)
- 🏭 **Manufacturer Identification** - automatic company recognition from device data
- 🔗 **Type Detection** - attempts to determine device type (phone, headphones, sensor, etc.)
- 📋 **Detailed Services** - displays available Bluetooth services
- 📄 **PDF Reports** - automatic generation of professional PDF reports with scan results
- 📊 **Statistics** - result summary with signal strength and manufacturer statistics

## PDF Reports

The application automatically generates professional PDF reports after each scan:

- 📊 **Condensed Table Format** - all device data in a single comprehensive table
- 🔍 **Complete Information** - device name, MAC address, RSSI, signal strength, manufacturer, company ID, service count, device type, and main services
- 📈 **Optimized Layout** - compact table design fitting all data on A4 format
- 📱 **Easy to Read** - color-coded headers and alternating row backgrounds

### Report Contents:
The condensed table includes these columns:
1. **#** - Device number
2. **Device Name** - Identified device name
3. **MAC Address** - Bluetooth hardware address
4. **RSSI (dBm)** - Signal strength value
5. **Signal Strength** - Human-readable signal level (Strong/Medium/Weak)
6. **Manufacturer** - Identified company name
7. **Company ID** - Bluetooth company identifier
8. **Services Count** - Number of available Bluetooth services
9. **Device Type** - Detected device category
10. **Main Services** - Key Bluetooth services offered

### Opening Reports:
```powershell
# Open latest report
.\open_latest_report.bat

# Or manually
start bluetooth_scan_report_YYYYMMDD_HHMMSS.pdf
```

## Example Output

```
🔵 Bluetooth Low Energy (BLE) Scanner
📅 Date: 2025-06-11 23:55:21
==================================================
🔍 Starting Bluetooth device scan...
⏱️  Scan duration: 10 seconds
==================================================
📡 Scanning for Bluetooth Low Energy (BLE) devices...
✅ Found 11 Bluetooth devices:
======================================================================
 1. 📱 iPhone/iPad
    📍 MAC Address: 80:2B:F9:D0:D8:E2
    📶 Signal Strength (RSSI): -59 dBm
    🔋 Signal Power: Medium 📶📶
    🏭 Manufacturer data: 1 entries
       • Apple, Inc.
    🔗 Type: 📱 Mobile Phone
--------------------------------------------------
 2. 📱 Google Device
    📍 MAC Address: 40:68:FC:89:BE:6A
    📶 Signal Strength (RSSI): -46 dBm
    🔋 Signal Power: Strong 📶📶📶
    🏭 Manufacturer data: 1 entries
       • Google
    🔗 Type: 🔵 Bluetooth Low Energy Device
--------------------------------------------------
```

## Troubleshooting

### Error: "Cannot access Bluetooth adapter"
- Check if Bluetooth is enabled in Windows settings
- Make sure Bluetooth drivers are installed
- Run the program as administrator

### Library installation error
- Install Microsoft Visual C++ Build Tools
- Use pre-compiled version: `pip install bleak reportlab`

### No devices found
- Make sure other devices have Bluetooth enabled
- Check if devices are in discoverable mode
- Reduce distance to scanned devices

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Run tests and ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Project Structure

```
bluetooth-scanner/
├── bluetooth_scanner.py    # Main scanner module
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Development dependencies
├── tests/                  # Test files
├── build.bat/build.sh     # Build scripts
├── test.bat/test.sh       # Test runners
├── setup.py               # Package setup
├── LICENSE                # MIT License
└── README.md              # This file
```

## Troubleshooting

### Common Issues

**Error: "Cannot access Bluetooth adapter"**
- Check if Bluetooth is enabled in system settings
- Ensure Bluetooth drivers are installed
- Try running as administrator (Windows)

**Library installation error**
- Install Microsoft Visual C++ Build Tools (Windows)
- Use: `pip install --upgrade pip setuptools wheel`

**No devices found**
- Ensure other devices have Bluetooth enabled and discoverable
- Reduce distance to target devices
- Check for interference from other devices

### Platform-Specific Notes

**Windows:**
- Requires Windows 10 version 1903 or later
- May need Visual C++ redistributable packages

**Linux:**
- May require `bluez` and `bluez-tools` packages
- User might need to be in `bluetooth` group

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Bleak](https://github.com/hbldh/bleak) - Bluetooth Low Energy platform Agnostic Klient
- [ReportLab](https://www.reportlab.com/) - PDF generation toolkit
- Community contributors and testers

---

**Made with ❤️ by [USS Developer](https://github.com/ussdeveloper)**
