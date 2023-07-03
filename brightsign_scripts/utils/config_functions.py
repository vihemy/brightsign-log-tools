from configparser import ConfigParser
import json

# file = 'config.ini'
# config = ConfigParser()
# config.read(file)

def get_file_path_from_config(file_name):
    # file = r"C:\Users\vhm\OneDrive - Kattegatcentret\Udstilling\Brightsign\brightsign_logs&scripts\config.ini"
    file = r"C:\VHM_local\Kode\BrightsignLogTools\config.ini"
    parser = ConfigParser()
    parser.read(file)
    file_path = parser.get('file_paths', file_name)
    return file_path

# def get_search_words_from_config(player_name):
#     file = 'config.ini'
#     config = ConfigParser()
#     config.read(file)
#     search_words = json.loads(config.get('search_words', player_name))
#     return search_words