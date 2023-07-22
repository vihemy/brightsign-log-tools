# External modules
import re
import os
import shutil

# Internal modules
import utilities
from player import Player


class LogMover:
    def __init__(self, player: Player, src_folder, dst_parent_folder):
        self.player = player
        self.src_folder = src_folder
        self.dst_parent_folder = dst_parent_folder

    def copy_logs_to_new_directory(self, src_folder, dst_parent_folder):
        dst_player_folder = self._set_destination_player_folder(
            dst_parent_folder
        )
        utilities.create_directory(dst_player_folder)
        self._copy_unique_files_to_directory(src_folder, dst_player_folder)

    def _set_destination_player_folder(self, dst_parent_folder):
        dst_player_folder = dst_parent_folder + f"\{self.player.name}"
        return dst_player_folder

    def _copy_unique_files_to_directory(self, src_folder, dst_player_folder):
        nr_files_moved = 0
        for filename in os.listdir(src_folder):
            if (
                self._does_file_belong_to_player == True
                and self._is_file_duplicate(filename) == False
            ):
                shutil.copy(
                    os.path.join(src_folder, filename), dst_player_folder
                )
                nr_files_moved += 1
        print(
            f"\nFiles copied from {src_folder} to {dst_player_folder}: {nr_files_moved}"
        )

    def _does_file_belong_to_player(self, filename):
        # uses serial because player-name is not present in file-name
        if self.player.serial in filename:
            return True
        else:
            return False

    def _is_file_duplicate(filename):
        # Define the regular expression pattern to match "(number)"
        pattern = r"\(\d+\)"

        # Search for the pattern in the filename
        match = re.search(pattern, filename)

        # If a match is found, return True; otherwise, return False
        return bool(match)
