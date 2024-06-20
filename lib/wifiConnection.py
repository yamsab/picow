import keys
import network
from time import sleep
from machine import Pin


led = Pin("LED", Pin.OUT)


def connect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            led.on()
            sleep(0.2)
            led.off
            sleep(0.8)
            print('.', end='')
    if wlan.isconnected():
        print("Wifi connected")
        led.on
         # Print the IP assigned by router
        ip = wlan.ifconfig()[0]
        print('\nConnected on {}'.format(ip))
        return ip
    else:
        led.off()
        print("Wifi disconnected")

def disconnect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    wlan.disconnect()
    wlan = None 
    led.off()
    print("Wifi disconnected")