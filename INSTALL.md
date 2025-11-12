# Installation Guide

## Prerequisites

### 1. Python
This application requires Python 3.7 or higher.

Check your Python version:
```bash
python3 --version
```

If you don't have Python installed:
- **Ubuntu/Debian**: `sudo apt install python3 python3-pip`
- **macOS**: `brew install python3` or download from [python.org](https://www.python.org/)
- **Windows**: Download from [python.org](https://www.python.org/)

### 2. FFmpeg (Required for video conversion)

FFmpeg is the core engine that powers video conversion. It must be installed separately.

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS
Using Homebrew:
```bash
brew install ffmpeg
```

#### Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add the `bin` folder to your system PATH:
   - Right-click "This PC" → Properties → Advanced system settings
   - Environment Variables → System Variables → Path → Edit
   - Add `C:\ffmpeg\bin` (or your installation path)

#### Verify FFmpeg Installation
```bash
ffmpeg -version
```

### 3. Tkinter (For GUI)
Tkinter is included with most Python installations, but on some Linux systems it needs to be installed separately.

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

## Installing Video Converter

### Method 1: From Source (Recommended for Development)

1. Clone the repository:
```bash
git clone https://github.com/hleong75/Vid-o-Converter.git
cd Vid-o-Converter
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Install the package in development mode:
```bash
pip3 install -e .
```

### Method 2: Direct Installation

```bash
pip3 install -r requirements.txt
python3 setup.py install
```

## Verifying Installation

### Test the CLI
```bash
videoconv --help
videoconv --list-presets
```

### Test the GUI
```bash
videoconv-gui
```

### Run Package Tests
```bash
python3 test_package.py
```

## Troubleshooting

### "videoconv: command not found"
The package isn't installed or the Python scripts directory isn't in your PATH.

**Solution:**
```bash
# Reinstall with pip
pip3 install -e .

# Or add to PATH (Linux/macOS)
export PATH="$HOME/.local/bin:$PATH"

# Or run directly with Python
python3 -m videoconverter.cli --help
```

### "FFmpeg is not installed"
FFmpeg is required but not found in your system PATH.

**Solution:**
1. Install FFmpeg (see instructions above)
2. Verify: `ffmpeg -version`
3. Ensure FFmpeg is in your system PATH

### "No module named 'tkinter'"
The GUI requires tkinter which isn't installed.

**Solution (Ubuntu/Debian):**
```bash
sudo apt install python3-tk
```

The CLI will still work without tkinter.

### Permission Errors
You don't have permission to write to the output directory.

**Solution:**
- Specify a different output directory with `-o` or `--output-dir`
- Or use `sudo` (not recommended for regular use)
- Or change the output directory permissions

### Slow Conversion
Video conversion is CPU-intensive and can be slow on older hardware.

**Tips to speed up:**
- Use faster presets: `--encoding-preset fast` or `ultrafast`
- Use GPU acceleration (requires FFmpeg with GPU support)
- Lower the output quality or resolution
- Close other applications

## Uninstallation

```bash
pip3 uninstall video-converter
```

## Getting Help

If you encounter issues:
1. Check the [README.md](README.md) for usage examples
2. Run `videoconv --help` for CLI options
3. Check that FFmpeg is properly installed: `ffmpeg -version`
4. Review the [Troubleshooting](#troubleshooting) section above
5. Open an issue on GitHub with:
   - Your operating system and version
   - Python version: `python3 --version`
   - FFmpeg version: `ffmpeg -version`
   - The command you ran and the error message
