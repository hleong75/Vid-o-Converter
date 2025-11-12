"""
Core video converter module using FFmpeg
"""

import os
import subprocess
import json
from typing import Optional, Dict, Any, Callable
from pathlib import Path
import shutil


class VideoConverter:
    """Main video converter class using FFmpeg"""
    
    def __init__(self):
        """Initialize the video converter"""
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        if not shutil.which('ffmpeg'):
            raise RuntimeError(
                "FFmpeg is not installed or not in PATH. "
                "Please install FFmpeg from https://ffmpeg.org/"
            )
    
    def get_video_info(self, input_file: str) -> Dict[str, Any]:
        """Get video information using ffprobe"""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            input_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get video info: {e}")
    
    def convert(
        self,
        input_file: str,
        output_file: str,
        video_codec: Optional[str] = None,
        audio_codec: Optional[str] = None,
        video_bitrate: Optional[str] = None,
        audio_bitrate: Optional[str] = None,
        resolution: Optional[str] = None,
        fps: Optional[int] = None,
        crf: Optional[int] = None,
        preset: Optional[str] = None,
        start_time: Optional[str] = None,
        duration: Optional[str] = None,
        audio_sample_rate: Optional[int] = None,
        additional_params: Optional[Dict[str, str]] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
        overwrite: bool = True
    ) -> bool:
        """
        Convert video with specified parameters
        
        Args:
            input_file: Path to input video file
            output_file: Path to output video file
            video_codec: Video codec (e.g., 'libx264', 'libx265', 'libvpx-vp9')
            audio_codec: Audio codec (e.g., 'aac', 'libmp3lame', 'libopus')
            video_bitrate: Video bitrate (e.g., '2000k', '5M')
            audio_bitrate: Audio bitrate (e.g., '128k', '192k')
            resolution: Output resolution (e.g., '1920x1080', '1280x720')
            fps: Frame rate
            crf: Constant Rate Factor (0-51, lower is better quality)
            preset: Encoding preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
            start_time: Start time for trimming (e.g., '00:00:10')
            duration: Duration for trimming (e.g., '00:00:30')
            audio_sample_rate: Audio sample rate (e.g., 44100, 48000)
            additional_params: Additional FFmpeg parameters
            progress_callback: Callback function for progress updates (0.0 to 1.0)
            overwrite: Whether to overwrite existing output file
            
        Returns:
            bool: True if conversion was successful
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Build FFmpeg command
        cmd = ['ffmpeg']
        
        # Overwrite option
        if overwrite:
            cmd.append('-y')
        else:
            cmd.append('-n')
        
        # Input file
        cmd.extend(['-i', input_file])
        
        # Trimming options
        if start_time:
            cmd.extend(['-ss', start_time])
        if duration:
            cmd.extend(['-t', duration])
        
        # Video codec
        if video_codec:
            cmd.extend(['-c:v', video_codec])
        
        # Audio codec
        if audio_codec:
            cmd.extend(['-c:a', audio_codec])
        elif video_codec and video_codec != 'copy':
            # If we're encoding video but audio codec not specified, copy audio
            cmd.extend(['-c:a', 'copy'])
        
        # Video bitrate
        if video_bitrate:
            cmd.extend(['-b:v', video_bitrate])
        
        # Audio bitrate
        if audio_bitrate:
            cmd.extend(['-b:a', audio_bitrate])
        
        # Resolution
        if resolution:
            cmd.extend(['-s', resolution])
        
        # Frame rate
        if fps:
            cmd.extend(['-r', str(fps)])
        
        # CRF (quality)
        if crf is not None:
            cmd.extend(['-crf', str(crf)])
        
        # Encoding preset
        if preset:
            cmd.extend(['-preset', preset])
        
        # Audio sample rate
        if audio_sample_rate:
            cmd.extend(['-ar', str(audio_sample_rate)])
        
        # Additional parameters
        if additional_params:
            for key, value in additional_params.items():
                cmd.extend([f'-{key}', str(value)])
        
        # Progress reporting
        cmd.extend(['-progress', 'pipe:1'])
        cmd.extend(['-stats_period', '0.5'])
        
        # Output file
        cmd.append(output_file)
        
        # Get total duration for progress calculation
        total_duration = None
        if progress_callback:
            try:
                info = self.get_video_info(input_file)
                if 'format' in info and 'duration' in info['format']:
                    total_duration = float(info['format']['duration'])
            except:
                pass
        
        # Execute conversion
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor progress
            current_time = 0.0
            for line in process.stdout:
                line = line.strip()
                if line.startswith('out_time_ms='):
                    try:
                        microseconds = int(line.split('=')[1])
                        current_time = microseconds / 1000000.0
                        
                        if progress_callback and total_duration and total_duration > 0:
                            progress = min(current_time / total_duration, 1.0)
                            progress_callback(progress)
                    except (ValueError, IndexError):
                        pass
            
            process.wait()
            
            if process.returncode != 0:
                stderr = process.stderr.read() if process.stderr else ""
                raise RuntimeError(f"FFmpeg conversion failed: {stderr}")
            
            # Final progress update
            if progress_callback:
                progress_callback(1.0)
            
            return True
            
        except Exception as e:
            raise RuntimeError(f"Conversion failed: {str(e)}")
    
    def extract_audio(
        self,
        input_file: str,
        output_file: str,
        audio_codec: str = 'libmp3lame',
        audio_bitrate: str = '192k',
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        """
        Extract audio from video
        
        Args:
            input_file: Path to input video file
            output_file: Path to output audio file
            audio_codec: Audio codec
            audio_bitrate: Audio bitrate
            progress_callback: Callback function for progress updates
            
        Returns:
            bool: True if extraction was successful
        """
        return self.convert(
            input_file=input_file,
            output_file=output_file,
            video_codec=None,  # No video
            audio_codec=audio_codec,
            audio_bitrate=audio_bitrate,
            progress_callback=progress_callback
        )
    
    def change_container(
        self,
        input_file: str,
        output_file: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        """
        Change video container format without re-encoding
        
        Args:
            input_file: Path to input video file
            output_file: Path to output video file
            progress_callback: Callback function for progress updates
            
        Returns:
            bool: True if conversion was successful
        """
        return self.convert(
            input_file=input_file,
            output_file=output_file,
            video_codec='copy',
            audio_codec='copy',
            progress_callback=progress_callback
        )
    
    def trim_video(
        self,
        input_file: str,
        output_file: str,
        start_time: str,
        duration: Optional[str] = None,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        """
        Trim video to specified time range
        
        Args:
            input_file: Path to input video file
            output_file: Path to output video file
            start_time: Start time (e.g., '00:00:10' or '10')
            duration: Duration (e.g., '00:00:30' or '30')
            progress_callback: Callback function for progress updates
            
        Returns:
            bool: True if trimming was successful
        """
        return self.convert(
            input_file=input_file,
            output_file=output_file,
            video_codec='copy',
            audio_codec='copy',
            start_time=start_time,
            duration=duration,
            progress_callback=progress_callback
        )
    
    def convert_with_preset(
        self,
        input_file: str,
        output_file: str,
        preset_params: Dict[str, Any],
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        """
        Convert video using preset parameters
        
        Args:
            input_file: Path to input video file
            output_file: Path to output video file
            preset_params: Preset parameters dictionary
            progress_callback: Callback function for progress updates
            
        Returns:
            bool: True if conversion was successful
        """
        # Extract parameters from preset
        kwargs = {
            'input_file': input_file,
            'output_file': output_file,
            'progress_callback': progress_callback
        }
        
        # Map preset parameters to convert method parameters
        param_mapping = {
            'vcodec': 'video_codec',
            'acodec': 'audio_codec',
            'video_bitrate': 'video_bitrate',
            'audio_bitrate': 'audio_bitrate',
            'r': 'fps',
            'crf': 'crf',
            'preset': 'preset',
            'ar': 'audio_sample_rate'
        }
        
        for preset_key, convert_key in param_mapping.items():
            if preset_key in preset_params:
                value = preset_params[preset_key]
                # Convert string numbers to int where needed
                if convert_key in ['fps', 'crf', 'audio_sample_rate']:
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        pass
                kwargs[convert_key] = value
        
        return self.convert(**kwargs)
