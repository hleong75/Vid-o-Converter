"""
Conversion presets for different use cases
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ConversionPreset:
    """Represents a conversion preset with specific settings"""
    name: str
    description: str
    video_codec: Optional[str] = None
    audio_codec: Optional[str] = None
    container: Optional[str] = None
    video_bitrate: Optional[str] = None
    audio_bitrate: Optional[str] = None
    resolution: Optional[str] = None
    fps: Optional[int] = None
    crf: Optional[int] = None
    preset: Optional[str] = None
    audio_sample_rate: Optional[int] = None
    
    def to_ffmpeg_params(self) -> Dict[str, Any]:
        """Convert preset to FFmpeg parameters"""
        params = {}
        
        if self.video_codec:
            params['vcodec'] = self.video_codec
        if self.audio_codec:
            params['acodec'] = self.audio_codec
        if self.video_bitrate:
            params['video_bitrate'] = self.video_bitrate
        if self.audio_bitrate:
            params['audio_bitrate'] = self.audio_bitrate
        if self.fps:
            params['r'] = str(self.fps)
        if self.crf is not None:
            params['crf'] = str(self.crf)
        if self.preset:
            params['preset'] = self.preset
        if self.audio_sample_rate:
            params['ar'] = str(self.audio_sample_rate)
            
        return params


# Standard presets
PRESETS = {
    # High quality presets
    "high_quality_h264": ConversionPreset(
        name="High Quality H.264",
        description="High quality H.264 video with AAC audio",
        video_codec="libx264",
        audio_codec="aac",
        container="mp4",
        crf=18,
        preset="slow",
        audio_bitrate="192k"
    ),
    "high_quality_h265": ConversionPreset(
        name="High Quality H.265",
        description="High quality H.265/HEVC video with AAC audio",
        video_codec="libx265",
        audio_codec="aac",
        container="mp4",
        crf=20,
        preset="slow",
        audio_bitrate="192k"
    ),
    
    # Standard quality presets
    "standard_h264": ConversionPreset(
        name="Standard H.264",
        description="Balanced quality and file size",
        video_codec="libx264",
        audio_codec="aac",
        container="mp4",
        crf=23,
        preset="medium",
        audio_bitrate="128k"
    ),
    
    # Web optimized presets
    "web_1080p": ConversionPreset(
        name="Web 1080p",
        description="Optimized for web streaming (1080p)",
        video_codec="libx264",
        audio_codec="aac",
        container="mp4",
        resolution="1920x1080",
        video_bitrate="5000k",
        audio_bitrate="128k",
        preset="medium"
    ),
    "web_720p": ConversionPreset(
        name="Web 720p",
        description="Optimized for web streaming (720p)",
        video_codec="libx264",
        audio_codec="aac",
        container="mp4",
        resolution="1280x720",
        video_bitrate="2500k",
        audio_bitrate="128k",
        preset="medium"
    ),
    "web_480p": ConversionPreset(
        name="Web 480p",
        description="Optimized for web streaming (480p)",
        video_codec="libx264",
        audio_codec="aac",
        container="mp4",
        resolution="854x480",
        video_bitrate="1000k",
        audio_bitrate="96k",
        preset="medium"
    ),
    
    # Mobile presets
    "mobile_high": ConversionPreset(
        name="Mobile High",
        description="High quality for modern smartphones",
        video_codec="libx264",
        audio_codec="aac",
        container="mp4",
        resolution="1280x720",
        video_bitrate="2000k",
        audio_bitrate="128k",
        preset="medium"
    ),
    "mobile_standard": ConversionPreset(
        name="Mobile Standard",
        description="Standard quality for smartphones",
        video_codec="libx264",
        audio_codec="aac",
        container="mp4",
        resolution="854x480",
        video_bitrate="1000k",
        audio_bitrate="96k",
        preset="medium"
    ),
    
    # Feature phone presets (low-end devices)
    "feature_phone_high": ConversionPreset(
        name="Feature Phone High",
        description="Best quality for feature phones",
        video_codec="libx264",
        audio_codec="aac",
        container="3gp",
        resolution="320x240",
        video_bitrate="256k",
        audio_bitrate="48k",
        fps=15,
        preset="fast"
    ),
    "feature_phone_standard": ConversionPreset(
        name="Feature Phone Standard",
        description="Standard quality for feature phones",
        video_codec="libx264",
        audio_codec="aac",
        container="3gp",
        resolution="240x180",
        video_bitrate="128k",
        audio_bitrate="32k",
        fps=15,
        preset="fast"
    ),
    "feature_phone_low": ConversionPreset(
        name="Feature Phone Low",
        description="Minimum size for feature phones",
        video_codec="libx264",
        audio_codec="aac",
        container="3gp",
        resolution="176x144",
        video_bitrate="96k",
        audio_bitrate="24k",
        fps=12,
        preset="ultrafast"
    ),
    
    # Audio extraction presets
    "audio_mp3_high": ConversionPreset(
        name="MP3 High Quality",
        description="Extract audio as high quality MP3",
        audio_codec="libmp3lame",
        container="mp3",
        audio_bitrate="320k"
    ),
    "audio_mp3_standard": ConversionPreset(
        name="MP3 Standard",
        description="Extract audio as standard MP3",
        audio_codec="libmp3lame",
        container="mp3",
        audio_bitrate="192k"
    ),
    "audio_aac": ConversionPreset(
        name="AAC Audio",
        description="Extract audio as AAC",
        audio_codec="aac",
        container="m4a",
        audio_bitrate="192k"
    ),
    "audio_opus": ConversionPreset(
        name="Opus Audio",
        description="Extract audio as Opus (high efficiency)",
        audio_codec="libopus",
        container="opus",
        audio_bitrate="128k"
    ),
    "audio_flac": ConversionPreset(
        name="FLAC Audio",
        description="Extract audio as lossless FLAC",
        audio_codec="flac",
        container="flac"
    ),
    
    # Format conversion presets
    "to_mp4": ConversionPreset(
        name="Convert to MP4",
        description="Convert to MP4 container",
        video_codec="copy",
        audio_codec="copy",
        container="mp4"
    ),
    "to_mkv": ConversionPreset(
        name="Convert to MKV",
        description="Convert to MKV container",
        video_codec="copy",
        audio_codec="copy",
        container="mkv"
    ),
    "to_webm": ConversionPreset(
        name="Convert to WebM",
        description="Convert to WebM with VP9",
        video_codec="libvpx-vp9",
        audio_codec="libopus",
        container="webm",
        crf=30,
        audio_bitrate="128k"
    ),
    "to_avi": ConversionPreset(
        name="Convert to AVI",
        description="Convert to AVI container",
        video_codec="copy",
        audio_codec="copy",
        container="avi"
    ),
}


def get_preset(name: str) -> Optional[ConversionPreset]:
    """Get a preset by name"""
    return PRESETS.get(name)


def list_presets() -> Dict[str, ConversionPreset]:
    """List all available presets"""
    return PRESETS.copy()


def get_presets_by_category():
    """Get presets organized by category"""
    return {
        "High Quality": [
            PRESETS["high_quality_h264"],
            PRESETS["high_quality_h265"],
        ],
        "Standard Quality": [
            PRESETS["standard_h264"],
        ],
        "Web Optimized": [
            PRESETS["web_1080p"],
            PRESETS["web_720p"],
            PRESETS["web_480p"],
        ],
        "Mobile": [
            PRESETS["mobile_high"],
            PRESETS["mobile_standard"],
        ],
        "Feature Phone": [
            PRESETS["feature_phone_high"],
            PRESETS["feature_phone_standard"],
            PRESETS["feature_phone_low"],
        ],
        "Audio Extraction": [
            PRESETS["audio_mp3_high"],
            PRESETS["audio_mp3_standard"],
            PRESETS["audio_aac"],
            PRESETS["audio_opus"],
            PRESETS["audio_flac"],
        ],
        "Format Conversion": [
            PRESETS["to_mp4"],
            PRESETS["to_mkv"],
            PRESETS["to_webm"],
            PRESETS["to_avi"],
        ],
    }
