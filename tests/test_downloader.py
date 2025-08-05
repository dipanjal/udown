"""
Tests for the you-down package
"""
from pathlib import Path
from unittest.mock import Mock, patch

from ytdl.downloader import Downloader
from ytdl.profiler import Profiler
from ytdl.utils import Utils


class TestProfiler:
    """
    Test the Profiler class.
    """
    def test_profiler_initialization(self) -> None:
        """
        Test profiler initialization.
        """
        profiler = Profiler(debug=True)
        assert profiler.debug is True
        assert not profiler.timings
        assert profiler.start_time is None

    def test_timer_functions(self) -> None:
        """
        Test timer start and end functions.
        """
        profiler = Profiler()
        profiler.start_timer("test")
        assert "test" in profiler.timings
        assert "start" in profiler.timings["test"]
        
        profiler.end_timer("test")
        assert "end" in profiler.timings["test"]
        assert "duration" in profiler.timings["test"]

    def test_overall_timer(self) -> None:
        """
        Test overall timer functionality.
        """
        profiler = Profiler()
        profiler.start_overall_timer()
        assert profiler.start_time is not None

        profiler.end_overall_timer()
        assert "total" in profiler.timings
        assert "duration" in profiler.timings["total"]


class TestUtils:
    """
    Test the Utils class.
    """
    def test_sanitize_filename(self) -> None:
        """
        Test filename sanitization.
        """
        # Test with invalid characters
        invalid_name = "file/name\\with*invalid?chars:"
        sanitized = Utils.sanitize_filename(invalid_name)
        assert sanitized == "filenamewithinvalidchars"

        # Test with valid name
        valid_name = "valid_filename_123"
        sanitized = Utils.sanitize_filename(valid_name)
        assert sanitized == valid_name

    def test_delete_file(self, tmp_path: Path) -> None:
        """
        Test file deletion.
        """
        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()

        # Delete the file
        Utils.delete_file(test_file)
        assert not test_file.exists()

        # Test deleting non-existent file (should not raise error)
        Utils.delete_file(tmp_path / "nonexistent.txt")


class TestDownloader:
    """
    Test the Downloader class.
    """
    @patch('ytdl.downloader.YouTube')
    def test_downloader_initialization(self, mock_youtube: Mock) -> None:
        """
        Test downloader initialization.
        """
        # Mock YouTube object
        mock_yt = Mock()
        mock_yt.title = "Test Video"
        mock_youtube.return_value = mock_yt

        downloader = Downloader(
            url="https://www.youtube.com/watch?v=test",
            caption=True,
            debug=True
        )

        assert downloader.url == "https://www.youtube.com/watch?v=test"
        assert downloader.caption is True
        assert downloader.debug is True
        assert downloader.title == "Test Video"
        assert downloader.profiler.debug is True
