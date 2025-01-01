import machine
import os
import time
import settings

# Initialize the SD card
def initialize_sdcard():
    try:
        # Use machine.SDCard with SPI interface
        sd = machine.SDCard(slot=2, sck=18, mosi=23, miso=19, cs=5, freq=500000)  # Match your pin configuration
        vfs=os.VfsFat(sd)
        os.mount(vfs, "/sd")
        return True
    except Exception as e:
        print("Failed to mount SD card:", e)
        return False

def file_or_dir_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

def write_value(value):
    """
    Writes a float value to an SD card file with the current timestamp.
    File name is the current date, and the data is appended at the beginning of the file.

    :param value: The float value to write to the file.
    """

    if not file_or_dir_exists(settings.Settings.get("logs_path")):
        print("making logs folder")
        os.mkdir(settings.Settings.get("logs_path"))

    # Get the current date and time
    current_time = time.localtime()
    print("Time: ", current_time)
    date_string = f"{current_time[0]:04d}-{current_time[1]:02d}-{current_time[2]:02d}-{current_time[3]:02d}"
    time_string = f"{current_time[3]:02d}:{current_time[4]:02d}:{current_time[5]:02d}"
    
    # SD card file path
    file_name = f"""{settings.Settings.get("logs_path")}/{date_string}.txt"""
    
    # Check if the file exists
    if file_or_dir_exists(file_name):
        # Read the existing content
        print("File exists", file_name)
        with open(file_name, "r") as file:
            content = file.read()
    else:
        # File does not exist; content is empty
        content = ""
    
    # New entry to be added
    new_entry = f"{time_string} {value:.2f}\n"

    # Write the new entry followed by the existing content
    with open(file_name, "w") as file:
        file.write(new_entry + content)

def list_log_files():
    """
    Lists all files in the '/sd/logs' folder in reverse order (most recent first).

    :return: A list of file names in reverse order.
    """

    # Check if the folder exists
    if not file_or_dir_exists(settings.Settings.get("logs_path")):
        print("Logs folder does not exist.")
        return ["(no files)"]

    # Get all files in the folder
    files = os.listdir(settings.Settings.get("logs_path"))

    # Filter only files that match the expected format (optional, for safety)
    log_files = [file for file in files if file.endswith(".txt")]

    # Sort files in reverse order (most recent first based on the YYYY-MM-DD naming convention)
    log_files.sort(reverse=True)

    return log_files

def read_log_file(file_name):
    """
    Reads and returns the content of a specified log file from the '/sd/logs' folder.

    :param file_name: The name of the file to read (e.g., '2024-12-24.txt').
    :return: The content of the file as a string, or an error message if the file doesn't exist.
    """

    file_path = f"""{settings.Settings.get("logs_path")}/{file_name}"""  # Full path to the file

    # Check if the file exists
    if not file_or_dir_exists(file_path):
        return f"File '{file_name}' does not exist in the logs folder."

    # Read and return the file content
    try:
        with open(file_path, "r") as file:
            lines = [line for line in file]
        return lines
    except Exception as e:
        return f"Error reading the file: {e}"

def delete_all_logs():
    try:
        # List all files in the folder
        path = settings.Settings.get("logs_path")
        files = os.listdir(path)
        for file in files:
            file_path = path + "/" + file
            os.remove(file_path)  # Delete the file
        print("All files deleted successfully!")
    except Exception as e:
        print("Error deleting files:", e)