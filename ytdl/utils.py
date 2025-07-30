import re
import subprocess

class Utils:
    @staticmethod
    def sanitize_filename(name: str) -> str:
        """Sanitize a string to be a valid filename."""
        return re.sub(r'[\\/*?:"<>|]', "", name)

    @staticmethod
    def merge_with_ffmpeg(video_file: str, audio_file: str, out_file: str):
        """
        Merge video and audio using ffmpeg via subprocess.
        """
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            out_file
        ]
        print("Running ffmpeg command:", " ".join(cmd))
        subprocess.run(cmd, check=True)
