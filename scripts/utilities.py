# Extermal modules
import os
import pandas as pd
import smtplib
import sys
from configparser import ConfigParser
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Internal modules
from player import Player


def get_data_from_config(section: str, key: str):
    config_path = _get_config_path()
    data = _parse_config_file(config_path, section, key)
    return data


def _get_config_path():
    """Return the path to the config.ini file."""
    app_dir = get_app_folder()
    config_path = os.path.join(app_dir, "config.ini")
    return config_path


def _parse_config_file(config_path, section: str, key: str):
    """Return a ConfigParser instance with the config.ini file parsed."""
    parser = ConfigParser()
    parser.read(config_path)
    data = parser.get(section, key, vars=os.environ)
    return data


def get_app_folder():
    """Return the path to the folder containing the application."""
    # determine if app is a script file or frozen exe
    # if exe
    if getattr(sys, "frozen", False):
        app_dir = os.path.dirname(sys.executable)
    # If script:
    # # NOTE! Returns the parent to the parent of the current file (because config-file is stored outside of scripts-folder when not build to exe)
    else:
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return app_dir


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


# OBS! HAS TO REFLECT ORDER OF HEADERS IN EXCEL FILE
def get_player_instances_from_index(index_path):
    PLAYER_COLUMN_MAPPING = {
        "Navn": "name",
        "Serienummer": "serial",
        "IP-adresse": "ip",
        "Log-indsamling": "collect_logs",
    }

    df = pd.read_excel(
        str(index_path),
        sheet_name="Players",
        usecols=list(PLAYER_COLUMN_MAPPING.keys()),  # Use keys from the mapping
    )

    if not all(column in df for column in PLAYER_COLUMN_MAPPING.keys()):
        raise ValueError(
            "One or more required columns in BrightSign Index are missing."
        )

    player_instances = []
    for _, row in df.iterrows():
        player_kwargs = {
            PLAYER_COLUMN_MAPPING[col]: row[col] for col in PLAYER_COLUMN_MAPPING
        }
        player_instances.append(Player(**player_kwargs))

    return player_instances


def get_player_name_from_serial(serial_number):
    index_path = get_data_from_config("file_paths", "player_index_path")
    df = pd.read_excel(
        str(index_path), sheet_name="Players", usecols=["Serienummer", "Navn"]
    )
    player_name = df.loc[df["Serienummer"] == serial_number, "Navn"].values[0]
    return player_name


def send_email(subject: str, message: str):
    # Set up the SMTP server
    smtp_server = get_data_from_config("mail", "email_server")
    smtp_port = get_data_from_config("mail", "email_port")
    smtp_username = get_data_from_config("mail", "email_from")
    smtp_password = get_data_from_config("mail", "email_password")
    mail_recipient = get_data_from_config("mail", "email_to")

    # Set up the email message
    msg = MIMEMultipart()
    msg["From"] = get_data_from_config("mail", "email_from")
    msg["To"] = mail_recipient
    msg["Subject"] = subject
    body = message
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, mail_recipient, msg.as_string())


def write_to_csv(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False)
    print(f"CSV file '{filepath}' generated successfully.")
