import re
import csv
import os


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


# Main function to orchestrate log parsing and CSV writing
def aggregate_logs_to_csv(log_directory, output_csv_path):
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

    with open(output_csv_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        # Iterate through all files in the directory
        for filename in os.listdir(log_directory):
            file_path = os.path.join(log_directory, filename)
            parse_log_file(file_path, writer)


aggregate_logs_to_csv("C:/Users/vhm/Desktop/test", "C:/Users/vhm/Desktop/output.csv")
