"""
YouTube Downloader CLI
A command-line interface for downloading YouTube videos with parallel processing.
"""

import argparse
import sys
from pathlib import Path

from ytdl.downloader import Downloader


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Download YouTube videos with parallel processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
              %(prog)s https://www.youtube.com/watch?v=dQw4w9WgXcQ
              %(prog)s -o /path/to/downloads https://www.youtube.com/watch?v=dQw4w9WgXcQ
              %(prog)s -c -d https://www.youtube.com/watch?v=dQw4w9WgXcQ
        """
    )
    parser.add_argument(
        "url",
        help="YouTube video URL to download"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_dir",
        help="Output directory for downloaded files (default: ./downloads)"
    )
    parser.add_argument(
        "-c", "--caption",
        action="store_true",
        help="Download captions/subtitles if available"
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug mode with detailed timing information"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    return parser


def validate_url(url: str) -> bool:
    """Validate if the URL is a valid YouTube URL."""
    youtube_domains = [
        "youtube.com",
        "www.youtube.com",
        "youtu.be",
        "m.youtube.com"
    ]

    url_lower = url.lower()
    return any(domain in url_lower for domain in youtube_domains)


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate URL
    if not validate_url(args.url):
        print("Error: Please provide a valid YouTube URL")
        print("Supported formats:")
        print("  - https://www.youtube.com/watch?v=VIDEO_ID")
        print("  - https://youtu.be/VIDEO_ID")
        print("  - https://m.youtube.com/watch?v=VIDEO_ID")
        sys.exit(1)

    # Set output directory
    output_dir = args.output_dir if args.output_dir else "./downloads"

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        # Initialize downloader
        downloader = Downloader(
            url=args.url,
            out_dir=str(output_path),
            caption=args.caption,
            debug=args.debug
        )

        # Start download
        downloader.start()

    except KeyboardInterrupt:
        print("\nDownload cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
