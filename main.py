import network
import ubinascii
import machine
import time
from machine import Pin
from secrets import secrets
import socket
import gc

# Set country to avoid possible errors
rp2.country('DE')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()

ssid = secrets['ssid']
pw = secrets['pw']
wlan.connect(ssid, pw)

timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

wlan_status = wlan.status()

# Define blinking function for onboard LED to indicate error codes
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for _ in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)

blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP = ' + status[0])

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', status[0])

# Enable garbage collection
gc.enable()

# Run garbage collection every 10 requests
request_count = 10

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        r = cl.recv(1024)

        r = str(r)

        # Load html page directly instead of using get_html function
        with open('index.html', 'r') as file:
            response = file.read()

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')

