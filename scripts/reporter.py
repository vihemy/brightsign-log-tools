import os
from utilities import get_app_folder, get_date2, send_email, create_directory

class Reporter:
    def __init__(self, data: str):
        self.name = f"LogDownloaderReport.{get_date2()}"
        self.data = data

    def save_to_file(self):
        """Export a given report to a log file."""
        app_dir = get_app_folder()
        report_dir = os.path.join(app_dir, "reports")
        report_file = os.path.join(report_dir, f"{self.name}.log")
        create_directory(report_dir)

        with open(report_file, "w") as file:
            file.write(self.data)

    def send_as_email(self):
        """Send a given report as an email."""
        send_email(self.name, self.data)
