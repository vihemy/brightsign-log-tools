# External modules
import os
import re
import pandas as pd

# Internal modules
from player import Player
from utilities import get_date2, get_data_from_config, create_directory


class LogAnalyzer:
    def __init__(self, player: Player):
        self.player = player
        self.log_parent_dir = get_data_from_config("file_paths", "log_parent_folder")
        self.log_dir = self.get_log_dir()
        self.log_names = self._get_log_names()
        self.log_paths = self._get_log_paths()

    def get_log_dir(self):
        """Return directory containing the log files to analyze."""
        log_dir = os.path.join(self.log_parent_dir, self.player.name)
        return log_dir

    def _get_log_names(self):
        log_names = [
            filename
            for filename in os.listdir(self.log_dir)
            if filename.endswith(".log")
        ]
        return log_names

    def _get_log_paths(self):
        log_paths = [
            os.path.join(self.log_dir, log_name) for log_name in self.log_names
        ]
        return log_paths

    def analyze_logs_and_export(self):
        data = self._create_data()
        for log_name in self.log_names:
            # Open log file and read content
            log_content = self._read_log_content(log_name)
            # append date to data dict
            date = self._extract_date(log_content)
            # Count occurences of each search word in log file
            counts = self._count_searchwords(log_content)
            # Add date and counts to data dict
            self._add_date_and_counts_to_data(data, date, counts)

        df = self._convert_data_to_df(data)
        print(df)
        player_export_dir = self._create_player_export_folder()
        self._write_csv_file(player_export_dir, df)

    def _create_data(self):
        data = {"Date": []}
        for searchword in self.player.searchword_list:
            data[searchword] = []
        return data

    def _read_log_content(self, log_name):
        log_file_path = os.path.join(self.log_dir, log_name)
        with open(log_file_path, "r") as log_file:
            log_content = log_file.read()
        return log_content

    def _count_searchwords(self, log_content):
        """Return a list of the number of occurences of each search word in a given log file."""
        counts = [
            len(re.findall(sw, log_content)) for sw in self.player.searchword_list
        ]
        return counts

    def _extract_date(self, log_content):
        """Return the date of a log file as a string in the format yyyy/mm/dd."""
        date_matches = re.findall(r"\d{4}/\d{2}/\d{2}", log_content)
        date = date_matches[0] if date_matches else "N/A"
        return date

    def _add_date_and_counts_to_data(self, data: dict[str, list], date, counts):
        self._add_date_to_data(data, date)
        self._add_counts_to_data(data, counts)

    def _add_date_to_data(self, data: dict[str, list], date):
        data["Date"].append(date)

    def _add_counts_to_data(self, data: dict[str, list], counts):
        # Add counts to data dict
        for i, sw in enumerate(self.player.searchword_list):
            if sw in data:
                data[sw].append(counts[i])
            else:
                data[sw] = [counts[i]]

    def _convert_data_to_df(self, data):
        df = pd.DataFrame(data)
        df = df.groupby("Date").sum()
        # Add total row
        df.loc["Total"] = df.sum(numeric_only=True)
        # Convert searchword columns to int
        df[self.player.searchword_list] = df[self.player.searchword_list].astype(int)
        return df

    def _create_player_export_folder(self):
        base_export_dir = "exports"
        player_export_dir = self.player.name
        folder_path = os.path.join(
            self.log_parent_dir, base_export_dir, player_export_dir
        )
        create_directory(folder_path)
        return folder_path

    def _write_csv_file(self, player_export_dir, df: pd.DataFrame):
        file_name = f"{self.player.name}_export_{get_date2()}.csv"
        file_path = os.path.join(player_export_dir, file_name)
        df.to_csv(file_path, index=False)
        print(f"CSV file '{file_path}' generated successfully.")

    def _write_xlsx_file(self, player_export_dir, df: pd.DataFrame):
        file_name = f"{self.player.name}_export_{get_date2()}.xlsx"
        file_path = os.path.join(player_export_dir, file_name)
        df.to_csv(file_path, index=False)
        print(f"XLSX file '{file_path}' generated successfully.")
