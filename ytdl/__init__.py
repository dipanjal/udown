"""
YouTube Downloader with Parallel Processing
A fast YouTube video downloader that downloads audio and video streams in parallel.
"""

from .downloader import Downloader
from .profiler import Profiler
from .utils import Utils

__version__ = "1.0.0"
__all__ = ["Downloader", "Profiler", "Utils"]
