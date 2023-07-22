import utilities
from log_downloader import LogDownloader
from log_mover import LogMover

from loghandlers import logscraper_main
from loghandlers import logdistributer_main
from loghandlers import dvaergpingvin_main
from loghandlers import kongepingvin_main
from loghandlers import lyttestation_common_main
from loghandlers import ekspertskaerm1_main
from loghandlers import ekspertskaerm2_main


def main():
    player_instances = get_player_instances()
    # download_logs(player_instances)
    move_logs(player_instances)

    # # ------------------------------------------------------ Move LOGS ------------------------------------------------------
    # log_source_directory = utilities.get_file_path_from_config(
    #     "log_source_directory"
    # )
    # log_destination_root_folder = utilities.get_file_path_from_config(
    #     "log_destination_root_folder"
    # )

    # log_downloader(players, log_source_directory, log_destination_root_folder)

    # # ------------------------------------------------------ ANALYZE LOGS ------------------------------------------------------
    # dvaergpingvin_main(log_destination_root_folder)
    # kongepingvin_main(log_destination_root_folder)
    # lyttestation_common_main(log_destination_root_folder, "Lyttestation 1")
    # lyttestation_common_main(log_destination_root_folder, "Lyttestation 2")
    # lyttestation_common_main(log_destination_root_folder, "Lyttestation 3")
    # ekspertskaerm1_main(log_destination_root_folder)
    # ekspertskaerm2_main(log_destination_root_folder)


def get_player_instances():
    index_path = utilities.get_file_path_from_config("brightsign_index_path")

    player_instances = utilities.get_player_instances_from_index(index_path)

    return player_instances


def download_logs(player_instances):
    for player in player_instances:
        downloader = LogDownloader(player)
        downloader.download_logs()


def move_logs(player_instances):
    src_folder = utilities.get_file_path_from_config("log_source_directory")
    dst_parent_folder = utilities.get_file_path_from_config(
        "log_destination_parent_folder"
    )

    for player in player_instances:
        mover = LogMover(player, src_folder, dst_parent_folder)
        mover.copy_logs_to_new_directory(src_folder, dst_parent_folder)


if __name__ == "__main__":
    main()
