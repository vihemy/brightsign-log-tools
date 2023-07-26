# Extermal modules
from configparser import ConfigParser
from datetime import date
from pathlib import Path
import os
import pandas as pd

# Internal modules
from player import Player


def get_file_path_from_config(config_key):
    """Return a file path from a given key in config.ini."""
    this_file = Path(__file__)
    ROOT_DIR = this_file.parent.parent.absolute()
    config_path = os.path.join(ROOT_DIR, "config.ini")
    parser = ConfigParser()
    parser.read(config_path)
    file_path = parser.get("file_paths", config_key)
    return file_path


def get_date():
    """Return today's date in danish format."""
    # converts to danish date-format
    today = date.today()
    today = today.strftime("%d-%m-%Y")
    return today


def shorten_filename(filename):
    """Return a shortened version of a given filename (using the final component of the path)."""
    # shortens filename for convience
    filenameShort = os.path.basename(filename)
    return filenameShort


def create_directory(path):
    """Create new path if doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def get_player_instances_from_index(index_path):
    """Return a list of instances of type Player from a given index file."""
    df = pd.read_excel(
        str(index_path),
        usecols=["Navn", "IP-adresse", "Serienummer", "Søgeord"],
    )
    players = df.values.tolist()
    player_instances = []
    for player in players:
        # unpacks values from the each item in players-list inside
        # an instance of the Player-class and appends this to
        # a new list
        player_instances.append(Player(*player))
    return player_instances
