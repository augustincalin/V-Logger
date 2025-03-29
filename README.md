# V-Logger
Voltage logger for max 250V~.

![Outside](/doc_images/outside.jpg "Outside")

## How it works
Plug the device and turn on the switch.

![Plug](/doc_images/plug.jpg "Plug")

> Eventually, you will want to adjust the settings before (wifi, password,...). To do this you will have to edit the appsettings.json (see [README.md](/sd/README.md) for details).

After a while (1-2min) the V-Logger will start and you can access it in your browser (default address http://vlogger.local).

At specified interval of time the voltage is read and written in a log file. If the value is smaller or greater than the specified values then an alert is sent via IFTTT.

A new log file is created each hour; the time is UTC.

## Hardware
1 ESP32
1 microSD Card module
1 ZMPT101B
1 Power adapter 5V 2A
2 Fuses 250V AC, 0.5A

### Wiring
| ESP32 | | ZMPT101B | | microSD module | | ESP32 |
|---|---|---|---|--|--|--|
| 3.3V | → | VCC || VCC | ← | 3.3V |
| GND | → | GND || GND | ← | GND |
| GPIO 32 | → | OUT || MISO | ← | GPIO 19 |
|  |  |  || MOSI | ← | GPIO 23 |
|  |  |  || SCK | ← | GPIO 18 |
|  |  |  || CS | ← | GPIO 5 |

![Inside](/doc_images/inside.jpg "Inside")
> Ignore the mess. This is my first time when I soldered.

## Software
- micropython
- Thonny
- microdot

# Thanks
Special thanks to [ChatGPT](https://chatgpt.com). Without it this project wouldn't exist.

# Things to improve
⬜ the log files are created indefinitely. They should be removed after a while.

