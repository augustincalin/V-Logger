import network
import machine
import settings
import time

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)
    time.sleep(0.5)
    wlan.disconnect()
    time.sleep(0.5)
    wlan.connect(ssid, password)
    wlan.config(dhcp_hostname = settings.Settings.get("hostname"))
    print (f"Connecting to WiFi {ssid}")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)

    print("Connected to WiFi:", wlan.ifconfig())