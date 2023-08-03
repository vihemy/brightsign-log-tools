import utilities
from log_downloader import LogDownloader
from log_mover import LogMover
from log_analyzer import LogAnalyzer


def main():
    player_instances = get_player_instances()
    # download_logs(player_instances)
    # move_logs(player_instances)
    analyze_logs(player_instances)


def get_player_instances():
    """Return a list of instances of type Player using player-data found through config.ini."""
    index_path = utilities.get_path_from_config("brightsign_index_path")
    player_instances = utilities.get_player_instances_from_index(index_path)
    return player_instances


def download_logs(player_instances):
    """Download all logs from a given list of BrightSign players via Brightsign's Diagnostic Web Server"""
    for player in player_instances:
        downloader = LogDownloader(player)
        downloader.download_logs()


def move_logs(player_instances):
    """Move all logs from a given list of BrightSign players to a destination directory configured in config.ini"""
    src_folder = utilities.get_path_from_config("log_source_directory")
    dst_parent_folder = utilities.get_path_from_config("log_destination_parent_folder")

    for player in player_instances:
        mover = LogMover(player, src_folder, dst_parent_folder)
        mover.relocate_logs()


def analyze_logs(player_instances):
    """Use LogAnalyzer-class to analyze logs belonging to each player-instance on a list and create a CSV file with the total count of occurrences + each search word"""
    log_parent_folder = utilities.get_path_from_config("log_destination_parent_folder")

    for player in player_instances:
        analyzer = LogAnalyzer(player, log_parent_folder)
        analyzer.analyze_logs_and_generate_csv()


if __name__ == "__main__":
    main()
