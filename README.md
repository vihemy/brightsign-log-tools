# Brightsign Player Log Tools
Scripts to download and process player logs from BrightSign mediaplayers configured on a local network using Local Diagnostic Web Server.

I created this tool to streamline the process of downloading logs from BrightSign players on a local network. Since the `brightsign_index` serves as a shared overview with non-technical colleagues, it is formatted as an `.xlsx` file.

I run both `main.py` and `log_aggregator.py` as cron jobs (both scripts are built as `.exe` files using PyInstaller) on Windows 10.

## Notes
- Works with BrightSign players with local network configuration.
- The tool collects the player logs in sd/logs/ folder in the player's file system. NOT the diagnostic log.
- It does not currently support dealing with authentication when connecting to BrightSign players.
- Has also been tested on Windows 10 and 11.

## How It Works
1. **Player Information**: `main.py` loads information about the BrightSign players from `brightsign_index.xlsx`. (This file is in Excel format to accommodate non-technical users who interact with the system.)
2. **Log Downloading**: Using IP addresses from `brightsign_index.xlsx`, `main.py` calls `log_downloader.py` to download log files from each player to a specified local directory. (You can configure the local download directory in `config.ini` by setting the `log_parent_folder` key.)
3. **Reporting**: `main.py` then uses `reporter.py` to generate and email a report of the downloaded logs to a specified address.
4. **Log Aggregation**: `log_aggregator.py` can be used to combine logs from multiple players into a single file, making it easier to analyze in applications like Excel or Power BI.

### Setting Up BrightSign Player Information
- Enter IP addresses, names, and serial numbers of your BrightSign players in `brightsign_index_template.xlsx`.
- Set the **Log-indsamling** column to `TRUE` for each player you want to include in log collection.
- Note: Headers in `brightsign_index_template.xlsx` are currently in Danish and should not be changed, as the script relies on these headers to function correctly.

### Configuration
In `config.ini`, you can set the following parameters:
- **log_parent_folder**: Specify the directory where logs will be saved.
- **email settings**: Configure recipient email addresses and SMTP settings for sending reports (add specific keys if applicable).

## Dependencies
- **pandas**
- **requests**

> To install the required dependencies, you can use:
> ```bash
> pip install pandas requests
> ```

