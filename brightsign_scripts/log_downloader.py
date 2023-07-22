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
            json_data = self._get_json()
        except requests.Timeout:
            print(
                f"\nCould not connect to player with name: {self.player.name}"
            )

        try:
            log_names: list = self._get_log_names(json_data)
        except KeyError:
            print(f"\nNo logs found on player with name: {self.player.name}")

        self._open_download_url(log_names)
        print(f"\nDownload of player with name: {self.player.name} complete")

    def _get_json(self):
        device_url = f"http://{self.player.ip}/api/v1/files/sd/logs/"
        # gets json from url
        r = requests.get(device_url)
        t = r.text
        json_data = json.loads(t)
        return json_data

    def _get_log_names(json_data):
        # collect log names from json
        logs = json_data["data"]["result"]["files"]
        log_count = len(logs)
        log_names = []
        x = 1

        for x in range(log_count):
            log_names.append(json_data["data"]["result"]["files"][x]["name"])
            x += 1
        return log_names

    def _open_download_url(self, log_names):
        # url_eksempel: "http://10.0.1.115/api/v1/files/sd/logs/BrightSignLog.TKD1CN002225-220919000.log?contents&stream"
        # Can't download through request. Uses webbrowser.open to open a download link in browser
        for log_name in log_names:
            download_url = f"http://{self.player.ip}/api/v1/files/sd/logs/{log_name}?contents&stream"
            webbrowser.open(download_url)
