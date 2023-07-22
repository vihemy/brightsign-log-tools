import utilities
from log_downloader import LogDownloader

from loghandlers import logscraper_main
from loghandlers import logdistributer_main
from loghandlers import dvaergpingvin_main
from loghandlers import kongepingvin_main
from loghandlers import lyttestation_common_main
from loghandlers import ekspertskaerm1_main
from loghandlers import ekspertskaerm2_main


def main():
    # ------------------------------------------------------ CONFIG ------------------------------------------------------
    index_path = utilities.get_file_path_from_config("brightsign_index_path")

    player_instances = utilities.get_player_instances_from_index(index_path)

    # # ------------------------------------------------------ DOWNLOAD LOGS -----------------------------------------------------

    for player in player_instances:
        downloader = LogDownloader(player)
        downloader.download_logs()

    # # ------------------------------------------------------ MOVE LOGS ------------------------------------------------------
    # log_download_folder = utilities.get_file_path_from_config("log_download_folder")
    # log_destination_root_folder = utilities.get_file_path_from_config(
    #     "log_destination_root_folder"
    # )

    # log_downloader(players, log_download_folder, log_destination_root_folder)

    # # ------------------------------------------------------ ANALYZE LOGS ------------------------------------------------------
    # dvaergpingvin_main(log_destination_root_folder)
    # kongepingvin_main(log_destination_root_folder)
    # lyttestation_common_main(log_destination_root_folder, "Lyttestation 1")
    # lyttestation_common_main(log_destination_root_folder, "Lyttestation 2")
    # lyttestation_common_main(log_destination_root_folder, "Lyttestation 3")
    # ekspertskaerm1_main(log_destination_root_folder)
    # ekspertskaerm2_main(log_destination_root_folder)


if __name__ == "__main__":
    main()
