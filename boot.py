from time import sleep_ms, ticks_ms
import network
import urequests
import json
import utime
from machine import RTC, I2C, Pin

SSID = "ASUS"
PASSWORD = "1234567890"
port = 100
wlan = None
s = None
url = "http://worldtimeapi.org/api/timezone/Europe/Moscow"

web_query_delay = 60000  # interval time of web JSON query
retry_delay = 5000  # interval time of retry after a failed Web query
rtc = RTC()
update_time = utime.ticks_ms() - web_query_delay
if utime.ticks_ms() - update_time >= web_query_delay:
    response = urequests.get(url)
if response.status_code == 200:  # query success
    print("JSON response:\n", response.text)

    # parse JSON
    parsed = response.json()
    datetime_str = str(parsed["datetime"])
    year = int(datetime_str[0:4])
    month = int(datetime_str[5:7])
    day = int(datetime_str[8:10])
    hour = int(datetime_str[11:13])
    minute = int(datetime_str[14:16])
    second = int(datetime_str[17:19])
    subsecond = int(round(int(datetime_str[20:26]) / 10000))

    # update internal RTC
    rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
    update_time = utime.ticks_ms()
    print("RTC updated\n")

else:  # query failed, retry retry_delay ms later
    update_time = utime.ticks_ms() - web_query_delay + retry_delay
date_str = "Date: {1:02d}/{2:02d}/{0:4d}".format(*rtc.datetime())
time_str = "Time: {4:02d}:{5:02d}:{6:02d}".format(*rtc.datetime())


def connectWifi(ssid, passwd):  # function to connect to the Web
    global wlan  # declare a WLAN object
    wlan = network.WLAN(network.STA_IF)  # create a wlan object
    wlan.active(True)  # Activate the network interface
    wlan.disconnect()  # Disconnect the last connected WiFi
    wlan.connect(ssid, passwd)  # connect wifi
    while (wlan.ifconfig()[0] == '0.0.0.0'):  # wait for connection
        sleep_ms(1)
    sleep_ms(1000)  # hold on for 1 second
    sendmessage("Connected to WLAN")
    sleep_ms(1000)  # hold on for 1 second
    return True


def sendmessage(myMessage):
    url = "http://192.168.1.24:5000/"
    headers = {'content-type': 'application/json'}
    data = {'message': myMessage}
    jsonObj = json.dumps(data)
    resp = urequests.post(url, data=jsonObj, headers=headers)
    return True


def main():
    connectWifi(SSID, PASSWORD)
    while True:
        meta = {
            str(date_str),
            str(time_str)
        }
        sendmessage(meta)
        sleep_ms(1000)


main()
