# You-Down

A fast YouTube video downloader with parallel processing capabilities. Downloads audio and video streams simultaneously for optimal performance.

## Features

- ⚡ **Parallel Processing**: Downloads audio and video streams simultaneously
- 📊 **Performance Profiling**: Detailed timing reports for download operations
- 🎯 **High Quality**: Downloads best available audio and video streams
- 📝 **Caption Support**: Optional subtitle/caption downloads
- 🔧 **FFmpeg Integration**: Automatic audio-video merging
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### From PyPI (Recommended)

```bash
pip install you-down
```

### From Source

```bash
git clone https://github.com/dipanjal/you-down.git
cd you-down
pip install -e .
```

## Prerequisites

- **Python 3.8+**
- **FFmpeg**: Required for audio-video merging

### Installing FFmpeg

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows
Download from [FFmpeg official website](https://ffmpeg.org/download.html) or install via Chocolatey:
```bash
choco install ffmpeg
```

## Usage

### Basic Usage

```bash
you-down <youtube_url>
```

### Advanced Usage

```bash
# Download to custom directory
you-down -o ~/Downloads <youtube_url>

# Download with captions
you-down -c <youtube_url>

# Enable debug mode with detailed timing
you-down -d <youtube_url>

# Combine options
you-down -o ~/Videos -c -d <youtube_url>
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output directory (default: `./downloads`) |
| `-c, --caption` | Download captions/subtitles if available |
| `-d, --debug` | Enable debug mode with detailed timing |
| `--version` | Show version information |
| `-h, --help` | Show help message |

### Examples

```bash
# Download a video
you-down https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Download with captions to Downloads folder
you-down -c -o ~/Downloads https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Debug mode to see performance metrics
you-down -d https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Performance

The parallel processing approach provides significant time savings:

- **Sequential Download**: Audio + Video + Merge = Total Time
- **Parallel Download**: Max(Audio, Video) + Merge = Reduced Time

### Sample Output

```
Downloading: Example Video Title
Downloading Audio File
Downloading Video File
Video downloaded successfully to: ./downloads/Example Video Title.mp4

==================================================
DOWNLOAD PERFORMANCE REPORT
==================================================
Audio Took: 12.34 seconds
Video Took: 15.67 seconds
Merging Took: 2.45 seconds
Expected Duration: 30.46 seconds
Total Process Time: 18.23 seconds
==================================================
Time Saved: 12.23 seconds
==================================================
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/dipanjal/you-down.git
cd you-down
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black ytdl/
```

## Architecture

```
you-down/
├── ytdl/
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Command-line interface
│   ├── downloader.py    # Core download logic
│   ├── profiler.py      # Performance timing
│   └── utils.py         # Utility functions
├── setup.py             # Package setup
├── pyproject.toml       # Modern packaging config
└── README.md           # This file
```

## How It Works

1. **URL Validation**: Validates YouTube URL format
2. **Stream Analysis**: Identifies best audio and video streams
3. **Parallel Downloads**: Downloads audio and video simultaneously
4. **FFmpeg Merge**: Combines streams into final video file
5. **Performance Profiling**: Tracks timing for optimization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [pytubefix](https://github.com/pytubefix/pytubefix) - YouTube data extraction
- [FFmpeg](https://ffmpeg.org/) - Audio/video processing

## Support

- 📧 **Email**: dipanjalmaitra@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/dipanjalmaitra/you-down/issues)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/dipanjalmaitra/you-down/wiki)
