"""
Test configuration for pytest
"""
import pytest
import asyncio
import sys
import os

# Add the parent directory to the path to import bluetooth_scanner
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_device():
    """Mock device for testing"""
    class MockDevice:
        def __init__(self, address="AA:BB:CC:DD:EE:FF", name="Test Device", rssi=-50):
            self.address = address
            self.name = name
            self.rssi = rssi
            
        def __str__(self):
            return f"{self.name} ({self.address})"
    
    return MockDevice

@pytest.fixture
def mock_advertisement_data():
    """Mock advertisement data for testing"""
    class MockAdvertisementData:
        def __init__(self, local_name=None, manufacturer_data=None, service_data=None):
            self.local_name = local_name
            self.manufacturer_data = manufacturer_data or {}
            self.service_data = service_data or {}
            
    return MockAdvertisementData
