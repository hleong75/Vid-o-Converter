# Project Structure

## Directory Layout

```
Vid-o-Converter/
├── README.md                    # Main documentation
├── QUICKSTART.md               # Quick start guide
├── INSTALL.md                  # Installation instructions
├── FEATURES.md                 # Detailed feature documentation
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup configuration
├── test_package.py            # Test suite
├── examples.sh                # CLI usage examples
│
└── videoconverter/            # Main package directory
    ├── __init__.py            # Package initialization
    ├── converter.py           # Core conversion engine (FFmpeg wrapper)
    ├── presets.py             # Conversion presets and configurations
    ├── cli.py                 # Command-line interface
    └── gui.py                 # Graphical user interface
```

## Module Overview

### `videoconverter/converter.py`
**Core Conversion Engine**

Main class: `VideoConverter`

Key methods:
- `convert()` - Main conversion method with full control
- `extract_audio()` - Extract audio from video
- `change_container()` - Change format without re-encoding
- `trim_video()` - Cut video to time range
- `convert_with_preset()` - Convert using preset
- `get_video_info()` - Get video metadata

Uses FFmpeg for actual video processing.

### `videoconverter/presets.py`
**Conversion Presets**

Main class: `ConversionPreset`

Preset categories:
- High Quality (2 presets)
- Standard Quality (1 preset)
- Web Optimized (3 presets: 1080p, 720p, 480p)
- Mobile (2 presets)
- Feature Phone (3 presets: high, standard, low)
- Audio Extraction (5 presets: MP3, AAC, Opus, FLAC)
- Format Conversion (4 presets: MP4, MKV, WebM, AVI)

Total: 20 presets

### `videoconverter/cli.py`
**Command-Line Interface**

Entry point: `videoconv` command

Features:
- Single file conversion
- Batch processing
- Video information display
- Progress tracking with tqdm
- Support for all presets
- Advanced parameter control

### `videoconverter/gui.py`
**Graphical User Interface**

Entry point: `videoconv-gui` command

Main class: `VideoConverterGUI`

Features:
- File/folder selection
- Preset browser
- Advanced options panel
- Real-time progress bar
- Batch processing
- Output directory selection

Built with tkinter (included with Python).

## Data Flow

```
Input Video File(s)
        ↓
[CLI or GUI Interface]
        ↓
[Preset Selection or Manual Config]
        ↓
[VideoConverter Class]
        ↓
[FFmpeg Processing]
        ↓
[Progress Callback]
        ↓
Output Video File(s)
```

## Key Dependencies

### Required
- **Python 3.7+**: Core language
- **FFmpeg**: Video processing engine (external)
- **ffmpeg-python**: Python wrapper for FFmpeg
- **tqdm**: Progress bars for CLI

### Optional
- **tkinter**: GUI support (usually included with Python)
- **Pillow**: Image processing (for GUI enhancements)

## Supported Formats

### Input Formats
MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, 3GP, and more

### Output Formats
MP4, MKV, AVI, WebM, MOV, 3GP (video)
MP3, M4A, AAC, Opus, FLAC (audio)

### Video Codecs
- H.264 (libx264) - Most compatible
- H.265 (libx265) - Better compression
- VP9 (libvpx-vp9) - Web optimized
- AV1 (libaom-av1) - Next generation
- Copy - No re-encoding

### Audio Codecs
- AAC - Best for MP4
- MP3 (libmp3lame) - Universal
- Opus (libopus) - High efficiency
- FLAC - Lossless
- Copy - No re-encoding

## Feature Comparison

| Feature | CLI | GUI |
|---------|-----|-----|
| Single file conversion | ✓ | ✓ |
| Batch processing | ✓ | ✓ |
| Preset support | ✓ | ✓ |
| Advanced options | ✓ | ✓ |
| Progress tracking | ✓ | ✓ |
| Video information | ✓ | ✗ |
| Scripting/automation | ✓ | ✗ |
| Drag & drop | ✗ | ✓ |
| Visual preset browser | ✗ | ✓ |

Both interfaces support the same core features.

## Preset Matrix

| Category | Count | Use Case |
|----------|-------|----------|
| High Quality | 2 | Archival, professional |
| Standard | 1 | General use |
| Web | 3 | Online streaming |
| Mobile | 2 | Smartphones |
| Feature Phone | 3 | Basic phones |
| Audio | 5 | Audio extraction |
| Format | 4 | Container conversion |

## Architecture Principles

1. **Separation of Concerns**
   - Core engine (converter.py)
   - Configuration (presets.py)
   - User interfaces (cli.py, gui.py)

2. **Modularity**
   - Each module has a single responsibility
   - Easy to extend with new presets or features
   - Can use CLI or GUI independently

3. **Flexibility**
   - Support both preset and manual modes
   - Progress callback system
   - Batch processing built-in

4. **User-Friendly**
   - Sensible defaults
   - Clear error messages
   - Comprehensive documentation

5. **Professional Quality**
   - Feature parity with commercial tools
   - No artificial limitations
   - Full control when needed

## Extension Points

To add new features:

1. **New Codec**: Add to converter.py methods
2. **New Preset**: Add to presets.py PRESETS dict
3. **New CLI Option**: Add to cli.py argument parser
4. **New GUI Feature**: Add to gui.py interface

## Testing

Run tests:
```bash
python test_package.py
```

Tests verify:
- Module imports
- Preset availability
- Converter initialization
- Feature phone presets

## Performance Considerations

- Conversion speed depends on:
  - Input file size
  - Output settings (resolution, codec)
  - Encoding preset (ultrafast to veryslow)
  - CPU performance
  
- Typical conversion time for 5-minute 1080p video: 1-5 minutes

## Security

- No network access required
- No external API calls
- Processes files locally
- No telemetry or data collection
- All processing done by FFmpeg (trusted, open-source)

CodeQL security scan: ✓ 0 vulnerabilities found

## License

MIT License - Free to use, modify, and distribute
