import network
import machine
from microdot import Microdot
import os
import socket



# Connect to Wi-Fi
DEFAULT_SSID = "HUAWEI-1040W3"
DEFAULT_PASSWORD = "erdal123"
DEFAULT_HOSTNAME = "vlogger"

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
                file.write(f"SSID={DEFAULT_SSID}\n")
                file.write(f"PASSWORD={DEFAULT_PASSWORD}\n")
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

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.config(dhcp_hostname = DEFAULT_HOSTNAME)
    wlan.connect(ssid, password)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        machine.idle()  # Save power while waiting
    print("Connected to Wi-Fi:", wlan.ifconfig())


app = Microdot()

html = '''<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
            <p><a href="/shutdown">Click to shutdown the server</a></p>
        </div>
    </body>
</html>
'''


@app.route('/')
async def hello(request):
    return html, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

if initialize_sdcard():
    check_and_create_config_file()  # Ensure config file exists
    ssid, password = read_wifi_credentials()  # Read credentials
    if ssid and password:
        connect_to_wifi(ssid, password)  # Connect to Wi-Fi
    else:
        print("Failed to retrieve Wi-Fi credentials.")
    app.run(port=80, debug=True)