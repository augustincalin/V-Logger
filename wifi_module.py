import network
import machine
import settings

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.config(dhcp_hostname = settings.Settings.get("hostname"))
    wlan.connect(ssid, password)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        machine.idle()  # Save power while waiting
    print("Connected to Wi-Fi:", wlan.ifconfig())