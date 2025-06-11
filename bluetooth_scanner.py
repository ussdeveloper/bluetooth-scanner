#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bluetooth Scanner - Professional BLE Device Discovery & PDF Reporting
Version: 2.1.1
Author: USS Developer
Repository: https://github.com/ussdeveloper/bluetooth-scanner

Professional Bluetooth Low Energy (BLE) scanner that discovers nearby devices 
and generates comprehensive PDF reports with detailed statistics and analysis.
Uses bleak library for cross-platform Bluetooth Low Energy device scanning.
"""

__version__ = "2.1.1"
__author__ = "USS Developer"
__license__ = "MIT"

import asyncio
from bleak import BleakScanner, BleakClient
import sys
import time
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

async def scan_bluetooth_devices(duration=10):
    """
    Scans for nearby Bluetooth devices
    
    Args:
        duration (int): Scanning duration in seconds
    
    Returns:
        dict: Dictionary with devices {address: (device, advertisement_data)}
    """
    print(f"🔍 Starting Bluetooth device scan...")
    print(f"⏱️  Scan duration: {duration} seconds")
    print("=" * 50)
    
    try:
        # Scan for Bluetooth Low Energy devices
        print("📡 Scanning for Bluetooth Low Energy (BLE) devices...")
        ble_devices = await BleakScanner.discover(timeout=duration, return_adv=True)
        
        # Additional scan with longer time for some devices
        if len(ble_devices) < 5:
            print("🔄 Additional scanning (extended time)...")
            additional_devices = await BleakScanner.discover(timeout=duration//2, return_adv=True)
            # Merge results
            for addr, data in additional_devices.items():
                if addr not in ble_devices:
                    ble_devices[addr] = data
        
        return ble_devices
        
    except Exception as e:
        print(f"❌ Error during scanning: {e}")
        return {}

def display_devices(devices):
    """
    Displays list of found Bluetooth devices
    
    Args:
        devices (dict): Dictionary with devices {address: (device, advertisement_data)}
    """
    if not devices:
        print("🚫 No Bluetooth devices found nearby.")
        print("\n💡 Make sure that:")
        print("   - Bluetooth is enabled on this computer")
        print("   - Other devices have Bluetooth enabled and are discoverable")
        print("   - You are within range of other Bluetooth devices")
        print("   - Devices support Bluetooth Low Energy (BLE)")
        return
    print(f"✅ Found {len(devices)} Bluetooth devices:")
    print("=" * 70)
    
    for i, (address, (device, adv_data)) in enumerate(devices.items(), 1):        # Get device name from various sources
        device_name = get_device_name(device, adv_data)
        
        print(f"{i:2d}. 📱 {device_name}")
        print(f"    📍 MAC Address: {device.address}")
        print(f"    📶 Signal Strength (RSSI): {adv_data.rssi if hasattr(adv_data, 'rssi') and adv_data.rssi else device.rssi} dBm")
        print(f"    🔋 Signal Power: {get_signal_strength_description(adv_data.rssi if hasattr(adv_data, 'rssi') and adv_data.rssi else device.rssi)}")
        
        # Additional information from advertisement data
        if adv_data.manufacturer_data:
            print(f"    🏭 Manufacturer data: {len(adv_data.manufacturer_data)} entries")
            # Show manufacturer details
            for company_id, data in list(adv_data.manufacturer_data.items())[:2]:
                company_name = get_company_name(company_id)
                print(f"       • {company_name}")
        
        if adv_data.service_data:
            print(f"    🔧 Service data: {len(adv_data.service_data)} services")
        
        if adv_data.service_uuids:
            print(f"    🆔 Service UUIDs: {len(adv_data.service_uuids)} services")
            for uuid in adv_data.service_uuids[:3]:  # Show first 3
                service_name = get_service_name(uuid)
                print(f"       • {service_name}")
            if len(adv_data.service_uuids) > 3:
                print(f"       • ... and {len(adv_data.service_uuids) - 3} more")
        
        print(f"    🔗 Type: {get_device_type(device_name, adv_data)}")
        print("-" * 50)

def get_signal_strength_description(rssi):
    """
    Converts RSSI value to signal strength description
    
    Args:
        rssi (int): RSSI value in dBm
    
    Returns:
        str: Signal strength description
    """
    if rssi >= -30:
        return "Very Strong 📶📶📶📶"
    elif rssi >= -50:
        return "Strong 📶📶📶"
    elif rssi >= -70:
        return "Medium 📶📶"
    elif rssi >= -90:
        return "Weak 📶"
    else:
        return "Very Weak 📵"

def get_service_name(uuid):
    """
    Maps service UUID to readable name
    
    Args:
        uuid (str): Service UUID
    
    Returns:
        str: Service name
    """
    # Standard Bluetooth service UUIDs
    service_names = {
        "0000180f-0000-1000-8000-00805f9b34fb": "Battery Service",
        "0000180a-0000-1000-8000-00805f9b34fb": "Device Information",
        "0000181c-0000-1000-8000-00805f9b34fb": "User Data",
        "0000180d-0000-1000-8000-00805f9b34fb": "Heart Rate",
        "0000181a-0000-1000-8000-00805f9b34fb": "Environmental Sensing",
        "0000180f-0000-1000-8000-00805f9b34fb": "Battery Service",
        "0000110a-0000-1000-8000-00805f9b34fb": "Audio Source",
        "0000110b-0000-1000-8000-00805f9b34fb": "Audio Sink",
        "0000111e-0000-1000-8000-00805f9b34fb": "Hands-Free",
        "6e400001-b5a3-f393-e0a9-e50e24dcca9e": "Nordic UART Service"
    }
    
    # Try to find full UUID
    full_uuid = str(uuid).lower()
    if full_uuid in service_names:
        return service_names[full_uuid]
    
    # Try short UUID (first 4 characters)
    short_uuid = full_uuid[:8]
    for full, name in service_names.items():
        if full.startswith(short_uuid):
            return name
    
    return "Unknown service"

def get_device_type(name, adv_data):
    """
    Próbuje określić typ urządzenia na podstawie nazwy i danych reklamowych
    
    Args:
        name (str): Nazwa urządzenia
        adv_data: Dane reklamowe urządzenia
    
    Returns:
        str: Domniemany typ urządzenia
    """
    name_lower = name.lower() if name else ""
    
    # Analiza nazwy urządzenia
    if any(keyword in name_lower for keyword in ['airpods', 'headphones', 'earbuds', 'speaker', 'audio']):        return "🎧 Audio Device"
    elif any(keyword in name_lower for keyword in ['iphone', 'samsung', 'phone', 'mobile']):
        return "📱 Mobile Phone"
    elif any(keyword in name_lower for keyword in ['watch', 'band', 'fitness']):
        return "⌚ Wearable Device"
    elif any(keyword in name_lower for keyword in ['mouse', 'keyboard', 'trackpad']):
        return "🖱️ Input Device"
    elif any(keyword in name_lower for keyword in ['tv', 'display', 'monitor']):
        return "📺 Display Device"
    elif any(keyword in name_lower for keyword in ['sensor', 'thermometer', 'humidity']):
        return "🌡️ Sensor"
    elif any(keyword in name_lower for keyword in ['light', 'bulb', 'lamp']):
        return "💡 Smart Light"
      # Analyze service UUIDs
    if adv_data.service_uuids:
        service_types = []
        for uuid in adv_data.service_uuids:
            service_name = get_service_name(uuid)
            service_types.append(service_name.lower())
        
        if any('heart rate' in s for s in service_types):
            return "❤️ Heart Rate Monitor"
        elif any('battery' in s for s in service_types):
            return "🔋 Battery Device"
        elif any('audio' in s for s in service_types):
            return "🎵 Audio Device"
    
    return "🔵 Bluetooth Low Energy Device"

async def get_detailed_info(address):
    """
    Attempts to connect to device and get detailed information
    
    Args:
        address (str): Device MAC address
    
    Returns:
        dict: Detailed device information
    """
    try:
        async with BleakClient(address) as client:
            if await client.is_connected():
                services = await client.get_services()
                return {
                    'connected': True,
                    'services': [str(s.uuid) for s in services],
                    'characteristics': sum(len(s.characteristics) for s in services)
                }
    except Exception as e:
        return {'connected': False, 'error': str(e)}
    
    return {'connected': False}

def get_device_name(device, adv_data):
    """
    Pobiera nazwę urządzenia z różnych źródeł
    
    Args:
        device: Obiekt BLEDevice
        adv_data: Dane reklamowe urządzenia
    
    Returns:
        str: Nazwa urządzenia lub opis na podstawie adresu MAC
    """
    # 1. Spróbuj pobrać nazwę z obiektu device
    if device.name and device.name.strip():
        return device.name.strip()
    
    # 2. Spróbuj pobrać nazwę z danych reklamowych
    if adv_data.local_name and adv_data.local_name.strip():
        return adv_data.local_name.strip()
    
    # 3. Spróbuj określić producenta na podstawie adresu MAC
    manufacturer = get_manufacturer_from_mac(device.address)
    if manufacturer:
        return f"{manufacturer} Device"
    
    # 4. Spróbuj określić typ na podstawie danych producenta
    device_type = get_device_type_from_manufacturer_data(adv_data)
    if device_type:
        return device_type
    
    # 5. Ostatnia opcja - nieznana nazwa z częścią adresu MAC
    mac_suffix = device.address.split(':')[-2:]
    return f"BLE Device ({':'.join(mac_suffix)})"

def get_manufacturer_from_mac(mac_address):
    """
    Określa producenta na podstawie OUI (Organizationally Unique Identifier) w adresie MAC
    
    Args:
        mac_address (str): Adres MAC urządzenia
    
    Returns:
        str: Nazwa producenta lub None
    """
    # Pobierz pierwsze 3 bajty adresu MAC (OUI)
    oui = mac_address.upper().replace(':', '').replace('-', '')[:6]
    
    # Słownik popularnych OUI i producentów
    oui_manufacturers = {
        '000000': 'Xerox',
        '0001C8': 'Hewlett Packard',
        '000C29': 'VMware',
        '001B63': 'Apple',
        '00A040': 'Apple',
        '28E02C': 'Apple',
        '2C5490': 'Apple',
        '3CAB8E': 'Apple',
        '4025C2': 'Apple',
        '509EA7': 'Apple',
        '68AB1E': 'Apple',
        '6C2483': 'Apple',
        '7CFA4E': 'Apple',
        '84F3EB': 'Apple',
        '8C2937': 'Apple',
        '90B21F': 'Apple',
        'A4C361': 'Apple',
        'B8E856': 'Apple',
        'C82A14': 'Apple',
        'D023DB': 'Apple',
        'E4C63D': 'Apple',
        'E8802E': 'Apple',
        'EC8892': 'Apple',
        'F01C13': 'Apple',
        'F40E22': 'Apple',
        '0050F2': 'Microsoft',
        '00155D': 'Microsoft',
        '001DD8': 'Microsoft',
        '0017FA': 'Microsoft',
        '7C1E52': 'Microsoft',
        '000272': 'Intel',
        '001B77': 'Intel',
        '0050F2': 'Intel',
        '24F5AA': 'Intel',
        '34E6AD': 'Intel',
        '7085C2': 'Intel',
        '001377': 'Samsung',
        '002454': 'Samsung',
        '00374A': 'Samsung',
        '003EE1': 'Samsung',
        '74DA38': 'Samsung',
        '8C77121': 'Samsung',
        'C869CD': 'Samsung',
        'E84E06': 'Samsung',
        'F09FC2': 'Samsung',
        '000F86': 'Huawei',
        '001E10': 'Huawei',
        '003048': 'Huawei',
        '00664C': 'Huawei',
        '001CF0': 'LG Electronics',
        '001E75': 'LG Electronics',
        '002140': 'LG Electronics',
        '0021D1': 'LG Electronics',
        '00E04C': 'Realtek',
        '52540E': 'Realtek',
        '9CEB2E': 'Realtek',
        'B0359E': 'Realtek'
    }
    
    return oui_manufacturers.get(oui)

def get_company_name(company_id):
    """
    Maps Company ID to company name
    
    Args:
        company_id (int): Company ID from manufacturer data
    
    Returns:
        str: Company name
    """
    company_names = {
        0: 'Ericsson Technology Licensing',
        1: 'Nokia Mobile Phones',
        2: 'Intel Corp.',
        3: 'IBM Corp.',
        4: 'Toshiba Corp.',
        5: '3Com',
        6: 'Microsoft',
        7: 'Lucent',
        8: 'Motorola',
        9: 'Infineon Technologies AG',
        10: 'Qualcomm Technologies International, Ltd.',
        15: 'Broadcom Corporation',
        29: 'Texas Instruments Inc.',
        48: 'Hewlett-Packard Company',
        57: 'AVM Berlin',
        69: 'Aruba Networks',
        76: 'Apple, Inc.',
        89: 'BlackBerry Limited',
        117: 'Samsung Electronics Co. Ltd.',
        224: 'Google',
        343: 'Xiaomi Inc.',
        2050: 'Amazon.com Services, Inc.'
    }
    
    return company_names.get(company_id, f"Unknown company (ID: {company_id})")

def get_device_type_from_manufacturer_data(adv_data):
    """
    Tries to determine device type based on manufacturer data
    
    Args:
        adv_data: Device advertisement data
    
    Returns:
        str: Device type or None
    """
    if not adv_data.manufacturer_data:
        return None
    
    # Check company ID from manufacturer data
    for company_id, data in adv_data.manufacturer_data.items():
        # Apple
        if company_id == 76:  # 0x004C - Apple
            if len(data) >= 2:
                apple_type = data[0]
                if apple_type == 0x02:
                    return "iPhone/iPad"
                elif apple_type == 0x07:
                    return "AirPods"
                elif apple_type == 0x0A:
                    return "Apple Watch"
                elif apple_type == 0x0F:
                    return "Mac/MacBook"
                elif apple_type == 0x10:
                    return "Apple TV"
                else:
                    return "Apple Device"
        
        # Microsoft
        elif company_id == 6:  # 0x0006 - Microsoft
            return "Microsoft Device"
        
        # Samsung
        elif company_id == 117:  # 0x0075 - Samsung
            return "Samsung Device"
        
        # Google
        elif company_id == 224:  # 0x00E0 - Google
            return "Google Device"
        
        # Xiaomi
        elif company_id == 343:  # 0x0157 - Xiaomi
            return "Xiaomi Device"
    
    return None

async def main():
    """
    Main program function
    """
    print("🔵 Bluetooth Low Energy (BLE) Scanner")
    print(f"🏷️  Version: {__version__}")
    scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"📅 Date: {scan_time}")
    print("=" * 50)
    
    try:
        # Scan for devices
        scan_duration = 10
        devices = await scan_bluetooth_devices(duration=scan_duration)
        
        # Display results
        display_devices(devices)
        
        # Optional: detailed information for selected devices
        if devices and len(devices) <= 3:
            print("\n🔍 Attempting to get detailed information...")
            for address, (device, adv_data) in list(devices.items())[:3]:
                print(f"\n🔗 Connecting to {device.name or address}...")
                details = await get_detailed_info(address)
                if details.get('connected'):
                    print(f"   ✅ Connected! Services: {len(details['services'])}, Characteristics: {details['characteristics']}")
                else:
                    print(f"   ❌ Cannot connect: {details.get('error', 'No response')}")
        
        # Generate PDF report
        if devices:
            print("\n📄 Generating PDF report...")
            try:
                pdf_path = generate_pdf_report(devices, scan_time, scan_duration)
                print(f"✅ PDF report generated: {os.path.basename(pdf_path)}")
                print(f"📁 Location: {pdf_path}")
            except Exception as e:
                print(f"❌ Error generating PDF report: {e}")
        else:
            print("\n📄 No devices found to generate PDF report")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Scanning interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print(f"💡 Make sure Bluetooth is enabled on the system")
    
    print("\n👋 Thank you for using the Bluetooth scanner!")

def generate_pdf_report(devices, scan_time, duration):
    """
    Generates a comprehensive PDF report with enhanced layout and detailed statistics
    
    Args:
        devices (dict): Dictionary with devices {address: (device, advertisement_data)}
        scan_time (str): Scan start time
        duration (int): Scan duration in seconds
    
    Returns:
        str: Path to generated PDF file
    """
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    
    # Filename with date and time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"bluetooth_scan_report_{timestamp}.pdf"
    filepath = os.path.join(os.getcwd(), filename)
    
    # Create PDF document with landscape orientation for better table layout
    doc = SimpleDocTemplate(filepath, pagesize=landscape(A4), 
                          leftMargin=0.5*inch, rightMargin=0.5*inch,
                          topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Enhanced custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    summary_style = ParagraphStyle(
        'SummaryStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=10,
        alignment=TA_LEFT,
        leftIndent=10
    )
      # Title
    story.append(Paragraph("🔵 Professional Bluetooth Low Energy (BLE) Device Scan Report", title_style))
    story.append(Spacer(1, 8))
    
    # Enhanced scan summary with comprehensive statistics
    device_count = len(devices)
    manufacturers = {}
    signal_strengths = {'Strong': 0, 'Medium': 0, 'Weak': 0, 'Very Weak': 0}
    device_types = {}
    total_services = 0
    rssi_values = []
    
    # Calculate detailed statistics
    for address, (device, adv_data) in devices.items():
        # Count manufacturers
        if adv_data.manufacturer_data:
            for company_id in adv_data.manufacturer_data.keys():
                company_name = get_company_name(company_id)
                if "Unknown company" in company_name:
                    company_name = f"Unknown (ID: {company_id})"
                manufacturers[company_name] = manufacturers.get(company_name, 0) + 1
        
        # Count signal strengths and collect RSSI values
        rssi = adv_data.rssi if hasattr(adv_data, 'rssi') and adv_data.rssi else device.rssi
        if rssi:
            rssi_values.append(rssi)
            if rssi >= -50:
                signal_strengths['Strong'] += 1
            elif rssi >= -70:
                signal_strengths['Medium'] += 1
            elif rssi >= -90:
                signal_strengths['Weak'] += 1
            else:
                signal_strengths['Very Weak'] += 1
        
        # Count device types
        device_name = get_device_name(device, adv_data)
        device_type = get_device_type(device_name, adv_data)
        device_types[device_type] = device_types.get(device_type, 0) + 1
        
        # Count services
        if adv_data.service_uuids:
            total_services += len(adv_data.service_uuids)
    
    # Calculate RSSI statistics
    avg_rssi = sum(rssi_values) / len(rssi_values) if rssi_values else 0
    min_rssi = min(rssi_values) if rssi_values else 0
    max_rssi = max(rssi_values) if rssi_values else 0
      # Create comprehensive but compact summary
    scan_info_text = f"""
    <b>📅 Scan Information:</b> {scan_time} • Duration: {duration}s • BLE Protocol • Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/><br/>
    
    <b>📊 Discovery Results:</b> <b>{device_count}</b> devices found • <b>{total_services}</b> services • <b>{len(manufacturers)}</b> manufacturers • Avg: <b>{total_services/device_count:.1f}</b> services/device<br/><br/>
    
    <b>📶 Signal Distribution:</b> Strong: <b>{signal_strengths['Strong']}</b> ({signal_strengths['Strong']/device_count*100:.0f}%) • Medium: <b>{signal_strengths['Medium']}</b> ({signal_strengths['Medium']/device_count*100:.0f}%) • Weak: <b>{signal_strengths['Weak']}</b> ({signal_strengths['Weak']/device_count*100:.0f}%) • Very Weak: <b>{signal_strengths['Very Weak']}</b> ({signal_strengths['Very Weak']/device_count*100:.0f}%) • RSSI: {avg_rssi:.1f} dBm avg<br/><br/>
    
    <b>🏭 Top Manufacturers:</b> """
    
    # Add top manufacturers in compact format
    if manufacturers:
        top_manufacturers = sorted(manufacturers.items(), key=lambda x: x[1], reverse=True)[:3]
        manufacturer_list = []
        for manufacturer, count in top_manufacturers:
            percentage = count/device_count*100
            manufacturer_list.append(f"{manufacturer} ({count}, {percentage:.0f}%)")
        scan_info_text += " • ".join(manufacturer_list)
    else:
        scan_info_text += "No manufacturer data available"
    
    # Add device types in compact format
    if device_types:
        scan_info_text += "<br/><b>🔧 Device Types:</b> "
        top_types = sorted(device_types.items(), key=lambda x: x[1], reverse=True)[:3]
        type_list = []
        for device_type, count in top_types:
            percentage = count/device_count*100
            type_list.append(f"{device_type} ({count}, {percentage:.0f}%)")
        scan_info_text += " • ".join(type_list)
    
    story.append(Paragraph(scan_info_text, summary_style))
    story.append(Spacer(1, 10))
      # Enhanced comprehensive device table optimized for landscape
    if not devices:
        story.append(Paragraph("No Bluetooth devices found during the scan.", styles['Normal']))
    else:
        # Enhanced table headers with more detailed information
        headers = [
            '#', 'Device Name', 'MAC Address', 'RSSI\n(dBm)', 'Signal\nStrength', 
            'Manufacturer', 'Company\nID', 'Services\nCount', 'Device Type', 
            'Primary Services', 'Manufacturer\nData Size', 'Service\nData Size'
        ]
        
        table_data = [headers]
        
        for i, (address, (device, adv_data)) in enumerate(devices.items(), 1):
            device_name = get_device_name(device, adv_data)
            rssi = adv_data.rssi if hasattr(adv_data, 'rssi') and adv_data.rssi else device.rssi
            rssi_str = str(rssi) if rssi else "N/A"
            
            # Enhanced signal strength description with visual indicators
            if rssi:
                if rssi >= -50:
                    signal_desc = "📶📶📶 Strong"
                elif rssi >= -70:
                    signal_desc = "📶📶 Medium"
                elif rssi >= -90:
                    signal_desc = "📶 Weak"
                else:
                    signal_desc = "📵 Very Weak"
            else:
                signal_desc = "❓ N/A"
            
            # Enhanced manufacturer information
            main_manufacturer = "Unknown"
            company_id_str = "N/A"
            manufacturer_data_size = 0
            
            if adv_data.manufacturer_data:
                first_company_id = list(adv_data.manufacturer_data.keys())[0]
                company_id_str = str(first_company_id)
                main_manufacturer = get_company_name(first_company_id)
                if "Unknown company" in main_manufacturer:
                    main_manufacturer = f"Unknown (ID:{first_company_id})"
                
                # Calculate total manufacturer data size
                manufacturer_data_size = sum(len(data) for data in adv_data.manufacturer_data.values())
            
            # Enhanced services information
            services_count = len(adv_data.service_uuids) if adv_data.service_uuids else 0
            
            # Enhanced device type detection
            device_type = get_device_type(device_name, adv_data)
            if len(device_type) > 18:
                device_type = device_type[:15] + "..."
            
            # Enhanced services list with more details
            primary_services = "None"
            if adv_data.service_uuids:
                service_names = []
                for uuid in adv_data.service_uuids[:3]:  # Show top 3 services
                    service_name = get_service_name(uuid)
                    if "Unknown service" not in service_name:
                        short_name = service_name.split('(')[0].strip()
                        if len(short_name) > 15:
                            short_name = short_name[:12] + "..."
                        service_names.append(short_name)
                    else:
                        # Show shortened UUID for unknown services
                        short_uuid = str(uuid)[:8]
                        service_names.append(f"{short_uuid}...")
                
                if service_names:
                    primary_services = ", ".join(service_names)
                    if len(adv_data.service_uuids) > 3:
                        primary_services += f" (+{len(adv_data.service_uuids)-3})"
            
            # Service data size
            service_data_size = 0
            if adv_data.service_data:
                service_data_size = sum(len(data) for data in adv_data.service_data.values())
            
            # Optimize text length for landscape table
            device_name_short = device_name[:20] + "..." if len(device_name) > 20 else device_name
            main_manufacturer_short = main_manufacturer[:15] + "..." if len(main_manufacturer) > 15 else main_manufacturer
            primary_services_short = primary_services[:30] + "..." if len(primary_services) > 30 else primary_services
            
            row = [
                str(i),
                device_name_short,
                device.address,
                rssi_str,
                signal_desc,
                main_manufacturer_short,
                company_id_str,
                str(services_count),
                device_type,
                primary_services_short,
                f"{manufacturer_data_size} bytes" if manufacturer_data_size > 0 else "0",
                f"{service_data_size} bytes" if service_data_size > 0 else "0"
            ]
            
            table_data.append(row)
          # Enhanced table with optimized column widths for landscape A4
        col_widths = [0.3*inch, 1.5*inch, 1.2*inch, 0.6*inch, 0.8*inch, 
                     1.0*inch, 0.5*inch, 0.5*inch, 1.0*inch, 1.8*inch, 0.7*inch, 0.7*inch]
        
        main_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        main_table.setStyle(TableStyle([
            # Enhanced header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            
            # Enhanced data styling with better readability
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightblue]),
            
            # Enhanced borders and padding
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            
            # Special formatting for signal strength column
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),  # RSSI column
            ('ALIGN', (6, 0), (6, -1), 'CENTER'),  # Company ID column
            ('ALIGN', (7, 0), (7, -1), 'CENTER'),  # Services count column
        ]))
        
        story.append(main_table)
    
    # Enhanced footer with technical information
    story.append(Spacer(1, 20))
    story.append(Paragraph("=" * 120, styles['Normal']))
    
    footer_text = f"""
    <b>🔧 Technical Report Information:</b><br/>
    • Report generated by: Bluetooth Scanner v2.1 Professional Edition<br/>
    • Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    • System Platform: Windows • Bluetooth Library: bleak (Python)<br/>
    • Report Format: PDF Landscape • Page Size: A4<br/>
    • Scan Method: Bluetooth Low Energy (BLE) Advertisement Discovery<br/>
    • Data Sources: Device advertisements, manufacturer data, service UUIDs, signal strength
    """
    
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build document
    doc.build(story)    
    return filepath

if __name__ == "__main__":
    # Run the main asynchronous function
    asyncio.run(main())
