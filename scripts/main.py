import utilities
from log_downloader import LogDownloader
from player import Player
from reporter import Reporter
import log_aggregator


def main():
    player_instances = get_player_instances()
    download_all_logs(player_instances)
    # download_specified_logs(player_instances, "Farlige Fisk (Lyd)")

    # # Run the log aggregator after all logs have been downloaded
    # log_parent_folder = utilities.get_data_from_config("file_paths", "log_parent_folder")
    # aggregated_log_file = utilities.get_data_from_config("file_paths", "aggregated_logs_path")
    # processed_logs = utilities.get_data_from_config("file_paths", "processed_logs_path")
    # log_aggregator.main(log_parent_folder, aggregated_log_file, processed_logs)


def get_player_instances():
    """Return a list of instances of type Player using player-data found through config.ini."""
    index_path = utilities.get_data_from_config("file_paths", "player_index_path")
    player_instances = utilities.get_player_instances_from_index(index_path)
    return player_instances


def download_all_logs(player_instances: list[Player]):
    """Download all logs from a given list of BrightSign players via Brightsign's Diagnostic Web Server"""
    report: str = ""
    for player in player_instances:
        if player.collect_logs:
            downloader = LogDownloader(player)
            report += downloader.download_logs()
    report += "All downloads complete"
    save_and_send_report(report)


def download_specified_logs(player_instances, *specified_names: str):
    """Download logs from specified BrightSign players via Brightsign's Diagnostic Web Server"""
    report: str = ""

    # Filter the player instances to include only those whose names are in specified_names
    specified_players = [
        player for player in player_instances if player.name in specified_names
    ]

    # Iterate over the specified players and download logs
    for player in specified_players:
        downloader = LogDownloader(player)
        report += downloader.download_logs()

    # Save and send the consolidated report
    save_and_send_report(report)


def save_and_send_report(report: str):
    reporter = Reporter(report)
    reporter.save_to_file()
    reporter.send_as_email()


def print_players(player_instances: list[Player]):
    """Print a list of players to the console."""
    for player in player_instances:
        print(player.name, player.ip, player.serial)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        utilities.send_email("Error running LogDownloader:", e)
