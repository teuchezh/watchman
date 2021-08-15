import serial
import time
import datetime
import psutil
import json

# ___________________VARIABLES___________________#
# com = "/dev/ttyUSB0"
com = "COM3"
# _______________________________________________#

target = serial.Serial(com, 9600)


def uptime():
    upTime = datetime.timedelta(
        seconds=round(time.time() - psutil.boot_time()))
    return upTime


def get_data():
    data = {
        "uptime": str(uptime()),
        "timestamp": str(time.time()),
    }
    return json.dumps(data)


def main():
    while True:
        print(time.time())
        print(get_data().encode('ascii'))
        target.write(get_data().encode('ascii'))
        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Exited')
