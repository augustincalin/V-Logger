# Instructions
Edit appsettings.json and copy it to SD card.

## Variables
| Name | Purpose | Default
|-----|-----|----|
| ssid | name of wifi network you want to connect to | YOUR_WIFI |
| password | the password for the above | YOUR_WIFI_PASSWORD |
| hostname | the name where the web app is accessible. If you set it to a value like `abc`, you have to navigate to `http://abc.local` | vlogger |
| adc_pin | pin on ESP32 board where you connect the OUT pin from the ZMPT101B circuit | 34 |
| min_voltage | the value that will trigger an alert if the measured voltage is smaller | 210 |
| max_voltage | if the measured voltage is bigger than this, an alert is also triggered | 240 |
| calibration_factor | adjust this until the value read by VLogger is equal with the value read by voltmeter | 323 |
| alert_url | IFTTT url for sending alerts | https://maker.ifttt.com/trigger/voltage_drop/json/with/key/{YOUR_IFTT_KEY} |
| num_samples | Number of reads to measure the voltage. Increase for better accuracy | 3000 |
| read_time | read voltage interval in seconds | 60 |
| logs_path | path where logs will be saved | /sd/logs" |

