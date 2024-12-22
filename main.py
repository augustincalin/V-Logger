import network
import machine
from microdot import Microdot
import os
import socket
import cardutils
import wifi_utils



# Connect to Wi-Fi
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

if cardutils.initialize_sdcard():
    cardutils.check_and_create_config_file()  # Ensure config file exists
    ssid, password = cardutils.read_wifi_credentials()  # Read credentials
    if ssid and password:
        wifi_utils.connect_to_wifi(ssid, password)  # Connect to Wi-Fi
    else:
        print("Failed to retrieve Wi-Fi credentials.")
    app.run(port=80, debug=True)