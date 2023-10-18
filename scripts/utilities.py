# Extermal modules
import os
import pandas as pd
import smtplib
import sys
from configparser import ConfigParser
from datetime import date
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Internal modules
from player import Player


def get_data_from_config(section: str, key: str):
    """Return a file path from a given key in config.ini."""
    this_file = Path(__file__)
    ROOT_DIR = this_file.parent.parent.absolute()
    config_path = os.path.join(ROOT_DIR, "config.ini")
    parser = ConfigParser()
    parser.read(config_path)
    data = parser.get(section, key)
    return data


def get_date():
    """Return today's date in danish format (dd-mm-yy)."""
    today = date.today()
    today = today.strftime("%d-%m-%Y")
    return today


def get_date2():
    """Return today's date in format (yymmdd)."""
    today = date.today()
    today = today.strftime("%Y%m%d")
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


def get_app_folder():
    """Return the path to the folder containing the application."""
    if getattr(sys, "frozen", False):
        # If the application is run as a -onefile (pyinstaller) the path is different than if run as a script
        app_dir = os.path.dirname(sys.executable)
    # If not the application is run as onefile (pyinstaller) the path is set to the parent directory of this script
    else:
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return app_dir


def send_email(subject: str, message: str):
    # Set up the SMTP server
    smtp_server = get_data_from_config("mail", "email_server")
    smtp_port = get_data_from_config("mail", "email_port")
    smtp_username = get_data_from_config("mail", "email_from")
    smtp_password = get_data_from_config("mail", "email_password")

    # Set up the email message
    msg = MIMEMultipart()
    msg["From"] = get_data_from_config("mail", "email_from")
    msg["To"] = get_data_from_config("mail", "email_to")
    msg["Subject"] = subject
    body = message
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, "vhm@kattegatcentret.dk", msg.as_string())
