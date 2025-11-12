# Video Converter Pro

A professional video and audio converter with CLI and GUI support. Convert videos to different codecs, formats, and optimize for various devices including feature phones.

## Features

### Core Features
- **Multiple Video Codecs**: H.264, H.265/HEVC, VP9, AV1, and more
- **Multiple Audio Codecs**: AAC, MP3, Opus, FLAC, and more
- **Container Formats**: MP4, MKV, AVI, WebM, MOV, 3GP, and more
- **Quality Presets**: High quality, standard, web-optimized, mobile, and feature phone presets
- **Batch Processing**: Convert multiple videos at once
- **Audio Extraction**: Extract audio from videos in various formats

### Professional Features
- **Video Trimming**: Cut videos to specific time ranges
- **Resolution Adjustment**: Change video resolution and aspect ratio
- **Bitrate Control**: Fine-tune video and audio bitrate
- **Frame Rate Adjustment**: Change video frame rate
- **Quality Control**: CRF-based quality settings
- **Progress Tracking**: Real-time conversion progress

### Device Optimization
- **Web Streaming**: Optimized presets for 1080p, 720p, 480p
- **Mobile Devices**: High-quality presets for smartphones
- **Feature Phones**: Special presets for low-end devices with physical keypads
  - Low resolution (240p, 176x144)
  - Low bitrate optimization
  - 3GP format support
  - Small file sizes

### Interface Options
- **CLI (Command-Line Interface)**: Powerful command-line tool for automation
- **GUI (Graphical User Interface)**: User-friendly visual interface
- **Both interfaces support all features**

## Installation

### Prerequisites
- Python 3.7 or higher
- FFmpeg (must be installed and in PATH)

#### Installing FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### Installing Video Converter

1. Clone the repository:
```bash
git clone https://github.com/hleong75/Vid-o-Converter.git
cd Vid-o-Converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Usage

### Command-Line Interface (CLI)

#### Basic Usage

Convert using a preset:
```bash
videoconv -i input.mp4 -p web_720p
```

Convert with custom settings:
```bash
videoconv -i input.mp4 -o output.mp4 --video-codec libx264 --crf 23
```

#### List Available Presets
```bash
videoconv --list-presets
```

#### Examples

**Web Optimization:**
```bash
# 1080p web streaming
videoconv -i input.mp4 -p web_1080p

# 720p web streaming
videoconv -i input.mp4 -p web_720p
```

**Mobile Conversion:**
```bash
# High quality for smartphones
videoconv -i input.mp4 -p mobile_high

# Standard quality
videoconv -i input.mp4 -p mobile_standard
```

**Feature Phone Optimization:**
```bash
# Best quality for feature phones
videoconv -i input.mp4 -p feature_phone_high

# Standard quality (smaller file)
videoconv -i input.mp4 -p feature_phone_standard

# Minimum size (lowest quality)
videoconv -i input.mp4 -p feature_phone_low
```

**Audio Extraction:**
```bash
# Extract as high-quality MP3
videoconv -i input.mp4 -p audio_mp3_high

# Extract as AAC
videoconv -i input.mp4 -p audio_aac

# Extract as lossless FLAC
videoconv -i input.mp4 -p audio_flac
```

**Video Trimming:**
```bash
# Trim from 10 seconds for 30 seconds duration
videoconv -i input.mp4 -o trimmed.mp4 --start-time 00:00:10 --duration 00:00:30
```

**Batch Processing:**
```bash
# Convert all MP4 files in current directory
videoconv --batch *.mp4 -p mobile_standard --output-dir converted

# Convert all videos in a directory
videoconv --batch /path/to/videos -p web_720p --output-dir output
```

**Get Video Information:**
```bash
videoconv -i input.mp4 --info
```

**Advanced Custom Settings:**
```bash
videoconv -i input.mp4 -o output.mp4 \
  --video-codec libx264 \
  --audio-codec aac \
  --resolution 1280x720 \
  --video-bitrate 2000k \
  --audio-bitrate 128k \
  --fps 30 \
  --crf 23
```

### Graphical User Interface (GUI)

Launch the GUI:
```bash
videoconv-gui
```

Or with Python:
```bash
python -m videoconverter.gui
```

#### GUI Features:
1. **Add Files**: Add individual video files or entire folders
2. **Select Preset**: Choose from categorized presets
3. **Advanced Options**: Fine-tune video/audio codecs, resolution, quality
4. **Batch Processing**: Convert multiple files at once
5. **Progress Tracking**: Visual progress bar with status updates
6. **Output Directory**: Choose where to save converted files

## Available Presets

### High Quality
- **High Quality H.264**: H.264 with AAC audio (CRF 18)
- **High Quality H.265**: H.265/HEVC with AAC audio (CRF 20)

### Standard Quality
- **Standard H.264**: Balanced quality and file size (CRF 23)

### Web Optimized
- **Web 1080p**: 1920x1080, 5000k bitrate
- **Web 720p**: 1280x720, 2500k bitrate
- **Web 480p**: 854x480, 1000k bitrate

### Mobile
- **Mobile High**: 1280x720, 2000k bitrate
- **Mobile Standard**: 854x480, 1000k bitrate

### Feature Phone
- **Feature Phone High**: 320x240, 256k bitrate, 15fps, 3GP format
- **Feature Phone Standard**: 240x180, 128k bitrate, 15fps, 3GP format
- **Feature Phone Low**: 176x144, 96k bitrate, 12fps, 3GP format

### Audio Extraction
- **MP3 High Quality**: 320k bitrate
- **MP3 Standard**: 192k bitrate
- **AAC Audio**: 192k bitrate, M4A format
- **Opus Audio**: 128k bitrate (high efficiency)
- **FLAC Audio**: Lossless compression

### Format Conversion
- **Convert to MP4**: Copy streams to MP4
- **Convert to MKV**: Copy streams to MKV
- **Convert to WebM**: VP9 video with Opus audio
- **Convert to AVI**: Copy streams to AVI

## Technical Details

### Supported Input Formats
- MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, 3GP, and more

### Supported Output Formats
- MP4, MKV, AVI, WebM, MOV, 3GP, M4A, MP3, AAC, Opus, FLAC

### Video Codecs
- H.264 (libx264)
- H.265/HEVC (libx265)
- VP9 (libvpx-vp9)
- AV1 (libaom-av1)
- Copy (no re-encoding)

### Audio Codecs
- AAC
- MP3 (libmp3lame)
- Opus (libopus)
- FLAC
- Copy (no re-encoding)

## Development

### Project Structure
```
Vid-o-Converter/
├── videoconverter/
│   ├── __init__.py          # Package initialization
│   ├── converter.py         # Core conversion engine
│   ├── presets.py           # Conversion presets
│   ├── cli.py               # Command-line interface
│   └── gui.py               # Graphical user interface
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
└── README.md               # This file
```

### Running Tests
```bash
# Check if FFmpeg is installed
ffmpeg -version

# Test CLI
videoconv --list-presets

# Test GUI (if display available)
videoconv-gui
```

## Troubleshooting

### FFmpeg Not Found
If you get an error about FFmpeg not being installed:
1. Install FFmpeg using instructions above
2. Verify installation: `ffmpeg -version`
3. Ensure FFmpeg is in your system PATH

### Permission Errors
If you get permission errors when writing output files:
1. Check output directory permissions
2. Try specifying a different output directory
3. Run with appropriate permissions

### Conversion Fails
If conversion fails:
1. Check input file is valid: `videoconv -i input.mp4 --info`
2. Try a different preset
3. Check FFmpeg error messages in console

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - See LICENSE file for details

## Credits

Built with:
- [FFmpeg](https://ffmpeg.org/) - Video/audio processing
- [Python](https://python.org/) - Core language
- [tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework

## Similar Tools

This tool provides features similar to professional video converters like 123apps, with the advantages of:
- Local processing (privacy and security)
- No file size limits
- No internet required
- Command-line automation
- Batch processing
- Free and open source