import re
import csv
import os

from utilities import get_data_from_config

headers = [
    "PlayerSerialNumber",
    "LogType",
    "Timestamp",
    "ZoneName",
    "StartTime",
    "EndTime",
    "ContentType",
    "ContentName",
    "StateName",
    "EventType",
    "EventData",
    "StateType",
    "PreviousState",
    "PreviousEventType",
    "PreviousEventData",
]


def get_processed_files(log_file):
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            processed_files = {line.strip() for line in file}
    else:
        processed_files = set()
    return processed_files


# Function to extract player serial number and date from the file name
def extract_info_from_filename(filename):
    pattern = r".*BrightSignLog\.(\w+)-(\d{6}).*\.log"
    match = re.search(pattern, filename)
    if match:
        serial_number = match.group(1)
        log_date = match.group(2)
        return serial_number, log_date
    return None, None


# Function to parse logs from a single file and append to the csv writer
def parse_log_file(file_path, csv_writer):
    serial_number, log_date = extract_info_from_filename(os.path.basename(file_path))
    if not serial_number:
        return  # Skip if the filename pattern does not match

    with open(file_path, "r") as file:

        for line in file:
            line = line.strip()
            if "L=p" in line:
                process_playback_log(line, csv_writer, serial_number, log_date)
            elif "L=e" in line:
                process_event_log(line, csv_writer, serial_number, log_date)
            elif "L=s" in line:
                process_state_log(line, csv_writer, serial_number, log_date)


# Processing playback logs
def process_playback_log(line, csv_writer, serial_number, log_date):
    data = {
        "PlayerSerialNumber": serial_number,
        "LogType": "Playback",
        "Timestamp": None,
        "ZoneName": None,
        "StartTime": None,
        "EndTime": None,
        "ContentType": None,
        "ContentName": None,
    }
    fields = line.split("\t")
    for field in fields:
        if "=" in field:
            key, value = field.split("=", 1)
            if key == "Z":
                data["ZoneName"] = value
            elif key == "S":
                data["StartTime"] = value
            elif key == "E":
                data["EndTime"] = value
            elif key == "I":
                data["ContentType"] = value
            elif key == "N":
                data["ContentName"] = value
    data["Timestamp"] = data["StartTime"]
    csv_writer.writerow(data)


# Processing event logs
def process_event_log(line, csv_writer, serial_number, log_date):
    data = {
        "PlayerSerialNumber": serial_number,
        "LogType": "Event",
        "Timestamp": None,
        "StateName": None,
        "EventType": None,
        "EventData": None,
    }
    fields = line.split("\t")
    for field in fields:
        if "=" in field:
            key, value = field.split("=", 1)
            if key == "S":
                data["StateName"] = value
            elif key == "T":
                data["Timestamp"] = value
            elif key == "E":
                data["EventType"] = value
            elif key == "D":
                data["EventData"] = value
    csv_writer.writerow(data)


# Processing state logs
def process_state_log(line, csv_writer, serial_number, log_date):
    data = {
        "PlayerSerialNumber": serial_number,
        "LogType": "State",
        "Timestamp": None,
        "StateName": None,
        "StateType": None,
        "PreviousState": None,
        "PreviousEventType": None,
        "PreviousEventData": None,
    }
    fields = line.split("\t")
    for field in fields:
        if "=" in field:
            key, value = field.split("=", 1)
            if key == "S":
                data["StateName"] = value
            elif key == "T":
                data["Timestamp"] = value
            elif key == "Y":
                data["StateType"] = value
            elif key == "LS":
                data["PreviousState"] = value
            elif key == "LE":
                data["PreviousEventType"] = value
            elif key == "LD":
                data["PreviousEventData"] = value
    csv_writer.writerow(data)


def update_processed_files(log_file, filename):
    with open(log_file, "a") as file:
        file.write(filename + "\n")


# Main function to orchestrate log parsing and CSV writing
def main(log_directory: str, output_csv_path: str, processed_log_file: str):
    processed_files = get_processed_files(processed_log_file)

    with open(output_csv_path, "a", newline="") as csv_file:  # Open in append mode
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        if os.stat(output_csv_path).st_size == 0:  # If file is empty, write header
            writer.writeheader()

        for dirpath, dirnames, filenames in os.walk(log_directory):
            for filename in filenames:
                if filename not in processed_files:
                    file_path = os.path.join(dirpath, filename)
                    parse_log_file(file_path, writer)
                    update_processed_files(processed_log_file, filename)

    print("Log aggregation completed.")


log_parent_folder = get_data_from_config("file_paths", "log_parent_folder")
aggregated_log_file = get_data_from_config("file_paths", "aggregated_logs_path")
processed_logs = get_data_from_config("file_paths", "processed_logs_path")

main(log_parent_folder, aggregated_log_file, processed_logs)
