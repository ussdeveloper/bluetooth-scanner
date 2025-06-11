#!/usr/bin/env python3
"""
Simple test to verify bluetooth scanner functions work correctly
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the module
import bluetooth_scanner

def test_get_company_name():
    """Test company name detection"""
    print("Testing get_company_name...")
    
    # Test known manufacturers
    assert bluetooth_scanner.get_company_name(76) == "Apple, Inc."  # Apple is ID 76, not 0x004C
    assert bluetooth_scanner.get_company_name(6) == "Microsoft"
    assert bluetooth_scanner.get_company_name(15) == "Broadcom Corporation"
    
    # Test unknown manufacturer
    result = bluetooth_scanner.get_company_name(9999)
    assert "Unknown company" in result
    
    # Test edge cases with None
    result = bluetooth_scanner.get_company_name(None)
    assert "Unknown company" in result
    
    print("✅ get_company_name tests passed!")

def test_get_device_type():
    """Test device type detection"""
    print("Testing get_device_type...")
    
    # Create mock advertisement data
    class MockAdvData:
        def __init__(self):
            self.manufacturer_data = {}
            self.service_uuids = []
    
    mock_adv = MockAdvData()
    
    # Test smartphone detection
    result = bluetooth_scanner.get_device_type("iPhone 15", mock_adv)
    assert "Mobile Phone" in result or "📱" in result
    
    # Test headphones detection
    result = bluetooth_scanner.get_device_type("AirPods Pro", mock_adv)
    assert "Audio Device" in result or "🎧" in result
    
    # Test smartwatch detection  
    result = bluetooth_scanner.get_device_type("Apple Watch", mock_adv)
    assert "Wearable Device" in result or "⌚" in result
    
    # Test default case
    result = bluetooth_scanner.get_device_type("Unknown Device", mock_adv)
    assert "Bluetooth" in result or "🔵" in result
    
    print("✅ get_device_type tests passed!")

def test_signal_strength_text():
    """Test signal strength categorization"""
    print("Testing get_signal_strength_description...")
    
    # Test different signal levels
    result = bluetooth_scanner.get_signal_strength_description(-30)
    assert "Very Strong" in result or "Bardzo mocny" in result
    
    result = bluetooth_scanner.get_signal_strength_description(-50)
    assert "Strong" in result or "Mocny" in result or "Strong" in result
    
    result = bluetooth_scanner.get_signal_strength_description(-70)
    assert "Medium" in result or "Średni" in result
    
    result = bluetooth_scanner.get_signal_strength_description(-85)
    assert "Weak" in result or "Słaby" in result
    
    result = bluetooth_scanner.get_signal_strength_description(-95)
    assert "Very Weak" in result or "Bardzo słaby" in result
    
    print("✅ get_signal_strength_description tests passed!")

if __name__ == "__main__":
    print("🧪 Running simple bluetooth scanner tests...")
    print("=" * 50)
    
    try:
        test_get_company_name()
        test_get_device_type()
        test_signal_strength_text()
        
        print("=" * 50)
        print("🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
