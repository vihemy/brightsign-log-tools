import utilities
from log_downloader import LogDownloader
from player import Player
from reporter import Reporter
import log_aggregator

REPORT_NAME = "LogDownloaderReport"


def main():
    player_instances = get_player_instances()
    report_content = download_all_logs(player_instances)
    return report_content


def get_player_instances():
    """Return a list of instances of type Player using player-data found through config.ini."""
    index_path = utilities.get_data_from_config("file_paths", "player_index_path")
    player_instances = utilities.get_player_instances_from_index(index_path)
    return player_instances


def download_all_logs(player_instances: list[Player]):
    """Download all logs from a given list of BrightSign players via Brightsign's Diagnostic Web Server"""
    report_content: str = ""
    for player in player_instances:
        if player.collect_logs:
            downloader = LogDownloader(player)
            report_content += downloader.download_logs()
    report_content += "All downloads complete"
    return report_content


def aggregate_all_logs():
    """Aggregate all logs into a single CSV file."""
    log_parent_folder = utilities.get_data_from_config(
        "file_paths", "log_parent_folder"
    )
    aggregated_log_file = utilities.get_data_from_config(
        "file_paths", "aggregated_logs_path"
    )
    processed_logs = utilities.get_data_from_config("file_paths", "processed_logs_path")
    log_aggregator.main(log_parent_folder, aggregated_log_file, processed_logs)


def download_specified_logs(player_instances, *specified_names: str):
    """Download logs from specified BrightSign players via Brightsign's Diagnostic Web Server"""
    report_content: str = ""

    # Filter the player instances to include only those whose names are in specified_names
    specified_players = [
        player for player in player_instances if player.name in specified_names
    ]

    # Iterate over the specified players and download logs
    for player in specified_players:
        downloader = LogDownloader(player)
        report_content += downloader.download_logs()

    # Save and send the consolidated report_content
    save_and_send_report(REPORT_NAME, report_content)


def save_and_send_report(name: str, report_content: str):
    reporter = Reporter(name, report_content)
    reporter.save_to_file()
    reporter.send_as_email(onlyErrors=True)


def print_players(player_instances: list[Player]):
    """Print a list of players to the console."""
    for player in player_instances:
        print(player.name, player.ip, player.serial)


if __name__ == "__main__":
    try:
        report_content = main()
    except Exception as e:
        report_content = f"Error downloading logs: {e}"
    finally:
        print(report_content)
        save_and_send_report(REPORT_NAME, report_content)
