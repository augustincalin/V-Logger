import ntptime
import machine

def init_time():
    ntptime.settime()
    rtc = machine.RTC()
    print("Time retrieved from NTP server: ", rtc.datetime())