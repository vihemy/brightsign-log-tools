import os
import shutil
from utils import directory_functions


def main(players, src_path, dst_root):
     # gets dictionary players from index file through read_brightsign_index()
    for key, value in players.items():
        #sets player_name to dict-key and player_serial to 2. item of the tuple in dict-value
        player_name = key
        player_serial = value[1]
        #sets destination folder using the player name
        dst_path = set_dst_path(dst_root, player_name)
        directory_functions.create_directory(dst_path)

        #uses string_to_match and string_to_avoid to find relavant files and avoid dublicates (paranthesis implies duplication)
        string_to_match = player_serial
        string_to_avoid = "("
        move_certain_files(src_path, dst_path, string_to_match, string_to_avoid)

# def semi_main():
#     #for copying individual player's logs
#     #set player_name to relavant dict-key and player_serial to 2. item of the tuple in the same dict-value
#         player_name = "dvaergpingvin"
#         player_serial = "46D98V000729"
#         #sets destination folder using the player name
#         dst_path = set_dst_path(player_name)

#         #uses string_to_match and string_to_avoid to find relavant files and avoid dublicates.
#         string_to_match = player_serial
#         string_to_avoid = "("
#         move_certain_files(src_path, dst_path, string_to_match, string_to_avoid)

def set_dst_path(dst_root, player_name):
    dst_path = dst_root + f"\{player_name}"
    return dst_path

def move_certain_files(src_path, dst_path, string_to_match, string_to_avoid):
    nr_files_moved = 0
    for filename in os.listdir(src_path):
        #Move file if the filename contains string_to_match and doesn't contain string_to_avoid
        if string_to_match in filename and not string_to_avoid in filename:
            shutil.copy(os.path.join(src_path,filename), dst_path)
            nr_files_moved+=1
    print(f"\nFiles copied from {src_path} to {dst_path}: {nr_files_moved}")