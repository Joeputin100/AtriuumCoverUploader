#!/usr/bin/env python3
"""
Platform detection utility for AtriuumCoverUploader
Determines the execution environment and configures dependencies accordingly
"""

import os
import sys
import platform
from typing import Dict, Any


class PlatformDetector:
    """Detects and configures the execution platform."""
    
    def __init__(self):
        self.platform_info = self.detect_platform()
    
    def detect_platform(self) -> Dict[str, Any]:
        """Detect the current execution platform."""
        platform_info = {
            'name': 'unknown',
            'supports_playwright': False,
            'supports_headless': False,
            'is_cloud': False,
            'is_termux': False,
            'python_version': platform.python_version(),
            'system': platform.system(),
            'machine': platform.machine(),
        }
        
        # Check for Termux
        if 'com.termux' in sys.prefix or 'TERMUX_VERSION' in os.environ:
            platform_info.update({
                'name': 'termux',
                'supports_playwright': False,
                'supports_headless': False,
                'is_termux': True,
                'browser_recommendation': 'selenium'
            })
        
        # Check for Replit
        elif 'REPLIT' in os.environ or 'REPL_ID' in os.environ:
            platform_info.update({
                'name': 'replit',
                'supports_playwright': True,
                'supports_headless': True,
                'is_cloud': True,
                'browser_recommendation': 'playwright'
            })
        
        # Check for GitHub Actions
        elif 'GITHUB_ACTIONS' in os.environ:
            platform_info.update({
                'name': 'github-actions',
                'supports_playwright': True,
                'supports_headless': True,
                'is_cloud': True,
                'browser_recommendation': 'playwright'
            })
        
        # Check for local Linux/macOS/Windows
        else:
            platform_info.update({
                'name': 'local',
                'supports_playwright': True,
                'supports_headless': True,
                'browser_recommendation': 'playwright'
            })
        
        return platform_info
    
    def get_browser_config(self) -> Dict[str, Any]:
        """Get browser configuration based on platform."""
        if self.platform_info['supports_playwright']:
            return {
                'browser_type': 'playwright',
                'headless': True,
                'timeout': 30000,
                'retries': 3
            }
        else:
            return {
                'browser_type': 'selenium',
                'headless': False,  # Termux doesn't support headless well
                'timeout': 45000,   # Longer timeout for Termux
                'retries': 5        # More retries for reliability
            }
    
    def get_requirements_file(self) -> str:
        """Get the appropriate requirements file."""
        if self.platform_info['is_cloud']:
            return 'requirements-cloud.txt'
        else:
            return 'requirements.txt'
    
    def print_platform_info(self):
        """Print platform detection results."""
        print("🔍 Platform Detection Results:")
        print(f"   Platform: {self.platform_info['name']}")
        print(f"   Python: {self.platform_info['python_version']}")
        print(f"   System: {self.platform_info['system']} {self.platform_info['machine']}")
        print(f"   Supports Playwright: {self.platform_info['supports_playwright']}")
        print(f"   Supports Headless: {self.platform_info['supports_headless']}")
        print(f"   Recommended Browser: {self.platform_info.get('browser_recommendation', 'unknown')}")
        print(f"   Requirements File: {self.get_requirements_file()}")
        
        browser_config = self.get_browser_config()
        print(f"   Browser Config: {browser_config['browser_type']} (headless: {browser_config['headless']})")


def main():
    """Main function for platform detection."""
    detector = PlatformDetector()
    detector.print_platform_info()
    
    # Return appropriate exit code
    if detector.platform_info['name'] == 'unknown':
        print("⚠️  Warning: Unknown platform detected")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())