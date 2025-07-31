import os
import subprocess
from pathlib import Path

from pytubefix import YouTube
from pytubefix.cli import on_progress

from ytdl import ROOT_DIR
from ytdl.utils import Utils

DOWNLOAD_DIR = ROOT_DIR/"downloads"
TEMP_DIR = ROOT_DIR/"temp"

class Downloader:
    def __init__(self, url: str, out_dir: str = DOWNLOAD_DIR):
        self.url = url
        self.temp_video_file: Path = TEMP_DIR/"temp.mp4"
        self.temp_audio_file: Path = TEMP_DIR/"temp.m4a"
        self.yt = YouTube(url, on_progress_callback=on_progress)
        self.file_name: str = f"{Utils.sanitize_filename(self.yt.title)}.mp4"
        self.out_file = os.path.join(out_dir, self.file_name)

    def merge_with_ffmpeg(self):
        Utils.merge_with_ffmpeg(
            video_file=str(self.temp_video_file),
            audio_file=str(self.temp_audio_file),
            out_file=self.out_file
        )


    def download_audio_file(self, file_path: Path):
        """Download the best audio stream."""
        self.yt.streams.filter(
            only_audio=True
        ).order_by("abr").desc().first().download(
            output_path=str(file_path.parent),
            filename=file_path.name
        )


    def download_video_file(self, file_path: Path):
        """Download the best video stream."""
        self.yt.streams.filter(
            only_video=True, file_extension="mp4"
        ).order_by('resolution').desc().first().download(
            output_path=str(file_path.parent),
            filename=file_path.name
        )

    def cleanup_temps(self):
        # Clean up temporary files
        if self.temp_video_file.exists():
            os.remove(self.temp_video_file)
        if self.temp_audio_file.exists():
            os.remove(self.temp_audio_file)

    def download(self):
        self.download_video_file(self.temp_video_file)
        self.download_audio_file(self.temp_audio_file)


    def start(self):
        """Download video and audio, then merge them with FFmpeg."""
        print(f"Title: {self.file_name}")
        try:
            self.cleanup_temps()
            self.download()
            self.merge_with_ffmpeg()
        except Exception as e:
            print(e)
        finally:
            self.cleanup_temps()
        print(f"File saved to: {self.out_file}")




if __name__ == "__main__":
    # CLI Mode coming soon
    down = Downloader(
        url="https://www.youtube.com/watch?v=9JPnN1Z_iSY",
    )
    down.start()
