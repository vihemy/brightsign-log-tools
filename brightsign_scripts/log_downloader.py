# External modules
import requests
import json
import webbrowser

# Internal modules
from player import Player


class LogDownloader:
    def __init__(self, player: Player):
        self.player = player

    def download_logs(self):
        print(f"\nAttempting downloading logs from player: {self.player.name}")
        try:
            json_data = self._json_from_url()
        except requests.Timeout:
            print(
                f"\nCould not connect to player with name: {self.player.name}"
            )
        try:
            log_name_list = self._log_name_list_from_json(json_data)
        except KeyError:
            print(f"\nNo logs found on player with name: {self.player.name}")

        self._download_logs_from_list(
            log_name_list, self.player.name
        )  # STEMMER IKKE OVERENS MED IP I METHOD
        print(f"\nDownload of player with name: {self.player.name} complete")

    def _json_from_url(self):
        device_url = f"http://{self.player.ip}/api/v1/files/sd/logs/"
        # gets json from url
        r = requests.get(device_url)
        t = r.text
        json_data = json.loads(t)
        return json_data

    def _log_name_list_from_json(data):
        # counts nr of log-entries
        logs = data["data"]["result"]["files"]
        log_count = len(logs)
        log_name_list = []
        x = 1
        for x in range(log_count):
            log_name_list.append(data["data"]["result"]["files"][x]["name"])
            x += 1
        return log_name_list

    def _download_logs_from_list(self, log_name_list):
        # url_eksempel: "http://10.0.1.115/api/v1/files/sd/logs/BrightSignLog.TKD1CN002225-220919000.log?contents&stream"
        # Can't download through request. Uses webbrowser.open instead to open a download-window
        for log_name in log_name_list:
            download_url = f"http://{self.player.ip}/api/v1/files/sd/logs/{log_name}?contents&stream"
            webbrowser.open(download_url)
