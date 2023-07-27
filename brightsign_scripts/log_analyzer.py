import os
import csv
import re
import pandas as pd

from player import Player


class LogAnalyzer:
    """
    Class to analyze log files and count appearances of search words for a specific player.

    Attributes
    ----------
    player : Player
        an instance of the Player class
    file_directory : str
        the directory containing the log files to analyze

    Methods
    -------
    analyze_logs_and_generate_csv(csv_filename)
        Analyze log files and generate a CSV file with the count of search words in each log file
        as well as the total count of all appearances of the search words.
    """

    def __init__(self, player: Player, file_directory):
        self.player = player
        self.file_directory = file_directory
        self.search_word_counts = pd.DataFrame(
            columns=["Log File", "Total Count"]
            + [word.strip() for word in self.player.searchwords.split(",")]
        )
        self.total_count = 0

    def analyze_logs_and_generate_csv(self, csv_filename):
        log_files = self._get_log_files()
        for log_file in log_files:
            log_content = self._read_log_content(log_file)
            search_word_counts = self._count_search_words(log_content)
            total_count = sum(search_word_counts.values())
            self._add_to_search_word_counts(log_file, total_count, search_word_counts)
            self.total_count += total_count

        self._write_csv_file(csv_filename)

    def _get_log_files(self):
        log_files = [
            filename
            for filename in os.listdir(self.file_directory)
            if filename.endswith(".log")
        ]
        return log_files

    def _read_log_content(self, log_file):
        log_file_path = os.path.join(self.file_directory, log_file)
        with open(log_file_path, "r") as log_file:
            log_content = log_file.read()
        return log_content

    def _count_search_words(self, log_content):
        search_word_counts = {}
        for search_word in self.player.searchwords.split(","):
            occurrences = len(
                re.findall(search_word.strip(), log_content, re.IGNORECASE)
            )
            search_word_counts[search_word.strip()] = occurrences
        return search_word_counts

    def _add_to_search_word_counts(self, log_file, total_count, search_word_counts):
        data = {"Log File": log_file, "Total Count": total_count, **search_word_counts}
        self.search_word_counts = self.search_word_counts.append(
            data, ignore_index=True
        )

    def _write_csv_file(self, csv_filename):
        self.search_word_counts.to_csv(csv_filename, index=False)
        print(f"CSV file '{csv_filename}' generated successfully.")
