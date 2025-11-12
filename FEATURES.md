# Features Documentation

## Overview

Video Converter Pro provides comprehensive video and audio conversion capabilities similar to professional tools like 123apps, with the advantages of local processing, no file size limits, and complete privacy.

## Core Features

### 1. Video Codec Support

Convert videos between multiple modern and legacy codecs:

- **H.264 (AVC)**: Most compatible codec, works on all devices
- **H.265 (HEVC)**: Better compression, smaller files, newer devices
- **VP9**: Google's codec, excellent for web streaming
- **AV1**: Next-generation codec, best compression (requires modern FFmpeg)
- **Copy**: Keep original codec without re-encoding (fast)

**Example:**
```bash
# Convert to H.265 for better compression
videoconv -i input.mp4 -o output.mp4 --video-codec libx265 --crf 23
```

### 2. Audio Codec Support

Extract and convert audio in various formats:

- **AAC**: Best for MP4/M4A, wide compatibility
- **MP3**: Universal compatibility, good for music
- **Opus**: Best quality-to-size ratio for speech and music
- **FLAC**: Lossless compression, archival quality
- **Copy**: Keep original audio without re-encoding

**Example:**
```bash
# Extract high-quality MP3 audio
videoconv -i video.mp4 -p audio_mp3_high
```

### 3. Container Format Support

Convert between different container formats:

- **MP4**: Most compatible, works everywhere
- **MKV**: Supports multiple audio/subtitle tracks
- **WebM**: Optimized for web, HTML5 compatible
- **AVI**: Legacy format for older devices
- **3GP**: Mobile phones, especially feature phones
- **MOV**: Apple QuickTime format

**Example:**
```bash
# Change container without re-encoding (fast)
videoconv -i input.avi -o output.mp4 --video-codec copy --audio-codec copy
```

### 4. Quality Control

Fine-tune output quality with multiple methods:

#### CRF (Constant Rate Factor)
- Scale: 0-51 (lower = better quality, larger file)
- Recommended: 18-28
- 18: Visually lossless
- 23: Default, good balance
- 28: Lower quality, smaller file

**Example:**
```bash
videoconv -i input.mp4 -o output.mp4 --crf 20
```

#### Bitrate Control
- Specify exact video/audio bitrate
- More predictable file sizes
- Use k (kilobits) or M (megabits)

**Example:**
```bash
videoconv -i input.mp4 -o output.mp4 \
  --video-bitrate 2000k \
  --audio-bitrate 128k
```

### 5. Resolution and Scaling

Change video resolution for different purposes:

**Common Resolutions:**
- **1920x1080** (1080p/Full HD): High quality, large files
- **1280x720** (720p/HD): Good quality, medium files
- **854x480** (480p/SD): Decent quality, small files
- **640x360** (360p): Low quality, very small files
- **320x240** (240p): Feature phones, tiny files

**Example:**
```bash
# Scale to 720p
videoconv -i input.mp4 -o output.mp4 --resolution 1280x720
```

### 6. Frame Rate Adjustment

Change video frame rate (FPS):

- **60fps**: Smooth motion, sports, gaming
- **30fps**: Standard video, most common
- **24fps**: Cinematic look, movies
- **15fps**: Low bandwidth, feature phones

**Example:**
```bash
videoconv -i input.mp4 -o output.mp4 --fps 30
```

### 7. Video Trimming

Cut videos to specific time ranges:

**Time Format:**
- Seconds: `10`, `90`
- HH:MM:SS: `00:01:30`, `00:00:10`

**Example:**
```bash
# Extract 30 seconds starting at 10 seconds
videoconv -i input.mp4 -o trimmed.mp4 \
  --start-time 00:00:10 \
  --duration 00:00:30
```

### 8. Batch Processing

Convert multiple videos at once:

**Example:**
```bash
# Convert all MP4 files in current directory
videoconv --batch *.mp4 -p web_720p --output-dir converted

# Convert all videos in a folder
videoconv --batch /path/to/videos -p mobile_standard --output-dir output
```

## Preset Categories

### High Quality Presets

For archival and professional use:

- **High Quality H.264**: CRF 18, slow preset
- **High Quality H.265**: CRF 20, slow preset, 40% smaller files

**Use when:**
- Archiving important videos
- Need best possible quality
- File size is not a concern

### Web Optimized Presets

For online streaming and sharing:

- **Web 1080p**: 5000k bitrate, 1920x1080
- **Web 720p**: 2500k bitrate, 1280x720
- **Web 480p**: 1000k bitrate, 854x480

**Use when:**
- Uploading to YouTube, Vimeo, etc.
- Embedding in websites
- Sharing on social media

### Mobile Presets

For smartphones and tablets:

- **Mobile High**: 720p, 2000k bitrate
- **Mobile Standard**: 480p, 1000k bitrate

**Use when:**
- Viewing on phones/tablets
- Saving phone storage
- Mobile data constraints

### Feature Phone Presets

For devices with physical keypads and limited capabilities:

- **Feature Phone High**: 320x240, 256k bitrate, 15fps, 3GP format
- **Feature Phone Standard**: 240x180, 128k bitrate, 15fps, 3GP format
- **Feature Phone Low**: 176x144, 96k bitrate, 12fps, 3GP format

**Use when:**
- Target device has physical keypad
- Very limited storage (< 1GB)
- Slow processor
- Need smallest possible file size

**File Size Comparison:**
For a 5-minute video:
- Original (1080p): ~200MB
- Feature Phone High: ~10MB
- Feature Phone Standard: ~5MB
- Feature Phone Low: ~3MB

### Audio Extraction Presets

For extracting audio from videos:

- **MP3 High Quality**: 320k bitrate
- **MP3 Standard**: 192k bitrate
- **AAC Audio**: 192k bitrate, M4A format
- **Opus Audio**: 128k bitrate (best efficiency)
- **FLAC Audio**: Lossless (largest file)

**Use when:**
- Creating audio podcasts from videos
- Extracting music tracks
- Converting for audio players

## Advanced Features

### 1. Encoding Speed Presets

Balance between speed and compression:

- **ultrafast**: Fastest, largest files
- **superfast, veryfast, faster, fast**: Speed/size tradeoffs
- **medium**: Default, good balance
- **slow, slower, veryslow**: Best compression, slowest

**Example:**
```bash
videoconv -i input.mp4 -o output.mp4 --encoding-preset fast
```

### 2. Audio Sample Rate

Change audio quality:

- **48000 Hz**: Professional audio
- **44100 Hz**: CD quality (default)
- **22050 Hz**: Lower quality, smaller files

**Example:**
```bash
videoconv -i input.mp4 -o output.mp4 --audio-sample-rate 44100
```

### 3. Video Information

Get detailed information about video files:

```bash
videoconv -i input.mp4 --info
```

Shows:
- Format and duration
- File size and bitrate
- Video codec, resolution, FPS
- Audio codec, sample rate, channels

## CLI vs GUI

### CLI (Command-Line Interface)

**Advantages:**
- Automation and scripting
- Batch processing multiple files
- Integration with other tools
- Remote server use
- More control over parameters

**Best for:**
- Power users
- Automated workflows
- Server environments
- Batch conversions

### GUI (Graphical User Interface)

**Advantages:**
- Visual and intuitive
- Preset browser
- Progress visualization
- Easier for beginners
- Drag-and-drop support

**Best for:**
- Casual users
- One-off conversions
- Visual feedback needed
- Desktop environments

## Performance Tips

### Speed Up Conversions

1. **Use faster presets**: `--encoding-preset fast`
2. **Lower resolution**: Smaller resolution = faster
3. **Copy when possible**: `--video-codec copy --audio-codec copy`
4. **Use CRF instead of 2-pass**: CRF is single-pass
5. **Close other applications**: Free up CPU

### Reduce File Size

1. **Increase CRF**: Higher CRF = smaller file (e.g., 28)
2. **Lower resolution**: 720p instead of 1080p
3. **Use H.265**: 40% smaller than H.264
4. **Lower bitrate**: Specify lower video/audio bitrate
5. **Use Opus audio**: Better compression than AAC/MP3

### Maximize Quality

1. **Lower CRF**: Use 18-20 for near-lossless
2. **Slow preset**: `--encoding-preset slow`
3. **Higher bitrate**: More data = better quality
4. **Match source resolution**: Don't upscale
5. **Use lossless audio**: FLAC for archival

## Comparing to 123apps

| Feature | Video Converter Pro | 123apps |
|---------|---------------------|---------|
| Local Processing | ✓ Yes | ✗ No (online) |
| File Size Limit | ✓ Unlimited | ✗ Limited |
| Privacy | ✓ Complete | ⚠ Upload required |
| Batch Processing | ✓ Yes | ✗ One at a time |
| CLI/Automation | ✓ Yes | ✗ No |
| Cost | ✓ Free | ⚠ Free with limits |
| Feature Phone Support | ✓ Yes | ✗ No |
| Internet Required | ✗ No | ✓ Yes |
| Speed | ✓ Fast (local) | ⚠ Upload/download time |

## Use Cases

### Personal Video Library
- Archive home videos in high quality
- Organize with consistent format (all MP4)
- Reduce storage with H.265 encoding

### Content Creation
- Prepare videos for YouTube (web_1080p preset)
- Create mobile-friendly versions (mobile_high)
- Extract audio for podcasts

### Sharing with Family
- Convert for older devices (feature_phone presets)
- Reduce size for email/messaging
- Compatible formats for all devices

### Professional Work
- Prepare videos for clients in specific formats
- Batch convert projects
- Maintain quality while meeting size requirements

## FAQ

**Q: How long does conversion take?**
A: Depends on file size, settings, and computer speed. Typically 1-5 minutes for a 5-minute 1080p video.

**Q: Does it work offline?**
A: Yes, completely offline. No internet required.

**Q: Can I convert multiple files?**
A: Yes, use `--batch` for batch processing.

**Q: Will it reduce quality?**
A: Only if you choose to. Use CRF 18-20 or "copy" codec for no quality loss.

**Q: What's the difference between H.264 and H.265?**
A: H.265 provides 40-50% better compression (smaller files) but requires more processing power and newer devices.

**Q: Which preset should I use?**
A: For most uses, `web_720p` is a good balance. Use `--list-presets` to see all options.
