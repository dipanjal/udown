import os
import re
import subprocess
from pathlib import Path

from pytubefix import YouTube, Stream
from pytubefix.cli import on_progress

from ytdl import ROOT_DIR

DOWNLOAD_DIR = ROOT_DIR/"downloads"

def merge_with_ffmpeg(temp_video_path, temp_audio_path, output_path):
    """
    Merge video and audio using ffmpeg via subprocess.
    """
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output file if it exists
        "-i", str(temp_video_path),
        "-i", str(temp_audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        str(output_path)
    ]
    print("Running ffmpeg command:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def sanitize_filename(name: str) -> str:
    """Sanitize a string to be a valid filename."""
    return re.sub(r'[\\/*?:"<>|]', "", name)


def save(stream: Stream, file_path: Path):
    """Download a stream to a given path."""
    print(f"Downloading to: {file_path.name}")
    stream.download(
        output_path=str(file_path.parent),
        filename=file_path.name
    )
    print(f"Finished downloading: {file_path.name}")


def download_audio_file(yt: YouTube, file_path: Path):
    """Download the best audio stream."""
    audio_stream = yt.streams.filter(
        only_audio=True
    ).order_by("abr").desc().first()
    save(audio_stream, file_path)


def download_video_file(yt: YouTube, file_path: Path):
    """Download the best video stream."""
    video_stream = yt.streams.filter(
        only_video=True, file_extension="mp4"
    ).order_by('resolution').desc().first()
    save(video_stream, file_path)

def main(url: str):
    """Download video and audio, then merge them with FFmpeg."""
    yt = YouTube(url, on_progress_callback=on_progress)
    print(f"Title: {yt.title}")

    sanitized_title = sanitize_filename(yt.title)

    temp_video_path = DOWNLOAD_DIR / "temp.mp4"
    temp_audio_path = DOWNLOAD_DIR / "temp.m4a"
    output_path = DOWNLOAD_DIR / f"{sanitized_title}.mp4"

    download_video_file(yt, temp_video_path)
    download_audio_file(yt, temp_audio_path)

    print("Merging Audio and Video Streams")
    merge_with_ffmpeg(temp_video_path, temp_audio_path, output_path)
    print(f"Successfully merged video and audio to: {output_path}")

    # Clean up temporary files
    os.remove(temp_video_path)
    os.remove(temp_audio_path)
    print("Temporary files removed.")


if __name__ == "__main__":
    # CLI Mode coming soon
    main(
        url="https://www.youtube.com/watch?v=djV11Xbc914"
    )