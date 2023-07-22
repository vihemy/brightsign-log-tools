# External modules
import re
import os
import shutil

# Internal modules
import utilities
from player import Player


class LogMover:
    def __init__(self, player: Player, source_path, destination_root):
        self.player = player
        self.source_path = source_path
        self.destination_root = destination_root

    def copy_logs_to_new_directory(self, source_path, destination_root):
        destination_path = self._set_destination_path(destination_root)
        utilities.create_directory(destination_path)
        self._copy_unique_files_to_directory(source_path, destination_path)

    def _set_destination_path(self, destination_root):
        # sets destination folder using the player name
        destination_path = destination_root + f"\{self.player.name}"
        return destination_path

    def _copy_unique_files_to_directory(self, source_path, destination_path):
        nr_files_moved = 0
        for filename in os.listdir(source_path):
            if (
                self._does_file_belong_to_player == True
                and self._is_file_duplicate(filename) == False
            ):
                shutil.copy(os.path.join(source_path, filename), destination_path)
                nr_files_moved += 1
        print(
            f"\nFiles copied from {source_path} to {destination_path}: {nr_files_moved}"
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
