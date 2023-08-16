# External modules
import re
import os
import shutil

# Internal modules
import utilities
from player import Player


class LogMover:
    """
    Class to handle moving of logs from a BrightSign player between direcotries

    Attributes
    ----------
    player : Player
        an instance of the Player class
    src_folder : str
        the source directory from which to move logs
    dst_parent_folder : str
        the destination directory to which to move logs

    Methods
    -------
    relocate_logs()
        Move all logs from download-folder to a given destination directory
    """

    def __init__(self, player: Player, src_folder, dst_parent_folder):
        self.player = player
        self.src_folder = src_folder
        self.dst_parent_folder = dst_parent_folder

    def relocate_logs(self):
        """Move all logs from download-folder to a given destination directory"""
        dst_player_folder = self._set_dst_player_folder()
        utilities.create_directory(dst_player_folder)
        self._move_non_dublicates(dst_player_folder)

    def _set_dst_player_folder(self):
        """Create and return a destination directory for a given player"""
        dst_player_folder = self.dst_parent_folder + f"\{self.player.name}"
        return dst_player_folder

    def _move_non_dublicates(self, dst_player_folder):
        """Move all non-dublicate logs from download-folder to a given destination directory"""
        nr_files_moved = 0
        for filename in os.listdir(self.src_folder):
            if (
                self._belongs_to_player(filename) == True
                and self._is_duplicate(filename) == False
            ):
                file_to_move = os.path.join(self.src_folder, filename)
                shutil.move(file_to_move, dst_player_folder)
                nr_files_moved += 1
        print(
            f"\nFiles copied from {self.src_folder} to {dst_player_folder}: {nr_files_moved}"
        )

    def _belongs_to_player(self, filename):
        """Return True if a given filename contains a given player's serial number"""
        if self.player.serial in filename:
            return True
        else:
            return False

    def _is_duplicate(self, filename):
        """Return True if a given filename containsindication of duplcation (e.g. "(1)")"""
        # Define the regular expression pattern to match "(number)"
        pattern = r"\(\d+\)"
        # Search for the pattern in the filename
        match = re.search(pattern, filename)
        # If a match is found, return True; otherwise, return False
        return bool(match)