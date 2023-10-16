# External modules
import requests
import json
import webbrowser
import http.client

# Internal modules
from player import Player
from utilities import get_path_from_config, create_directory, send_email


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
        """Download all logs from a given BrightSign players log directory via Brightsign's Diagnostic Web Server.
        Returns systemLog for export to email or log file"""
        try:
            try:
                json_data = self._get_json()
                log_names: list = self._get_log_names(json_data)
                count = self._download_to_folder(log_names)
                msg = f"Download of player with name: {self.player.name} complete. Logs downloaded: {count + 1}\n"
            except (
                requests.Timeout,
                requests.ConnectionError,
                http.client.RemoteDisconnected,
            ) as err:
                msg = f"Could not connect to player with name: {self.player.name} \n Error messag: {err}\n"
            except KeyError:
                msg = f"No logs found on player with name: {self.player.name}. Continuing to next player.\n"
        except UnboundLocalError as err:
            msg = err
        finally:
            print(msg)
            return msg

    def _get_json(self):
        """Return json object containing given Brightsign player's log info from Diagnostic Web Server"""
        device_url = f"http://{self.player.ip}/api/v1/files/sd/logs/"
        r = requests.get(device_url)
        t = r.text
        json_data = json.loads(t)
        return json_data

    def _get_log_names(self, json_data):
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

        for i, log_name in enumerate(log_names):
            file_path = self._create_log_file_path(log_name)

            url = f"http://{self.player.ip}/api/v1/files/sd/logs/{log_name}?contents&stream"
            r = requests.get(url, allow_redirects=True)
            open(file_path, "wb").write(r.content)
        return i

    def _create_log_file_path(self, log_name):
        """Create and return a file path for a given log name"""
        log_parent_folder = get_path_from_config("log_parent_folder")
        log_player_folder = log_parent_folder + f"/{self.player.name}"
        create_directory(log_player_folder)
        file_path = log_player_folder + f"/{log_name}"
        return file_path

    def _open_download_url(self, log_names):
        """Open a download url for each log in given list of log names. (Faster than downloading to folder with requests, but opens a webbrowser to do it.)"""
        # url_eksempel: "http://10.0.1.115/api/v1/files/sd/logs/BrightSignLog.TKD1CN002225-220919000.log?contents&stream"
        # Uses webbrowser.open to open a download link in browser
        for log_name in log_names:
            download_url = f"http://{self.player.ip}/api/v1/files/sd/logs/{log_name}?contents&stream"
            webbrowser.open(download_url)
