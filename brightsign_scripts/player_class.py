import requests
import json
import webbrowser
import os
import shutil

from utils import directory_functions


class Player:
    def __init__(self, name, ip, serial):
        self.name = name
        self.ip = ip
        self.serial = serial

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

    def move_logs(self, src_path, dst_root):
        # sets destination folder using the player name
        dst_path = self._set_dst_path(dst_root, self.name)
        directory_functions.create_directory(dst_path)

        # uses string_to_match and string_to_avoid to find relavant
        # files and avoid dublicates (paranthesis implies duplication)
        string_to_match = self.serial
        string_to_avoid = "("
        self._move_certain_files(src_path, dst_path, string_to_match, string_to_avoid)

    def _set_dst_path(dst_root, player_name):
        dst_path = dst_root + f"\{player_name}"
        return dst_path

    def _move_certain_files(src_path, dst_path, string_to_match, string_to_avoid):
        nr_files_moved = 0
        for filename in os.listdir(src_path):
            # Move file if the filename contains string_to_match and doesn't contain string_to_avoid
            if string_to_match in filename and not string_to_avoid in filename:
                shutil.copy(os.path.join(src_path, filename), dst_path)
                nr_files_moved += 1
        print(f"\nFiles copied from {src_path} to {dst_path}: {nr_files_moved}")
