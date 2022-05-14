import json
import time
import requests
import serial

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while 1:
    x = ser.readline().decode()
    line = x.strip()
    if len(line) > 0:
        if line[0] == '{' and line[-1] == '}':
            slovar = json.loads(line)
            id_luc = slovar['from']
            vsebina = slovar['msg']

            if 'duration' in vsebina:
                duration = vsebina['duration']
            else:
                duration=0

            if 'humidity' in vsebina:
                humidity = vsebina['humidity']
            else:
                humidity = 0
            if 'pressure' in vsebina:
                pressure = vsebina['pressure']
            else:
                pressure = 0
            if 'brightness' in vsebina:
                brightness = vsebina['lux']
            else:
                brightness = 0
            if 'temperature' in vsebina:
                temperature = vsebina['temperature']
            else:
                temperature = "0"
            url = "http://127.0.0.1:8001/add/pass/?id={}&duration={}&temperature={}&brightness={}&humidity={}&pressure={}".format(
                id_luc, duration,
                temperature, brightness, humidity, pressure)
            poslji = requests.get(url)
            print(poslji.text)
