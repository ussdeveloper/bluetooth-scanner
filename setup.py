#!/usr/bin/env python3
"""
Setup script for bluetooth-scanner package
"""
from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bluetooth-scanner",
    version="1.0.0",
    author="USS Developer",
    author_email="ussdeveloper@example.com",
    description="Professional Bluetooth Low Energy (BLE) scanner with PDF reporting",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ussdeveloper/bluetooth-scanner",
    py_modules=["bluetooth_scanner"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Networking",
        "Topic :: Communications",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "pytest-mock",
            "black",
            "flake8",
            "mypy",
            "coverage",
        ],
        "build": [
            "pyinstaller",
        ],
    },
    entry_points={
        "console_scripts": [
            "bluetooth-scanner=bluetooth_scanner:main",
        ],
    },
    keywords="bluetooth, ble, scanner, network, devices, pdf, report",
    project_urls={
        "Bug Reports": "https://github.com/ussdeveloper/bluetooth-scanner/issues",
        "Source": "https://github.com/ussdeveloper/bluetooth-scanner",
        "Documentation": "https://github.com/ussdeveloper/bluetooth-scanner#readme",
    },
)
