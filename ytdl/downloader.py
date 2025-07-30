import os
from pathlib import Path

from pytubefix import YouTube
from pytubefix.cli import on_progress

from ytdl import ROOT_DIR
from ytdl.utils import Utils

DOWNLOAD_DIR = ROOT_DIR/"downloads"

def download_audio_file(yt: YouTube, file_path: Path):
    """Download the best audio stream."""
    yt.streams.filter(
        only_audio=True
    ).order_by("abr").desc().first().download(
        output_path=str(file_path.parent),
        filename=file_path.name
    )


def download_video_file(yt: YouTube, file_path: Path):
    """Download the best video stream."""
    yt.streams.filter(
        only_video=True, file_extension="mp4"
    ).order_by('resolution').desc().first().download(
        output_path=str(file_path.parent),
        filename=file_path.name
    )

def main(url: str):
    """Download video and audio, then merge them with FFmpeg."""
    yt = YouTube(url, on_progress_callback=on_progress)
    print(f"Title: {yt.title}")

    sanitized_title = Utils.sanitize_filename(yt.title)

    temp_video_path = DOWNLOAD_DIR / "temp.mp4"
    temp_audio_path = DOWNLOAD_DIR / "temp.m4a"
    output_path = DOWNLOAD_DIR / f"{sanitized_title}.mp4"

    download_video_file(yt, temp_video_path)
    download_audio_file(yt, temp_audio_path)

    # print("Merging Audio and Video Streams")
    Utils.merge_with_ffmpeg(temp_video_path, temp_audio_path, output_path)
    print(f"File saved to: {output_path}")

    # Clean up temporary files
    os.remove(temp_video_path)
    os.remove(temp_audio_path)
    print("Temporary files removed.")


if __name__ == "__main__":
    # CLI Mode coming soon
    main(
        url="https://www.youtube.com/watch?v=cjSjlHUmaBU"
    )