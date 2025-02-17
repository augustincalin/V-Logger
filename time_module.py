import ntptime
import machine
import socket
import time

def init_time():

    for attempt in range(5):
        try:
            print(f"Attempt {attempt+1} to sync time...")
            ntptime.settime()
            rtc = machine.RTC()
            print("Time retrieved from NTP server: ", rtc.datetime())
            return
        except OSError as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(3)

    print("Failed to sync time after multiple attempts.")
