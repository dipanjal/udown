import concurrent.futures
import os
from pathlib import Path

from pytubefix import YouTube  # type: ignore
from pytubefix.cli import on_progress  # type: ignore

from ytdl.profiler import Profiler
from ytdl.utils import Utils

ROOT_DIR = Path(__file__).parent.parent.resolve()
DOWNLOAD_DIR = ROOT_DIR/"downloads"
TEMP_DIR = ROOT_DIR/"temp"


class Downloader:
    def __init__(
        self,
        url: str,
        out_dir: str = str(DOWNLOAD_DIR),
        caption: bool = False,
        debug: bool = False
    ):
        self.url = url
        self.out_dir = out_dir
        self.caption = caption
        self.debug = debug
        self._pre_config()

    def _pre_config(self) -> None:
        self.yt = YouTube(self.url, on_progress_callback=on_progress)
        self.title = Utils.sanitize_filename(self.yt.title)
        self.profiler = Profiler(self.debug)

        # Setting up temp files
        self.temp_video_file: Path = TEMP_DIR / "temp.mp4"
        self.temp_audio_file: Path = TEMP_DIR / "temp.m4a"

        # Create out directory if not exists
        TEMP_DIR.mkdir(exist_ok=True)
        DOWNLOAD_DIR.mkdir(exist_ok=True)
        if self.out_dir != str(DOWNLOAD_DIR):
            Path(self.out_dir).mkdir(exist_ok=True)

    def _cleanup_temps(self) -> None:
        # Clean up temporary files
        Utils.delete_file(self.temp_video_file)
        Utils.delete_file(self.temp_audio_file)

    def _merge_with_ffmpeg(self) -> str:
        self.profiler.start_timer("merging")
        out_file_path: str = os.path.join(
            self.out_dir, f"{self.title}.mp4"
        )
        Utils.merge_with_ffmpeg(
            video_file=str(self.temp_video_file),
            audio_file=str(self.temp_audio_file),
            out_file=out_file_path
        )
        self.profiler.end_timer("merging")
        return out_file_path

    def _download_audio_file(self, file_path: Path) -> None:
        """Download the best audio stream."""
        print("Downloading Audio File")
        self.profiler.start_timer('audio')
        self.yt.streams.filter(
            only_audio=True
        ).order_by("abr").desc().first().download(
            output_path=str(file_path.parent),
            filename=file_path.name
        )
        self.profiler.end_timer('audio')

    def _download_video_file(self, file_path: Path) -> None:
        """Download the best video stream."""
        print("Downloading Video File")
        self.profiler.start_timer('video')
        self.yt.streams.filter(
            only_video=True, file_extension="mp4"
        ).order_by('resolution').desc().first().download(
            output_path=str(file_path.parent),
            filename=file_path.name
        )
        self.profiler.end_timer('video')

    def _download_caption_file(self) -> None:
        caption = self.yt.captions.get("a.en", None)
        if not caption:
            print("No caption found")
            return

        out_file_path: str = os.path.join(
            self.out_dir, f"{self.title}.srt"
        )
        try:
            self.profiler.start_timer('caption')
            print("Downloading Caption File")
            caption.save_captions(out_file_path)
            self.profiler.end_timer('caption')
        except Exception as e:
            print("Unable to download caption file: ", str(e))
            Utils.delete_file(out_file_path)

    def _download(self) -> None:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit video and audio download tasks
            future_video = executor.submit(self._download_video_file, self.temp_video_file)
            future_audio = executor.submit(self._download_audio_file, self.temp_audio_file)

            # Submit caption download task if caption is requested
            futures = [future_video, future_audio]
            if self.caption:
                future_caption = executor.submit(self._download_caption_file)
                futures.append(future_caption)

            # Wait for all downloads to complete
            concurrent.futures.wait(futures)

    def start(self) -> None:
        """Download video and audio, then merge them with FFmpeg."""
        print(f"Downloading: {self.title}")
        self.profiler.start_overall_timer()

        try:
            self._cleanup_temps()
            self._download()
            out_file_path: str = self._merge_with_ffmpeg()
            print(f"Video downloaded successfully to: {out_file_path}")
        except Exception as e:
            print(f"Video downloaded failed due to unknown error: {str(e)}")
        finally:
            self._cleanup_temps()

        self.profiler.end_overall_timer()
        self.profiler.print_report()
