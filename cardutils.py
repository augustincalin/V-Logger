import machine
import os
import globals

# Initialize the SD card
def initialize_sdcard():
    try:
        # Use machine.SDCard with SPI interface
        sd = machine.SDCard(slot=2, sck=18, mosi=23, miso=19, cs=5, freq=500000)  # Match your pin configuration
        vfs=os.VfsFat(sd)
        os.mount(vfs, "/sd")
        print("SD card mounted successfully.")
        print(os.listdir("/sd"))
        return True
    except Exception as e:
        print("Failed to mount SD card:", e)
        return False

def check_and_create_config_file():
    """Checks if the Wi-Fi config file exists and creates one if it doesn't."""
    file_path = "wifi_config.txt"
    try:
        if file_path not in os.listdir("/sd"):
            print("Config file not found. Creating a new one with default values...")
            with open(file_path, "w") as file:
                file.write(f"SSID={globals.DEFAULT_SSID}\n")
                file.write(f"PASSWORD={globals.DEFAULT_PASSWORD}\n")
            print(f"Config file created at {file_path}")
        else:
            print("Config file already exists.")
    except Exception as e:
        print("Error while checking or creating config file:", e)

def read_wifi_credentials():
    """Reads Wi-Fi credentials from the config file."""
    file_path = "/sd/wifi_config.txt"
    try:
        with open(file_path, "r") as file:
            credentials = {}
            for line in file:
                if "=" in line:
                    key, value = line.strip().split("=")
                    credentials[key] = value
            return credentials.get("SSID"), credentials.get("PASSWORD")
    except Exception as e:
        print("Error reading Wi-Fi credentials:", e)
        return None, None