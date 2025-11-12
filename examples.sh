#!/bin/bash
# Example script showing various CLI usage patterns

echo "=== Video Converter CLI Examples ==="
echo

# Check if videoconv is available
if ! command -v videoconv &> /dev/null; then
    echo "Error: videoconv command not found"
    echo "Please install the package first: pip install -e ."
    exit 1
fi

# Example 1: List presets
echo "1. Listing available presets:"
videoconv --list-presets
echo

# Example 2: Get video information (requires actual video file)
# echo "2. Getting video information:"
# videoconv -i input.mp4 --info
# echo

# Example 3: Convert using web preset
echo "3. Example command for web conversion (720p):"
echo "   videoconv -i input.mp4 -p web_720p"
echo

# Example 4: Feature phone conversion
echo "4. Example command for feature phone conversion:"
echo "   videoconv -i input.mp4 -p feature_phone_standard"
echo

# Example 5: Audio extraction
echo "5. Example command for audio extraction (MP3):"
echo "   videoconv -i input.mp4 -p audio_mp3_high"
echo

# Example 6: Batch conversion
echo "6. Example command for batch conversion:"
echo "   videoconv --batch *.mp4 -p mobile_standard --output-dir converted"
echo

# Example 7: Custom settings
echo "7. Example command with custom settings:"
echo "   videoconv -i input.mp4 -o output.mp4 \\"
echo "     --video-codec libx264 \\"
echo "     --audio-codec aac \\"
echo "     --resolution 1280x720 \\"
echo "     --video-bitrate 2000k \\"
echo "     --audio-bitrate 128k \\"
echo "     --crf 23"
echo

# Example 8: Video trimming
echo "8. Example command for video trimming:"
echo "   videoconv -i input.mp4 -o trimmed.mp4 \\"
echo "     --start-time 00:00:10 \\"
echo "     --duration 00:00:30"
echo

echo "=== Examples Complete ==="
echo
echo "Note: These are example commands. You'll need actual video files to run them."
echo "FFmpeg must be installed for conversions to work."
