#!/usr/bin/env python3
"""
Command-line interface for Video Converter
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional
from tqdm import tqdm

from .converter import VideoConverter
from .presets import get_preset, list_presets, get_presets_by_category


class ProgressBar:
    """Progress bar handler for CLI"""
    
    def __init__(self, desc: str = "Converting"):
        self.pbar = tqdm(total=100, desc=desc, unit='%', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}%')
        self.last_value = 0
    
    def update(self, progress: float):
        """Update progress bar"""
        current = int(progress * 100)
        if current > self.last_value:
            self.pbar.update(current - self.last_value)
            self.last_value = current
    
    def close(self):
        """Close progress bar"""
        self.pbar.close()


def list_available_presets():
    """List all available presets"""
    print("\n=== Available Conversion Presets ===\n")
    
    categories = get_presets_by_category()
    for category, presets in categories.items():
        print(f"{category}:")
        for preset in presets:
            print(f"  - {preset.name}")
            print(f"    {preset.description}")
        print()


def convert_video(args):
    """Convert video with specified parameters"""
    converter = VideoConverter()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    
    # Determine output file
    output_file = args.output
    if not output_file:
        input_path = Path(args.input)
        if args.preset:
            preset = get_preset(args.preset)
            if preset and preset.container:
                ext = preset.container
            else:
                ext = 'mp4'
        elif args.format:
            ext = args.format
        else:
            ext = 'mp4'
        
        output_file = str(input_path.parent / f"{input_path.stem}_converted.{ext}")
    
    print(f"Input: {args.input}")
    print(f"Output: {output_file}")
    
    try:
        # Show video info if requested
        if args.info:
            print("\n=== Video Information ===")
            info = converter.get_video_info(args.input)
            
            # Display format info
            if 'format' in info:
                fmt = info['format']
                print(f"\nFormat: {fmt.get('format_name', 'unknown')}")
                print(f"Duration: {float(fmt.get('duration', 0)):.2f} seconds")
                print(f"Size: {int(fmt.get('size', 0)) / (1024*1024):.2f} MB")
                print(f"Bitrate: {int(fmt.get('bit_rate', 0)) / 1000:.0f} kbps")
            
            # Display stream info
            if 'streams' in info:
                for stream in info['streams']:
                    codec_type = stream.get('codec_type', 'unknown')
                    if codec_type == 'video':
                        print(f"\nVideo Stream:")
                        print(f"  Codec: {stream.get('codec_name', 'unknown')}")
                        print(f"  Resolution: {stream.get('width', 0)}x{stream.get('height', 0)}")
                        print(f"  FPS: {eval(stream.get('r_frame_rate', '0/1')):.2f}")
                        print(f"  Bitrate: {int(stream.get('bit_rate', 0)) / 1000:.0f} kbps")
                    elif codec_type == 'audio':
                        print(f"\nAudio Stream:")
                        print(f"  Codec: {stream.get('codec_name', 'unknown')}")
                        print(f"  Sample Rate: {stream.get('sample_rate', 'unknown')} Hz")
                        print(f"  Channels: {stream.get('channels', 'unknown')}")
                        print(f"  Bitrate: {int(stream.get('bit_rate', 0)) / 1000:.0f} kbps")
            
            print()
            if not args.convert:
                return 0
        
        # Prepare conversion parameters
        progress_bar = ProgressBar(desc=f"Converting {Path(args.input).name}")
        
        if args.preset:
            # Use preset
            preset = get_preset(args.preset)
            if not preset:
                print(f"Error: Preset '{args.preset}' not found", file=sys.stderr)
                print("Use --list-presets to see available presets", file=sys.stderr)
                return 1
            
            print(f"\nUsing preset: {preset.name}")
            print(f"Description: {preset.description}\n")
            
            # Determine output extension from preset
            if preset.container and not args.output:
                input_path = Path(args.input)
                output_file = str(input_path.parent / f"{input_path.stem}_converted.{preset.container}")
            
            success = converter.convert_with_preset(
                input_file=args.input,
                output_file=output_file,
                preset_params=preset.to_ffmpeg_params(),
                progress_callback=progress_bar.update
            )
        else:
            # Use manual parameters
            success = converter.convert(
                input_file=args.input,
                output_file=output_file,
                video_codec=args.video_codec,
                audio_codec=args.audio_codec,
                video_bitrate=args.video_bitrate,
                audio_bitrate=args.audio_bitrate,
                resolution=args.resolution,
                fps=args.fps,
                crf=args.crf,
                preset=args.encoding_preset,
                start_time=args.start_time,
                duration=args.duration,
                audio_sample_rate=args.audio_sample_rate,
                progress_callback=progress_bar.update,
                overwrite=not args.no_overwrite
            )
        
        progress_bar.close()
        
        if success:
            output_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"\n✓ Conversion successful!")
            print(f"Output file: {output_file}")
            print(f"Output size: {output_size:.2f} MB")
            return 0
        else:
            print("\n✗ Conversion failed!", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        return 1


def batch_convert(args):
    """Batch convert multiple videos"""
    converter = VideoConverter()
    
    # Get input files
    input_files = []
    for pattern in args.inputs:
        if os.path.isfile(pattern):
            input_files.append(pattern)
        elif os.path.isdir(pattern):
            # Get all video files in directory
            path = Path(pattern)
            for ext in ['*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv', '*.flv', '*.webm', '*.m4v']:
                input_files.extend([str(f) for f in path.glob(ext)])
        else:
            # Try glob pattern
            from glob import glob
            input_files.extend(glob(pattern))
    
    if not input_files:
        print("Error: No input files found", file=sys.stderr)
        return 1
    
    print(f"Found {len(input_files)} files to convert")
    
    # Create output directory
    output_dir = args.output_dir or "converted"
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert each file
    successful = 0
    failed = 0
    
    for i, input_file in enumerate(input_files, 1):
        print(f"\n[{i}/{len(input_files)}] Processing: {input_file}")
        
        # Determine output file
        input_path = Path(input_file)
        if args.preset:
            preset = get_preset(args.preset)
            ext = preset.container if preset and preset.container else 'mp4'
        elif args.format:
            ext = args.format
        else:
            ext = input_path.suffix[1:] or 'mp4'
        
        output_file = os.path.join(output_dir, f"{input_path.stem}.{ext}")
        
        try:
            progress_bar = ProgressBar(desc=f"Converting {input_path.name}")
            
            if args.preset:
                preset = get_preset(args.preset)
                success = converter.convert_with_preset(
                    input_file=input_file,
                    output_file=output_file,
                    preset_params=preset.to_ffmpeg_params(),
                    progress_callback=progress_bar.update
                )
            else:
                success = converter.convert(
                    input_file=input_file,
                    output_file=output_file,
                    video_codec=args.video_codec,
                    audio_codec=args.audio_codec,
                    video_bitrate=args.video_bitrate,
                    audio_bitrate=args.audio_bitrate,
                    resolution=args.resolution,
                    fps=args.fps,
                    crf=args.crf,
                    preset=args.encoding_preset,
                    progress_callback=progress_bar.update,
                    overwrite=True
                )
            
            progress_bar.close()
            
            if success:
                print(f"✓ Converted: {output_file}")
                successful += 1
            else:
                print(f"✗ Failed: {input_file}")
                failed += 1
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            failed += 1
    
    print(f"\n=== Batch Conversion Complete ===")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(input_files)}")
    
    return 0 if failed == 0 else 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Professional Video Converter - Convert videos to different formats and codecs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert using preset
  videoconv -i input.mp4 -p web_720p
  
  # Convert with custom settings
  videoconv -i input.mp4 -o output.mp4 --video-codec libx264 --crf 23
  
  # Extract audio
  videoconv -i input.mp4 -p audio_mp3_high
  
  # Trim video
  videoconv -i input.mp4 -o trimmed.mp4 --start-time 00:00:10 --duration 00:00:30
  
  # Batch convert
  videoconv --batch *.mp4 -p mobile_standard --output-dir converted
  
  # Feature phone optimization
  videoconv -i input.mp4 -p feature_phone_standard
  
  # Get video info
  videoconv -i input.mp4 --info
        """
    )
    
    # Input/Output
    parser.add_argument('-i', '--input', help='Input video file')
    parser.add_argument('-o', '--output', help='Output video file')
    parser.add_argument('-f', '--format', help='Output format/container (mp4, mkv, avi, webm, etc.)')
    
    # Preset
    parser.add_argument('-p', '--preset', help='Conversion preset (use --list-presets to see options)')
    parser.add_argument('--list-presets', action='store_true', help='List all available presets')
    
    # Video options
    parser.add_argument('--video-codec', help='Video codec (libx264, libx265, libvpx-vp9, etc.)')
    parser.add_argument('--video-bitrate', help='Video bitrate (e.g., 2000k, 5M)')
    parser.add_argument('--resolution', help='Output resolution (e.g., 1920x1080, 1280x720)')
    parser.add_argument('--fps', type=int, help='Frame rate')
    parser.add_argument('--crf', type=int, help='Constant Rate Factor (0-51, lower is better)')
    parser.add_argument('--encoding-preset', help='Encoding speed preset (ultrafast to veryslow)')
    
    # Audio options
    parser.add_argument('--audio-codec', help='Audio codec (aac, libmp3lame, libopus, etc.)')
    parser.add_argument('--audio-bitrate', help='Audio bitrate (e.g., 128k, 192k)')
    parser.add_argument('--audio-sample-rate', type=int, help='Audio sample rate (e.g., 44100, 48000)')
    
    # Trimming options
    parser.add_argument('--start-time', help='Start time for trimming (e.g., 00:00:10)')
    parser.add_argument('--duration', help='Duration for trimming (e.g., 00:00:30)')
    
    # Batch processing
    parser.add_argument('--batch', nargs='+', dest='inputs', help='Batch process multiple files/directories')
    parser.add_argument('--output-dir', help='Output directory for batch processing')
    
    # Other options
    parser.add_argument('--info', action='store_true', help='Show video information')
    parser.add_argument('--convert', action='store_true', help='Convert after showing info')
    parser.add_argument('--no-overwrite', action='store_true', help='Do not overwrite existing files')
    
    args = parser.parse_args()
    
    # Handle list presets
    if args.list_presets:
        list_available_presets()
        return 0
    
    # Handle batch processing
    if args.inputs:
        return batch_convert(args)
    
    # Handle single file conversion
    if not args.input:
        parser.print_help()
        return 1
    
    return convert_video(args)


if __name__ == '__main__':
    sys.exit(main())
