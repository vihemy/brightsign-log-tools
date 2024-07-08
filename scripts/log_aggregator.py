import re
import csv
import os

from utilities import get_data_from_config
from reporter import Reporter

REPORT_NAME = "LogAggregatorReport"
report_content = ""

# Load configuration settings
log_parent_folder = get_data_from_config("file_paths", "log_parent_folder")
aggregated_log_file = get_data_from_config("file_paths", "aggregated_logs_path")
processed_logs = get_data_from_config("file_paths", "processed_logs_path")

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

FILENAME_PATTERN = re.compile(r".*BrightSignLog\.(\w+)-(\d{6}).*\.log")


def get_processed_files(log_file):
    """Retrieves set of previously processed file names from a log file."""
    processed_files = set()
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            processed_files = {line.strip() for line in file}
    return processed_files


def extract_info_from_filename(filename):
    """Extracts player serial number and log date from filename."""
    match = FILENAME_PATTERN.search(filename)
    if match:
        return match.group(1), match.group(2)
    return None, None


def parse_log_file(file_path, csv_writer):
    """Parses a log file and processes different types of log entries."""
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


def process_playback_log(line, csv_writer, serial_number, log_date):
    """Processes playback logs and writes data to a CSV file."""
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


def process_event_log(line, csv_writer, serial_number, log_date):
    """Processes event logs and writes data to a CSV file."""
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


def process_state_log(line, csv_writer, serial_number, log_date):
    """Processes state logs and writes data to a CSV file."""
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
            value = value.strip()
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
    """Updates log file with new entries of processed files."""
    with open(log_file, "a") as file:
        file.write(filename + "\n")


def save_and_send_report(name: str, content: str):
    reporter = Reporter(name, content)
    reporter.save_to_file()
    reporter.send_as_email()


def main(log_directory: str, output_csv_path: str, processed_log_file: str):
    """Orchestrates log parsing and CSV writing for an entire directory of log files."""
    processed_files = get_processed_files(processed_log_file)

    with open(output_csv_path, "a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        if os.stat(output_csv_path).st_size == 0:
            writer.writeheader()

        for dirpath, dirnames, filenames in os.walk(log_directory):
            for filename in filenames:
                if filename not in processed_files:
                    file_path = os.path.join(dirpath, filename)
                    parse_log_file(file_path, writer)
                    update_processed_files(processed_log_file, filename)

    report_content = f"Log aggregation complete.\nOutput path: {output_csv_path}.\nTotal nr. of log-files aggregated: {len(get_processed_files(processed_log_file))}"
    print(report_content)
    return report_content


if __name__ == "__main__":
    try:
        report_content = main(log_parent_folder, aggregated_log_file, processed_logs)
    except Exception as e:
        report_content = f"Error aggregating logs: {e}"
    finally:
        print(report_content)
        save_and_send_report(REPORT_NAME, report_content)
