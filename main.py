import network
import machine
from microdot import Microdot
import os
import socket
import uasyncio as asyncio
import sd_card_module
import wifi_module
import voltage_module
import globals
import alert_module
import time_module


# Connect to Wi-Fi
app = Microdot()

html = '''<!DOCTYPE html>
<html>
    <head>
        <title>V-Logger</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <div>
            <h1>History</h1>
            <p>Here you can see the historical data:</p>
            <ul>
                <li>
                    <div class="history-item">
                        <div class="date">13.12.2024</div>
                        <div class="value">210</div>
                    </div>
                </li>
            </ul>
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

async def main():

    while True:
        voltage = voltage_module.read_voltage()
        sd_card_module.write_value(voltage)

        # Check if voltage is outside the specified range
        if voltage < globals.MIN_VOLTAGE or globals.voltage > MAX_VOLTAGE:
            alert_module.send_alert(voltage)

        await asyncio.sleep(globals.READ_TIME)

if sd_card_module.initialize_sdcard():
    sd_card_module.check_and_create_config_file()  # Ensure config file exists
    ssid, password = sd_card_module.read_wifi_credentials()  # Read credentials
    if ssid and password:
        wifi_module.connect_to_wifi(ssid, password)  # Connect to Wi-Fi
        time_module.init_time()
    else:
        print("Failed to retrieve Wi-Fi credentials.")

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(port=80, debug=True)
