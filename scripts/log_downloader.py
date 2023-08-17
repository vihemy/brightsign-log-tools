# External modules
import requests
import json
import webbrowser

# Internal modules
from player import Player
from utilities import get_path_from_config


class LogDownloader:
    """
    Class to handle downloading of logs from a BrightSign player using Brightsign's Diagnostic Web Server

    Attributes
    ----------
    player : Player
        an instance of the Player class

    Methods
    -------
    download_logs()
        Download all logs from a given BrightSign players log directory via Brightsign's Diagnostic Web Server
    """

    def __init__(self, player: Player):
        self.player = player

    def download_logs(self):
        """Download all logs from a given BrightSign players log directory via Brightsign's Diagnostic Web Server"""
        print(f"\nAttempting downloading logs from player: {self.player.name}")

        try:
            json_data = self._get_json()
        except requests.Timeout:
            print(f"\nCould not connect to player with name: {self.player.name}")
            return

        try:
            log_names: list = self._get_log_names(json_data)
        except KeyError:
            print(f"\nNo logs found on player with name: {self.player.name}. Continuing to next player.")
            return
        
        try:
            self._download_to_folder(log_names)
        except UnboundLocalError as err:
            print(err)
            return
        else:
            print(f"\nDownload of player with name: {self.player.name} complete")

    def _get_json(self):
        """Return json object containing given Brightsign player's log info from Diagnostic Web Server"""
        device_url = f"http://{self.player.ip}/api/v1/files/sd/logs/"
        r = requests.get(device_url)
        t = r.text
        json_data = json.loads(t)
        return json_data

    def _get_log_names(self,json_data):
        """Return a list of log names from given json object"""
        logs = json_data["data"]["result"]["files"]
        log_count = len(logs)
        log_names = []
        x = 1

        for x in range(log_count):
            log_names.append(json_data["data"]["result"]["files"][x]["name"])
            x += 1
        return log_names

    def _download_to_folder(self, log_names):
        """Open a download url for each log in given list of log names using requests and write to file. (Slower than opening a download url in browser, but doesn't open webbrowser)"""
        # url_eksempel: "http://10.0.1.115/api/v1/files/sd/logs/BrightSignLog.TKD1CN002225-220919000.log?contents&stream"

        for log_name in log_names:
            log_file_path = self._create_log_file_path(log_name)

            url = f"http://{self.player.ip}/api/v1/files/sd/logs/{log_name}?contents&stream"
            r = requests.get(url, allow_redirects=True)
            open(log_file_path, "wb").write(r.content)

    def _create_log_file_path(self, log_name):
        """Create and return a file path for a given log name"""
        log_parent_folder = get_path_from_config("log_destination_parent_folder")
        log_file_path = log_parent_folder + f"/{self.player.name}" + f"/{log_name}"
        return log_file_path
    
    def _open_download_url(self, log_names):
        """Open a download url for each log in given list of log names. (Faster than downloading to folder with requests, but opens a webbrowser to do it.)"""
        # url_eksempel: "http://10.0.1.115/api/v1/files/sd/logs/BrightSignLog.TKD1CN002225-220919000.log?contents&stream"
        # Uses webbrowser.open to open a download link in browser
        for log_name in log_names:
            download_url = f"http://{self.player.ip}/api/v1/files/sd/logs/{log_name}?contents&stream"
            webbrowser.open(download_url)