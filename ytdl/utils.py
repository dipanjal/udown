import re
import subprocess
from pathlib import Path


class Utils:
    @staticmethod
    def sanitize_filename(name: str) -> str:
        """Sanitize a string to be a valid filename."""
        return re.sub(r'[\\/*?:"<>|]', "", name)

    @staticmethod
    def merge_with_ffmpeg(temp_video_path: Path, temp_audio_path: Path, output_path: str):
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
