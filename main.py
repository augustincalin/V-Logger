import network
import machine
from microdot import Microdot, Response
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


# Connect to Wi-Fi
app = Microdot()

html = '''
    <!DOCTYPE html>
    <html lang="en">

    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>VLogger</title>
      <style>
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: Arial, sans-serif;
          display: flex;
          flex-direction: column;
          min-height: 100vh;
        }

        header {
          position: fixed;
          top: 0;
          width: 100%;
          background-color: #3b2abd;
          color: white;
          padding: 10px 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          z-index: 1000;
        }

        header .controls {
          display: flex;
          align-items: center;
          gap: 10px;
        }

        header select,
        header button {
          width: 100px;
          padding: 5px 10px;
          background: rgba(255, 255, 255, 0.2);
          color: white;
          border: 2px solid rgba(255, 255, 255, 0.4);
          border-radius: 10px;
          backdrop-filter: blur(10px);
          cursor: pointer;
          transition: background 0.3s, border 0.3s;
        }

        header select option {
          color: black;
        }

        header select:hover,
        header button:hover {
          background: rgba(255, 255, 255, 0.3);
          border: 2px solid rgba(255, 255, 255, 0.6);
        }

        main {
          margin-top: 70px;
          padding: 20px;
          flex: 1;
        }

        .list {
          width: 300px;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .list-item {
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 5px;
          background-color: #f9f9f9;
          display: flex;
        }

        .list-item .time {
          flex: 1;
        }

        .list-item .value {
          flex: 1;
          text-align: right;
        }

        footer {
          color: rgb(95, 95, 95);
          text-align: center;
          padding: 10px 0;
        }

        .title {
          font-size: 1.5rem;
        }

        .day-selector {
          width: 150px;
        }

        a, a:visited{
          text-decoration: none;
          color: white;
        }
        a:hover{
          text-decoration: underline;
        }
      </style>
    </head>

    <body>
      <header>
        <div class="title">Voltage Logger</div>
        <div class="controls">
          <select id="dropdown" class="day-selector">
            <option value="">(wait...)</option>
          </select>
          <button>Read now</button>
          <button>Delete all</button>
          <button>Reset</button>
        </div>
      </header>

      <main>
        <div class="list" id="list-container">
          <p>Select a file</p>
        </div>
      </main>

      <footer><a href="https://github.com/augustincalin/V-Logger" target="_blank">Made by Gusti 2024 (Christmas holiday)</a>
      </footer>

      <script>
        async function fetchFileNames() {
          const apiUrl = `http://vlogger.local/days`;

          try {
            // Make a GET request to the Microdot API
            const response = await fetch(apiUrl);

            // Check if the response is OK
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Parse the JSON response
            const data = await response.json();

            // Check for errors in the JSON response
            if (data.error) {
              console.error(`API Error: ${data.error}`);
              return [];
            }

            // Process the file names and remove their extensions
            const fileNames = data.files.map(file => {
              const dotIndex = file.lastIndexOf('.');
              return dotIndex > 0 ? file.substring(0, dotIndex) : file; // Remove extension
            });

            return fileNames;
          } catch (error) {
            console.error(`Failed to fetch file names: ${error.message}`);
            return [];
          }
        }

        async function fetchFileContent(day) {
          console.log(day);
          const apiUrl = `http://vlogger.local/day/${day}`;

          try {
            // Make a GET request to the Microdot API
            const response = await fetch(apiUrl);

            // Check if the response is OK
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Parse the JSON response
            const data = await response.json();

            // Check for errors in the JSON response
            if (data.error) {
              console.error(`API Error: ${data.error}`);
              return [];
            }

            // Process the file names and remove their extensions
            const content_lines = data.values.map(line => {
              const items = line.split(' ');
              return {
                time: items[0],
                value: items[1]
              }
            });

            return content_lines;
          } catch (error) {
            console.error(`Failed to fetch file content: ${error.message}`);
            return [];
          }

        }

        document.addEventListener("DOMContentLoaded", async () => {
          const fileNames = await fetchFileNames();

          const day_selector = document.getElementById("dropdown");
          day_selector.innerHTML = `<option value="">..select:</option>` + fileNames.map((item) => `<option value="${item}">${item}</option>`);
        });

        document.getElementById("dropdown")
          .addEventListener("change", async function() {
            const selectedValue = this.value;
            const listContainer = document.getElementById("list-container");

            let items = [];
            if (selectedValue !== "") {
              items = await fetchFileContent(selectedValue);
            }

            listContainer.innerHTML = '<div class="list-item"><span class="time">Time</span><span class="value">Value</span></div>' + items
              .map((item) => `<div class="list-item"><span class="time">${item.time}</span><span class="value">${item.value}</span></div>`).join("");
          });
      </script>
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

@app.route('/days')
def list_files(request):
    try:
        
        files = sd_card_module.list_log_files()
        return ujson.dumps({"files": files}), 200, {'Content-Type': 'application/json'}
    except OSError as e:
        return ujson.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/day/<day>')
def list_files(request, day):
    try:
        content = sd_card_module.read_log_file(f"{day}.txt")
        return ujson.dumps({"values": content}), 200, {'Content-Type': 'application/json'}
    except OSError as e:
        return ujson.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}


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
        print("Failed to retrieve Wi-Fi credentials.")

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(port=80, debug=True)

