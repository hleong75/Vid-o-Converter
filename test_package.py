#!/usr/bin/env python3
"""
Simple test script to verify the video converter package
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from videoconverter import VideoConverter, ConversionPreset
        print("✓ Core modules imported successfully")
        
        from videoconverter.presets import list_presets, get_preset
        print("✓ Presets module imported successfully")
        
        from videoconverter.cli import main as cli_main
        print("✓ CLI module imported successfully")
        
        # GUI module requires tkinter which may not be available
        try:
            from videoconverter.gui import main as gui_main
            print("✓ GUI module imported successfully")
        except ImportError as e:
            if 'tkinter' in str(e):
                print("⚠ GUI module requires tkinter (not available in this environment)")
            else:
                raise
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_presets():
    """Test preset functionality"""
    print("\nTesting presets...")
    try:
        from videoconverter.presets import list_presets, get_preset, get_presets_by_category
        
        presets = list_presets()
        print(f"✓ Found {len(presets)} presets")
        
        categories = get_presets_by_category()
        print(f"✓ Found {len(categories)} preset categories")
        
        # Test getting a specific preset
        preset = get_preset("web_720p")
        if preset:
            print(f"✓ Successfully retrieved 'web_720p' preset")
            print(f"  - Name: {preset.name}")
            print(f"  - Description: {preset.description}")
        else:
            print("✗ Failed to retrieve 'web_720p' preset")
            return False
        
        # Test feature phone presets
        for preset_name in ["feature_phone_high", "feature_phone_standard", "feature_phone_low"]:
            preset = get_preset(preset_name)
            if preset:
                print(f"✓ Feature phone preset '{preset_name}' exists")
            else:
                print(f"✗ Feature phone preset '{preset_name}' not found")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error testing presets: {e}")
        return False

def test_converter_init():
    """Test converter initialization (without FFmpeg)"""
    print("\nTesting converter initialization...")
    try:
        from videoconverter import VideoConverter
        
        # This will fail if FFmpeg is not installed, which is expected
        try:
            converter = VideoConverter()
            print("✓ VideoConverter initialized successfully")
            print("  (FFmpeg is installed)")
            return True
        except RuntimeError as e:
            if "FFmpeg is not installed" in str(e):
                print("⚠ FFmpeg is not installed (this is expected in CI)")
                print("  VideoConverter requires FFmpeg to be installed")
                return True
            else:
                raise
    except Exception as e:
        print(f"✗ Error testing converter: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Video Converter Package Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Presets", test_presets()))
    results.append(("Converter Init", test_converter_init()))
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
