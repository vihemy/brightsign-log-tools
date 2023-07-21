# Extermal modules
from configparser import ConfigParser
from datetime import date
import os
import pandas as pd


def get_file_path_from_config(file_name):
    # file = r"C:\Users\vhm\OneDrive - Kattegatcentret\Udstilling\Brightsign\brightsign_logs&scripts\config.ini"
    file = r"C:\VHM_local\Kode\BrightsignLogTools\config.ini"
    parser = ConfigParser()
    parser.read(file)
    file_path = parser.get("file_paths", file_name)
    return file_path


def get_date():
    # converts to danish date-format
    today = date.today()
    today = today.strftime("%d-%m-%Y")
    return today


def shorten_filename(filename):
    # shortens filename for convience
    filenameShort = os.path.basename(filename)
    return filenameShort


def create_directory(path):
    # Creates new folder if doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)


def get_dict_from_player_index(index_path):
    # get relavant columns from excel file (Ip-adress is used for download, serial for identification)
    df = pd.read_excel(str(index_path), usecols=["Navn", "IP-adresse", "Serienummer"])
    # create new tuple-column from columns ip-adresse and serienummer
    df["IP_serial"] = list(zip(df["IP-adresse"], df["Serienummer"]))
    # creates dict with new tuple as value
    players = df.set_index("Navn")["IP_serial"].to_dict()
    return players
