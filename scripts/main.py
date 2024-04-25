import utilities
from log_downloader import LogDownloader
from log_mover import LogMover
from log_analyzer import LogAnalyzer
from player import Player
from reporter import Reporter


def main():
    player_instances = get_player_instances()
    download_all_logs(player_instances)
    # download_specified_logs(player_instances)
    # analyze_logs_test(player_instances)


def analyze_logs_test(player_instances: list[Player]):
    analyzer = LogAnalyzer(player_instances[0])
    analyzer.analyze_logs_and_export()


def get_player_instances():
    """Return a list of instances of type Player using player-data found through config.ini."""
    index_path = utilities.get_data_from_config("file_paths", "player_index_path")
    player_instances = utilities.get_player_instances_from_index(index_path)
    return player_instances


def download_all_logs(player_instances: list[Player]):
    """Download all logs from a given list of BrightSign players via Brightsign's Diagnostic Web Server"""
    report: str = ""
    for player in player_instances:
        downloader = LogDownloader(player)
        report += downloader.download_logs()
    report += "All downloads complete"
    save_and_send_report(report)


def download_specified_logs(player_instances: list[Player]):
    """Download logs from specified BrightSign players via Brightsign's Diagnostic Web Server"""
    report: str = ""
    player = player_instances[7]
    downloader = LogDownloader(player)

    report += downloader.download_logs()
    save_and_send_report(report)


def move_logs(player_instances: list[Player]):
    """Move all logs from a given list of BrightSign players to a destination directory configured in config.ini"""
    src_folder = utilities.get_data_from_config("file_paths", "log_source_directory")
    dst_parent_folder = utilities.get_data_from_config(
        "file_paths", "log_parent_folder"
    )

    for player in player_instances:
        mover = LogMover(player, src_folder, dst_parent_folder)
        mover.relocate_logs()


def analyze_logs(player_instances: list[Player]):
    """Use LogAnalyzer-class to analyze logs belonging to each player-instance on a list and create a CSV file with the total count of occurrences + each search word"""
    for player in player_instances:
        analyzer = LogAnalyzer(player)
        # analyzer.analyze_logs_and_export()
        print(
            analyzer.player.name,
            analyzer.player.searchwords,
            analyzer.player.headers,
            analyzer.log_directory,
        )


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
        utilities.send_email("Error running LogDownloader", e)
