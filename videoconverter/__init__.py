"""
Video Converter Package
Professional video and audio conversion tool with CLI and GUI support
"""

__version__ = "1.0.0"
__author__ = "Video Converter Team"

from .converter import VideoConverter
from .presets import ConversionPreset

__all__ = ["VideoConverter", "ConversionPreset"]
