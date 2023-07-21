# External modules
import re
import requests
import json
import webbrowser
import os
import shutil

# Internal modules
from utils import directory_functions


class Player:
    def __init__(self, name, ip, serial, searchwords):
        self.name = name
        self.ip = ip
        self.serial = serial
        self.searchwords = searchwords

    def player_name(self):
        return self.name

    def player_ip(self):
        return self.ip

    def player_serial(self):
        return self.serial

    def download_logs(self):
        try:
            json_data = self._json_from_url(self.ip)
        except requests.Timeout as err:
            print(f"\nCould not connect to player with name: {self.name}")
        try:
            log_name_list = self._log_name_list_from_json(json_data)
        except KeyError as err:
            print(f"\nNo logs found on player with name: {self.name}")

        self._download_logs_from_list(log_name_list, self.name)
        print(f"\nDownload of player with name: {self.name} complete")

    def _json_from_url(ip):
        device_url = f"http://{ip}/api/v1/files/sd/logs/"
        # gets json from url
        r = requests.get(device_url)
        t = r.text
        json_data = json.loads(t)
        return json_data

    def _log_name_list_from_json(data):
        # counts nr of logentries
        logs = data["data"]["result"]["files"]
        log_count = len(logs)
        log_name_list = []
        x = 1
        for x in range(log_count):
            log_name_list.append(data["data"]["result"]["files"][x]["name"])
            x += 1
        return log_name_list

    def _download_logs_from_list(log_name_list, ip):
        # url_eksempel: "http://10.0.1.115/api/v1/files/sd/logs/BrightSignLog.TKD1CN002225-220919000.log?contents&stream"
        # Can't download through request, so webbrowser.open is used instead to open a download-window
        for log_name in log_name_list:
            download_url = (
                f"http://{ip}/api/v1/files/sd/logs/{log_name}?contents&stream"
            )
            webbrowser.open(download_url)

    def copy_logs_to_new_directory(self, source_path, destination_root):
        destination_path = self._set_destination_path(destination_root)
        directory_functions.create_directory(destination_path)
        self._copy_unique_files_to_directory(source_path, destination_path)

    def _set_destination_path(self, destination_root):
        # sets destination folder using the player name
        destination_path = destination_root + f"\{self.name}"
        return destination_path

    def _copy_unique_files_to_directory(self, source_path, destination_path):
        nr_files_moved = 0
        for filename in os.listdir(source_path):
            if (
                self._does_file_belong_to_player == True
                and self._is_file_duplicate(filename) == False
            ):
                shutil.copy(os.path.join(source_path, filename), destination_path)
                nr_files_moved += 1
        print(
            f"\nFiles copied from {source_path} to {destination_path}: {nr_files_moved}"
        )

    def _does_file_belong_to_player(self, filename):
        # uses serial because player-name is not present in file-name
        if self.serial in filename:
            return True
        else:
            return False

    def _is_file_duplicate(filename):
        # Define the regular expression pattern to match "(number)"
        pattern = r"\(\d+\)"

        # Search for the pattern in the filename
        match = re.search(pattern, filename)

        # If a match is found, return True; otherwise, return False
        return bool(match)

    # def analyze_logs():
    #     log_directory =
