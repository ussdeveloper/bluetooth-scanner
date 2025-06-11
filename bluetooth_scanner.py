#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bluetooth Scanner - scans and displays list of all nearby Bluetooth devices
Uses bleak library for Bluetooth Low Energy (BLE) device scanning
"""

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
    Generates PDF report with Bluetooth scan results in a condensed table format
    
    Args:
        devices (dict): Dictionary with devices {address: (device, advertisement_data)}
        scan_time (str): Scan start time
        duration (int): Scan duration in seconds
    
    Returns:
        str: Path to generated PDF file
    """
    # Filename with date and time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"bluetooth_scan_report_{timestamp}.pdf"
    filepath = os.path.join(os.getcwd(), filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.blue
    )
    
    # Title
    story.append(Paragraph("🔵 Bluetooth Device Scan Report", title_style))
    story.append(Spacer(1, 15))
    
    # Scan information paragraph
    scan_info_text = f"""
    <b>Scan Date & Time:</b> {scan_time}<br/>
    <b>Scan Duration:</b> {duration} seconds<br/>
    <b>Devices Found:</b> {len(devices)}<br/>
    <b>Scan Type:</b> Bluetooth Low Energy (BLE)
    """
    story.append(Paragraph(scan_info_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Main condensed table with ALL data
    if not devices:
        story.append(Paragraph("No Bluetooth devices found.", styles['Normal']))
    else:
        # Table headers
        headers = [
            '#', 'Device Name', 'MAC Address', 'RSSI\n(dBm)', 'Signal\nStrength', 
            'Manufacturer', 'Company\nID', 'Services\nCount', 'Device Type', 'Main Services'
        ]
        
        table_data = [headers]
        
        for i, (address, (device, adv_data)) in enumerate(devices.items(), 1):
            device_name = get_device_name(device, adv_data)
            rssi = adv_data.rssi if hasattr(adv_data, 'rssi') and adv_data.rssi else device.rssi
            rssi_str = str(rssi) if rssi else "N/A"
            
            # Signal strength description (short)
            if rssi:
                if rssi >= -50:
                    signal_desc = "Strong"
                elif rssi >= -70:
                    signal_desc = "Medium"
                elif rssi >= -90:
                    signal_desc = "Weak"
                else:
                    signal_desc = "Very Weak"
            else:
                signal_desc = "N/A"
            
            # Main manufacturer and company ID
            main_manufacturer = "Unknown"
            company_id_str = "N/A"
            if adv_data.manufacturer_data:
                first_company_id = list(adv_data.manufacturer_data.keys())[0]
                company_id_str = str(first_company_id)
                main_manufacturer = get_company_name(first_company_id)
                if "Unknown company" in main_manufacturer:
                    main_manufacturer = f"ID:{first_company_id}"
            
            # Services count
            services_count = len(adv_data.service_uuids) if adv_data.service_uuids else 0
            
            # Device type (shortened)
            device_type = get_device_type(device_name, adv_data)
            if len(device_type) > 15:
                device_type = device_type[:12] + "..."
            
            # Main services (top 2)
            main_services = "None"
            if adv_data.service_uuids:
                service_names = []
                for uuid in adv_data.service_uuids[:2]:
                    service_name = get_service_name(uuid)
                    if "Unknown service" not in service_name:
                        service_names.append(service_name.split('(')[0].strip())
                    else:
                        # Show short UUID for unknown services
                        short_uuid = str(uuid)[:8]
                        service_names.append(f"{short_uuid}...")
                
                if service_names:
                    main_services = ", ".join(service_names)
                    if len(adv_data.service_uuids) > 2:
                        main_services += f" (+{len(adv_data.service_uuids)-2})"
            
            # Truncate long names for table formatting
            device_name_short = device_name[:18] + "..." if len(device_name) > 18 else device_name
            main_manufacturer_short = main_manufacturer[:12] + "..." if len(main_manufacturer) > 12 else main_manufacturer
            main_services_short = main_services[:25] + "..." if len(main_services) > 25 else main_services
            
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
                main_services_short
            ]
            
            table_data.append(row)
        
        # Create table with optimized column widths for A4
        col_widths = [0.3*inch, 1.2*inch, 1.0*inch, 0.5*inch, 0.6*inch, 
                     0.8*inch, 0.4*inch, 0.4*inch, 0.8*inch, 1.5*inch]
        
        main_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        main_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            
            # Data styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            
            # Borders and padding
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        story.append(main_table)
    
    # Footer
    story.append(Spacer(1, 20))
    story.append(Paragraph("=" * 80, styles['Normal']))
    story.append(Paragraph(
        f"Report generated by Bluetooth Scanner v2.0 | "
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"System: Windows • Library: bleak", 
        styles['Normal']
    ))
    
    # Build document
    doc.build(story)
    
    return filepath

if __name__ == "__main__":
    # Uruchom asynchroniczną funkcję główną
    asyncio.run(main())
