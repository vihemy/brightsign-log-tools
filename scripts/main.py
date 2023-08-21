import utilities
from log_downloader import LogDownloader
from log_mover import LogMover
from log_analyzer import LogAnalyzer
from player import Player


def main():
    player_instances = get_player_instances()
    print_players(player_instances)
    # download_logs(player_instances)
    # move_logs(player_instances)
    # analyze_logs(player_instances)


def get_player_instances():
    """Return a list of instances of type Player using player-data found through config.ini."""
    index_path = utilities.get_path_from_config("player_index_path")
    player_instances = utilities.get_player_instances_from_index(index_path)
    return player_instances


def download_logs(player_instances: list[Player]):
    """Download all logs from a given list of BrightSign players via Brightsign's Diagnostic Web Server"""
    for player in player_instances:
        downloader = LogDownloader(player)
        downloader.download_logs()


def move_logs(player_instances: list[Player]):
    """Move all logs from a given list of BrightSign players to a destination directory configured in config.ini"""
    src_folder = utilities.get_path_from_config("log_source_directory")
    dst_parent_folder = utilities.get_path_from_config("log_destination_parent_folder")

    for player in player_instances:
        mover = LogMover(player, src_folder, dst_parent_folder)
        mover.relocate_logs()


def analyze_logs(player_instances: list[Player]):
    """Use LogAnalyzer-class to analyze logs belonging to each player-instance on a list and create a CSV file with the total count of occurrences + each search word"""
    log_parent_folder = utilities.get_path_from_config("log_destination_parent_folder")

    for player in player_instances:
        analyzer = LogAnalyzer(player, log_parent_folder)
        analyzer.analyze_logs_and_generate_csv()


def print_players(player_instances: list[Player]):
    """Print a list of players to the console."""
    for player in player_instances:
        print(player.name, player.ip, player.serial)


if __name__ == "__main__":
    main()
