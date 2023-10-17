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
    def __init__(self, player: Player):
        self.player = player
        self.log_directory = self.get_log_directory()
        self.log_names = self._get_log_names()
        self.log_paths = self._get_log_paths()

    def get_log_directory(self):
        """Return directory containing the log files to analyze."""
        log_directory = os.path.join(
            get_path_from_config("log_parent_folder"), self.player.name
        )
        return log_directory

    def _get_log_names(self):
        log_names = [
            filename
            for filename in os.listdir(self.log_directory)
            if filename.endswith(".log")
        ]
        return log_names

    def _get_log_paths(self):
        log_paths = [
            os.path.join(self.log_directory, log_name) for log_name in self.log_names
        ]
        return log_paths

    # ----------------------------------------------- RYD OP HERUNDER + LAV CSV EXPORT --------------------------------------------------#

    def analyze_logs_and_generate_csv(self):
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

    def _create_data(self):
        data = {"Date": []}
        for searchword in self.player.searchword_list:
            data[searchword] = []
        return data

    def _read_log_content(self, log_name):
        log_file_path = os.path.join(self.log_directory, log_name)
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
        # Create dataframe from data dict
        df = pd.DataFrame(data)
        # Group by date and sum
        df.groupby("Date").sum()
        # Add total row
        df.loc["Total"] = df.sum(numeric_only=True)
        # Convert searchword columns to int
        df[self.player.searchword_list] = df[self.player.searchword_list].astype(int)
        return df

    # def _add_count_to_df(self, log_content):
    #     for searchword in self.player.searchword_list:
    #         count = len(re.findall(searchword, log_content, re.IGNORECASE))

    #     df = self._count_searchwords(log_content)
    #     total_count = sum(df.values())
    #     self._add_to_df(log_name, total_count, df)
    #     self.total_count += total_count

    # for each log in log_names, count the occurences of each item in searchword_list and add it to the dataframe under the corresponding header

    #     self._write_csv_file()

    # def _count_searchwords(self, log_content):
    #     df = {}
    #     for sw in self.player.searchword_list:
    #         count = len(re.findall(sw.strip(), log_content, re.IGNORECASE))
    #         df[sw.strip()] = count
    #     return df

    # def _add_to_df(self, log_file, total_count, df):
    #     data = {"Log File": log_file, "Total Count": total_count, **df}
    #     self.df = self.df.append(data, ignore_index=True)

    # def _write_csv_file(self):
    #     csv_filepath = self._create_filepath()
    #     self.df.to_csv(csv_filepath, index=False)
    #     print(f"CSV file '{csv_filepath}' generated successfully.")

    # def _create_filepath(self):
    #     player_export_folder = os.path.join(
    #         get_path_from_config("export_parent_folder"),
    #         self.player.name + " export",
    #     )
    #     create_directory(player_export_folder)
    #     file_name = f"{self.player.name}_export_{get_date()}.csv"
    #     file_path = os.path.join(player_export_folder, file_name)
    #     return file_path
