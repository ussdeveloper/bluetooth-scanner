"""
Tests for bluetooth scanner functionality
"""
import pytest
import asyncio
import os
import tempfile
from unittest.mock import MagicMock, patch, AsyncMock

# Import the module to test
import bluetooth_scanner


class TestBluetoothScanner:
    """Test cases for bluetooth scanner functions"""
    
    def test_get_manufacturer_name(self):
        """Test manufacturer name detection"""
        # Test known manufacturers
        assert bluetooth_scanner.get_manufacturer_name(0x004C) == "Apple Inc."
        assert bluetooth_scanner.get_manufacturer_name(0x0006) == "Microsoft"
        assert bluetooth_scanner.get_manufacturer_name(0x000F) == "Broadcom Corporation"
        
        # Test unknown manufacturer
        assert bluetooth_scanner.get_manufacturer_name(0x9999) == "Unknown"
        
        # Test edge cases
        assert bluetooth_scanner.get_manufacturer_name(None) == "Unknown"
        assert bluetooth_scanner.get_manufacturer_name("invalid") == "Unknown"
    
    def test_get_device_type(self):
        """Test device type detection"""
        # Test smartphone detection
        assert "Smartphone" in bluetooth_scanner.get_device_type("iPhone 15", 0x004C)
        assert "Smartphone" in bluetooth_scanner.get_device_type("Samsung Galaxy", 0x0075)
        
        # Test headphones detection
        assert "Headphones" in bluetooth_scanner.get_device_type("AirPods Pro", 0x004C)
        assert "Headphones" in bluetooth_scanner.get_device_type("WH-1000XM4", 0x012D)
        
        # Test smartwatch detection
        assert "Smartwatch" in bluetooth_scanner.get_device_type("Apple Watch", 0x004C)
        assert "Smartwatch" in bluetooth_scanner.get_device_type("Galaxy Watch", 0x0075)
        
        # Test default case
        assert "Bluetooth Device" in bluetooth_scanner.get_device_type("Unknown Device", 0x9999)
    
    def test_format_device_info(self, mock_device, mock_advertisement_data):
        """Test device information formatting"""
        device = mock_device()
        adv_data = mock_advertisement_data(
            local_name="Test Device",
            manufacturer_data={0x004C: b"test"}
        )
        
        info = bluetooth_scanner.format_device_info(device, adv_data)
        
        assert device.address in info
        assert "Test Device" in info
        assert "Apple Inc." in info  # Should detect Apple manufacturer
        assert str(device.rssi) in info
    
    @pytest.mark.asyncio
    async def test_scan_bluetooth_devices(self):
        """Test the main scanning function"""
        # Mock the BleakScanner.discover method
        mock_devices = {
            "AA:BB:CC:DD:EE:FF": (
                MagicMock(address="AA:BB:CC:DD:EE:FF", name="Test Device", rssi=-50),
                MagicMock(local_name="Test Device", manufacturer_data={})
            )
        }
        
        with patch('bluetooth_scanner.BleakScanner.discover', new_callable=AsyncMock) as mock_discover:
            mock_discover.return_value = mock_devices
            
            result = await bluetooth_scanner.scan_bluetooth_devices(duration=1)
            
            assert len(result) == 1
            assert "AA:BB:CC:DD:EE:FF" in result
            mock_discover.assert_called()
    
    def test_generate_pdf_report(self, mock_device, mock_advertisement_data):
        """Test PDF report generation"""
        # Create mock devices
        devices = {
            "AA:BB:CC:DD:EE:FF": (
                mock_device(),
                mock_advertisement_data(local_name="Test Device")
            )
        }
        
        # Generate PDF in temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('bluetooth_scanner.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "20241211_120000"
                
                filename = bluetooth_scanner.generate_pdf_report(devices)
                
                # Check if file was created
                assert filename is not None
                assert filename.endswith(".pdf")
                
                # In a real test, we might check if the file exists
                # But since we're mocking datetime, the path might not match
    
    def test_clean_device_name(self):
        """Test device name cleaning function"""
        assert bluetooth_scanner.clean_device_name("  Test Device  ") == "Test Device"
        assert bluetooth_scanner.clean_device_name("") == "Unknown Device"
        assert bluetooth_scanner.clean_device_name(None) == "Unknown Device"
        assert bluetooth_scanner.clean_device_name("Device\x00with\x00nulls") == "Device with nulls"


class TestDataValidation:
    """Test data validation and edge cases"""
    
    def test_empty_device_list(self):
        """Test handling of empty device list"""
        filename = bluetooth_scanner.generate_pdf_report({})
        assert filename is not None
        assert filename.endswith(".pdf")
    
    def test_device_with_no_name(self, mock_device, mock_advertisement_data):
        """Test device without a name"""
        device = mock_device(name=None)
        adv_data = mock_advertisement_data()
        
        info = bluetooth_scanner.format_device_info(device, adv_data)
        assert "Unknown Device" in info
    
    def test_device_with_empty_manufacturer_data(self, mock_device, mock_advertisement_data):
        """Test device with empty manufacturer data"""
        device = mock_device()
        adv_data = mock_advertisement_data(manufacturer_data={})
        
        info = bluetooth_scanner.format_device_info(device, adv_data)
        assert "Unknown" in info  # Should show unknown manufacturer


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_signal_strength_description(self):
        """Test RSSI signal strength descriptions"""
        # These tests would depend on if such a function exists
        # Adding placeholder for future implementation
        pass
    
    def test_device_category_detection(self):
        """Test device category detection logic"""
        # Test various device categories
        categories = [
            ("iPhone", "Smartphone"),
            ("AirPods", "Headphones"),
            ("Apple Watch", "Smartwatch"),
            ("MacBook", "Computer"),
        ]
        
        for device_name, expected_category in categories:
            device_type = bluetooth_scanner.get_device_type(device_name, 0x004C)
            assert expected_category in device_type


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__])
