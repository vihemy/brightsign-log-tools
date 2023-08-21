# External modules
import os
import re
import pandas as pd

# Internal modules
from player import Player
from utilities import get_date
from utilities import get_path_from_config
from utilities import create_directory


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
    analyze_logs_and_generate_csv()
        Analyze log files and generate a CSV file with the count of search words in each log file
        as well as the total count of all appearances of the search words.
    """

    def __init__(self, player: Player):
        self.player = player

    def analyze_logs_and_generate_csv(self):
        log_files = self._get_log_files()
        for log_file in log_files:
            log_content = self._read_log_content(log_file)
            df = self._count_searchwords(log_content)
            total_count = sum(df.values())
            self._add_to_df(log_file, total_count, df)
            self.total_count += total_count

        self._write_csv_file()

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

    def _count_searchwords(self, log_content):
        df = {}
        for sw in self.player.searchwords.split(","):
            occurrences = len(re.findall(sw.strip(), log_content, re.IGNORECASE))
            df[sw.strip()] = occurrences
        return df

    def _add_to_df(self, log_file, total_count, df):
        data = {"Log File": log_file, "Total Count": total_count, **df}
        self.df = self.df.append(data, ignore_index=True)

    def _write_csv_file(self):
        csv_filepath = self._create_filepath()
        self.df.to_csv(csv_filepath, index=False)
        print(f"CSV file '{csv_filepath}' generated successfully.")

    def _create_filepath(self):
        player_export_folder = os.path.join(
            get_path_from_config("export_parent_folder"),
            self.player.name + " export",
        )
        create_directory(player_export_folder)
        file_name = f"{self.player.name}_export_{get_date()}.csv"
        file_path = os.path.join(player_export_folder, file_name)
        return file_path
