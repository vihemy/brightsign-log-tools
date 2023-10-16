# Extermal modules
import os
import pandas as pd
import smtplib
from configparser import ConfigParser
from datetime import date
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Internal modules
from player import Player


# DELETE THIS AND REPLACE USECASES WITH GET_DATA_FROM_CONFIG
def get_path_from_config(config_key):
    """Return a file path from a given key in config.ini."""
    this_file = Path(__file__)
    ROOT_DIR = this_file.parent.parent.absolute()
    config_path = os.path.join(ROOT_DIR, "config.ini")
    parser = ConfigParser()
    parser.read(config_path)
    file_path = parser.get("file_paths", config_key)
    return file_path


def get_data_from_config(config_key):
    """Return a file path from a given key in config.ini."""
    this_file = Path(__file__)
    ROOT_DIR = this_file.parent.parent.absolute()
    config_path = os.path.join(ROOT_DIR, "config.ini")
    parser = ConfigParser()
    parser.read(config_path)
    data = parser.get("mail", config_key)
    return data


def get_date():
    """Return today's date in danish format (dd-mm-yy)."""
    today = date.today()
    today = today.strftime("%d-%m-%Y")
    return today


def shorten_filename(filename):
    """Return a shortened version of a given filename (using the final component of the path)."""
    filenameShort = os.path.basename(filename)
    return filenameShort


def create_directory(path):
    """Create new folder path if it doesn't already exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def get_player_instances_from_index(index_path):
    """Return a list of instances of type Player from a given index file."""
    df = pd.read_excel(
        str(index_path),
        sheet_name="Players",
        usecols=["Navn", "IP-adresse", "Serienummer", "Søgeord", "Overskrifter"],
    )
    players = df.values.tolist()
    player_instances: list[Player] = []
    for player in players:
        # unpacks values from the each item in players-list inside
        # an instance of the Player-class and appends to list
        player_instances.append(Player(*player))
    return player_instances


def send_email(subject: str, message: str):
    # Set up the SMTP server
    smtp_server = get_data_from_config("email_server")
    smtp_port = get_data_from_config("email_port")
    smtp_username = get_data_from_config("email_from")
    smtp_password = get_data_from_config("email_password")

    # Set up the email message
    msg = MIMEMultipart()
    msg["From"] = get_data_from_config("email_from")
    msg["To"] = get_data_from_config("email_to")
    msg["Subject"] = subject
    body = message
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, "vhm@kattegatcentret.dk", msg.as_string())
