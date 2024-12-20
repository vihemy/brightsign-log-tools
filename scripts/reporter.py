import os
from utilities import get_app_folder, get_date2, send_email, create_directory


class Reporter:
    def __init__(self, name: str, content: str):
        self.name = f"{name}.{get_date2()}"
        self.content = content

    def save_to_file(self):
        """Export a given report to a log file."""
        app_dir = get_app_folder()
        report_dir = os.path.join(app_dir, "reports")
        report_file = os.path.join(report_dir, f"{self.name}.log")
        create_directory(report_dir)

        with open(report_file, "w") as file:
            file.write(self.content)

    def send_as_email(self, onlyErrors: bool):
        """
        Send the report as an email.

        Args:
            onlyErrors (bool): If True, only send the report if it contains errors.
        """
        if onlyErrors:
            if "Error" in self.content:
                send_email(self.name, self.content)
        else:
            send_email(self.name, self.content)
