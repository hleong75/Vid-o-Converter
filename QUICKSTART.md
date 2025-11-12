# Quick Start Guide

Get started with Video Converter Pro in 5 minutes!

## Installation

1. Install FFmpeg (required):
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows: Download from ffmpeg.org and add to PATH
   ```

2. Install Video Converter:
   ```bash
   git clone https://github.com/hleong75/Vid-o-Converter.git
   cd Vid-o-Converter
   pip install -r requirements.txt
   pip install -e .
   ```

3. Verify installation:
   ```bash
   videoconv --help
   python test_package.py
   ```

## Basic Usage

### GUI (Easiest Way)

```bash
videoconv-gui
```

1. Click "Add Files" to select videos
2. Choose a preset from the dropdown
3. Select output directory
4. Click "Convert"

### CLI (Quick Examples)

```bash
# See all presets
videoconv --list-presets

# Convert for web (720p)
videoconv -i input.mp4 -p web_720p

# Convert for mobile
videoconv -i input.mp4 -p mobile_high

# Convert for feature phone
videoconv -i input.mp4 -p feature_phone_standard

# Extract audio as MP3
videoconv -i input.mp4 -p audio_mp3_high

# Get video information
videoconv -i input.mp4 --info
```

## Common Tasks

### Task 1: Convert for YouTube/Web
```bash
videoconv -i myvideo.mp4 -p web_1080p
```

### Task 2: Reduce File Size
```bash
videoconv -i large.mp4 -p mobile_standard
```

### Task 3: Convert for Old Phone
```bash
videoconv -i video.mp4 -p feature_phone_high
```

### Task 4: Extract Audio
```bash
videoconv -i video.mp4 -p audio_mp3_high
```

### Task 5: Trim Video
```bash
videoconv -i long.mp4 -o short.mp4 \
  --start-time 00:01:00 \
  --duration 00:00:30
```

### Task 6: Batch Convert
```bash
videoconv --batch *.mp4 -p web_720p --output-dir converted
```

## Choosing the Right Preset

| Use Case | Preset | File Size | Quality |
|----------|--------|-----------|---------|
| YouTube/Vimeo | `web_1080p` | Large | Excellent |
| Social Media | `web_720p` | Medium | Great |
| WhatsApp/Email | `mobile_standard` | Small | Good |
| Feature Phone | `feature_phone_standard` | Very Small | Acceptable |
| Music Extraction | `audio_mp3_high` | Small | Excellent |

## Tips

1. **Always use presets first** - They're optimized for specific uses
2. **Check video info** - Use `--info` to see current format before converting
3. **Test on one file** - Before batch converting, test on one file
4. **Backup originals** - Always keep your original files
5. **Use batch mode** - Convert multiple files at once with `--batch`

## Getting Help

- Full documentation: `README.md`
- Installation help: `INSTALL.md`
- Feature details: `FEATURES.md`
- Examples: Run `./examples.sh`
- CLI help: `videoconv --help`

## Troubleshooting

**Problem:** "FFmpeg is not installed"
**Solution:** Install FFmpeg (see Installation above)

**Problem:** "videoconv: command not found"
**Solution:** Run `pip install -e .` in the project directory

**Problem:** Conversion is slow
**Solution:** Use a faster preset or lower resolution

**Problem:** Output file is too large
**Solution:** Use a lower quality preset or higher CRF value

---

For more details, see the full [README.md](README.md) documentation.
