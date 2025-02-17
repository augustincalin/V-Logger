import network
import machine
from microdot import Microdot, Response, send_file
import os
import socket
import uasyncio as asyncio
import sd_card_module
import wifi_module
import voltage_module
import alert_module
import time_module
import ujson
import settings
import time_module

# Connect to Wi-Fi
app = Microdot()


@app.route('/')
async def hello(request):
    return send_file("/index.html")

@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

@app.route('/days')
def list_files(request):
    try:
        files = sd_card_module.list_log_files()
        return ujson.dumps({"files": files}), 200, {'Content-Type': 'application/json'}
    except OSError as e:
        return ujson.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/day/<day>')
def get_day(request, day):
    try:
        content = sd_card_module.read_log_file(f"{day}.txt")
        return ujson.dumps({"values": content}), 200, {'Content-Type': 'application/json'}
    except OSError as e:
        return ujson.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/reset')
def reset_machine(request):
    machine.reset()

@app.route('/clear')
def clear_logs(request):
    sd_card_module.delete_all_logs()

@app.route('/read')
def read_value(request):
    try:
        content = voltage_module.read_voltage()
        return ujson.dumps({"value": content}), 200, {'Content-Type': 'application/json'}
    except OSError as e:
        return ujson.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/favicon.ico')
async def static(request):
    return send_file('/favicon.ico', max_age=86400)

async def main():
    alert_count = 0
    previous_alert_voltage = -1
    while True:
        voltage = voltage_module.read_voltage()
        sd_card_module.write_value(voltage)

        # Check if voltage is outside the specified range
        if voltage < settings.Settings.get("min_voltage") or voltage > settings.Settings.get("max_voltage"):
            alert_count = alert_count + 1
            if previous_alert_voltage == -1:
                previous_alert_voltage = voltage

            if abs(voltage - previous_alert_voltage) > settings.Settings.get("allowed_diff") or alert_count > settings.Settings.get("alerts_count"):
                alert_module.send_alert(voltage, alert_count)
                alert_count = 0

            previous_alert_voltage = voltage

        await asyncio.sleep(settings.Settings.get("read_time"))

if sd_card_module.initialize_sdcard():
    settings.Settings.load()
    ssid = settings.Settings.get("ssid")
    password = settings.Settings.get("password")
    if ssid and password:
        wifi_module.connect_to_wifi(ssid, password)  # Connect to Wi-Fi
        time_module.init_time()
    else:
        print("Failed to retrieve WiFi credentials.")

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(port=80, debug=True)

 