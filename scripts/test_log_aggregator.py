import unittest
from unittest.mock import patch, mock_open, MagicMock

from log_aggregator import (
    get_processed_files,
    extract_info_from_filename,
    parse_log_file,
    update_processed_files,
    main,
    process_playback_log,
    process_event_log,
    process_state_log,
)


class TestFileOperations(unittest.TestCase):
    """Test cases related to file operations like reading and updating processed files."""

    def test_get_processed_files_exists(self):
        """Test the retrieval of processed file names from an existing file."""
        mock_data = "file1.log\nfile2.log\n"
        with patch("os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=mock_data)
        ):
            result = get_processed_files("dummy.log")
            self.assertEqual(result, {"file1.log", "file2.log"})

    def test_get_processed_files_not_exists(self):
        """Test the behavior when the processed files log does not exist."""
        with patch("os.path.exists", return_value=False):
            result = get_processed_files("dummy.log")
            self.assertEqual(result, set())

    def test_update_processed_files(self):
        """Test updating the list of processed files with a new entry."""
        with patch("builtins.open", mock_open()) as mocked_file:
            update_processed_files("processed.log", "newfile.log")
            mocked_file.assert_called_once_with("processed.log", "a")
            mocked_file().write.assert_called_once_with("newfile.log\n")


class TestFilenameExtraction(unittest.TestCase):
    """Tests for extracting information from filenames using regex patterns."""

    def test_extract_info_from_filename_valid(self):
        """Test successful extraction of player serial number and date from valid filenames."""
        self.assertEqual(
            extract_info_from_filename("BrightSignLog.46D98V000729-22081900.log"),
            ("46D98V000729", "220819"),
        )
        self.assertEqual(
            extract_info_from_filename(
                "sd_logs_BrightSignLog.46D98C000712-220908001.log"
            ),
            ("46D98C000712", "220908"),
        )

    def test_extract_info_from_filename_invalid(self):
        """Test extraction attempt from an incorrectly formatted filename."""
        self.assertEqual(
            extract_info_from_filename("incorrect_log_format.log"), (None, None)
        )


class TestLogParsing(unittest.TestCase):
    """Tests focused on parsing different types of log data."""

    def test_parse_log_file_valid_pattern(self):
        """Ensure that valid log files are properly parsed and processed."""
        file_path = "path/to/BrightSignLog.46D98C000712-220823000.log"
        log_data = "L=p\tZ=Zone 1\tS=2022/08/23 10:28:21.435\tE=2022/08/23 11:47:51.559\tI=audio\tN=Silence_stilhed.wav"
        with patch(
            "os.path.basename", return_value="BrightSignLog.46D98C000712-220823000.log"
        ), patch("builtins.open", mock_open(read_data=log_data)), patch(
            "csv.DictWriter"
        ) as mock_writer:
            writer = MagicMock()
            mock_writer.return_value = writer
            parse_log_file(file_path, writer)
            writer.writerow.assert_called_once()

    def test_parse_log_file_invalid_pattern(self):
        """Verify that files not matching the expected log format are skipped."""
        file_path = "path/to/invalid_filename.log"
        with patch("os.path.basename", return_value="invalid_filename.log"), patch(
            "builtins.open", mock_open(read_data="")
        ), patch("csv.DictWriter") as mock_writer:
            writer = MagicMock()
            mock_writer.return_value = writer
            parse_log_file(file_path, writer)
            writer.writerow.assert_not_called()


class TestLogProcessing(unittest.TestCase):
    """Testing the specific log processing functions that write data to CSV files."""

    def test_process_playback_log(self):
        """Test processing of playback log data."""
        mock_writer = MagicMock()
        line = "L=p\tZ=Zone 2\tS=2023/08/29 10:13:58.547\tE=2023/08/29 10:14:06.030\tI=image\tN=Hajtank Touchskærm74.jpg"
        process_playback_log(line, mock_writer, "serial123", "290823")
        expected_data = {
            "PlayerSerialNumber": "serial123",
            "LogType": "Playback",
            "Timestamp": "2023/08/29 10:13:58.547",
            "ZoneName": "Zone 2",
            "StartTime": "2023/08/29 10:13:58.547",
            "EndTime": "2023/08/29 10:14:06.030",
            "ContentType": "image",
            "ContentName": "Hajtank Touchskærm74.jpg",
        }
        mock_writer.writerow.assert_called_once_with(expected_data)

    def test_process_event_log(self):
        """Test processing of event log data."""
        mock_writer = MagicMock()
        line = "L=e\tS=Lyttestation_20.05_DA.wav\tT=2023/07/19 10:00:04.317\tE=serial\tD=2 X001A[5]\tA=1"
        process_event_log(line, mock_writer, "serial123", "190723")
        expected_data = {
            "PlayerSerialNumber": "serial123",
            "LogType": "Event",
            "Timestamp": "2023/07/19 10:00:04.317",
            "StateName": "Lyttestation_20.05_DA.wav",
            "EventType": "serial",
            "EventData": "2 X001A[5]",
        }
        mock_writer.writerow.assert_called_once_with(expected_data)

    def test_process_state_log(self):
        """Test processing of state log data with actual log entry."""
        mock_writer = MagicMock()
        line = "L=s\tS=Teknik i anlæg_1.mp4\tT=2022/08/22 11:53:04.385\tY=video\tLS=Karsten Idle_1.mp4\tLE=touch\tLD= 2"
        process_state_log(line, mock_writer, "serial123", "220822")
        expected_data = {
            "PlayerSerialNumber": "serial123",
            "LogType": "State",
            "Timestamp": "2022/08/22 11:53:04.385",
            "StateName": "Teknik i anlæg_1.mp4",
            "StateType": "video",
            "PreviousState": "Karsten Idle_1.mp4",
            "PreviousEventType": "touch",
            "PreviousEventData": "2",
        }
        mock_writer.writerow.assert_called_once_with(expected_data)


class TestIntegration(unittest.TestCase):
    """Integration tests that simulate the entire process flow of log parsing and file updating."""

    def test_main_integration(self):
        """Test the main function with a simulated directory structure and files."""
        with patch(
            "os.walk", return_value=[("path", [], ["file1.log", "file2.log"])]
        ), patch("os.path.join", side_effect=lambda x, y: f"{x}/{y}"), patch(
            "builtins.open", mock_open()
        ), patch(
            "csv.DictWriter"
        ), patch(
            "os.stat"
        ) as mock_stat:
            mock_stat.return_value.st_size = 0  # Simulate empty file
            main("dummy_dir", "output.csv", "processed.log")


if __name__ == "__main__":
    unittest.main()
