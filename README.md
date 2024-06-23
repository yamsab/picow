Temperature and Humidity Sensor Tutorial
Author

Yama Sabit (ys222fh)
Project Overview

This project involves creating a temperature and humidity sensor using a Raspberry Pi Pico, a DHT11 sensor, and an MQTT broker to publish the data to Adafruit IO. The estimated time to complete this project is approximately 4-6 hours.
Objective
Why This Project?

I chose to build this temperature and humidity sensor to monitor environmental conditions in real-time. This data can be useful for various applications such as home automation, weather monitoring, and agricultural purposes.
Purpose

The main purpose of this project is to gather real-time temperature and humidity data and publish it to an online dashboard for remote monitoring.
Insights

This project will provide insights into the environmental conditions of a specific area, helping to understand trends and make informed decisions based on the data collected.
Materials
Materials
List of Materials

Purchased from Electrokit Sweden AB as part of a startup kit:

    1x Raspberry Pi Pico WH (Artikelnr: 41019114)
    1x Breadboard 840 connections (Artikelnr: 10160840)
    1x USB cable A-male to micro B 5-pin male 1.8m (Artikelnr: 41003290)
    20x Jumper wires 30cm male/male (Artikelnr: 41012684)
    10x Jumper wires 30cm female/male (Artikelnr: 41012686)
    10x Resistors 0.25W 330Ω (Artikelnr: 40810233)
    10x Resistors 0.25W 560Ω (Artikelnr: 40810256)
    10x Resistors 0.25W 1kΩ (Artikelnr: 40810310)
    10x Resistors 0.25W 10kΩ (Artikelnr: 40810410)
    5x LED 5mm red diffuse 1500mcd (Artikelnr: 40307020)
    5x LED 5mm yellow diffuse 1500mcd (Artikelnr: 40307021)
    5x LED 5mm green diffuse 80mcd (Artikelnr: 40307023)
    2x Photoresistor CdS 4-7kΩ (Artikelnr: 40850001)
    1x Tilt switch (Artikelnr: 41004308)
    1x MCP9700 TO-92 Temperature sensor (Artikelnr: 41011628)
    1x TLV49645 SIP-3 Hall-effect sensor digital (Artikelnr: 41015964)
    1x Magnet Neo35 Ø5mm x 5mm (Artikelnr: 41011480)
    1x Digital temperature and humidity sensor DHT11 (Artikelnr: 41015728)

Total Cost: 399 SEK (excluding tax and shipping)
Specifications and Costs

    Raspberry Pi Pico: Microcontroller with multiple GPIO pins.
    DHT11 Sensor: Measures temperature and humidity.
    LEDs: Indicators for different temperature ranges.
    Jumper Wires: For connections.
    Breadboard: For prototyping.
    Power Supply: 5V USB power source.

Computer Setup
Chosen IDE

I used the Thonny IDE, which is specifically designed for MicroPython and works seamlessly with the Raspberry Pi Pico.
Steps to Setup

    Install Thonny IDE: Download and install from Thonny.org.
    Flash MicroPython Firmware:
        Connect the Pico to your computer while holding the BOOTSEL button.
        Download the latest MicroPython firmware from MicroPython.org.
        Drag and drop the firmware onto the Pico.

Required Installations

    Node.js: For additional package installations if needed.
    Drivers: Ensure USB drivers for Pico are installed.

Putting Everything Together
Circuit Diagram

Electrical Connections

    Connect DHT11 sensor to GPIO27.
    Connect the magnet sensor to GPIO26.
    Connect LEDs to GPIO2 (Red), GPIO3 (Yellow), GPIO4 (Blue), and GPIO5 (White).

Platform
Platform Choice

I chose Adafruit IO for its ease of use and integration with MQTT. It offers a free tier that is sufficient for small-scale projects and allows easy scaling if needed.
Platform Details

    Functionality: Real-time data monitoring and visualization.
    Cost: Free tier available with options to upgrade.

The Code
Core Functions

python

import time
import gc
from machine import ADC, unique_id, Pin
import ubinascii
from lib.umqtt_simple import MQTTClient
import lib.keys as keys
import dht

# Initialize Pins
redLight = Pin(2, Pin.OUT)
yellowLight = Pin(3, Pin.OUT)
blueLight = Pin(4, Pin.OUT)
whitelight = Pin(5, Pin.OUT)

# Initialize ADC
dht_sensor = dht.DHT11(Pin(27))
magnetSensor = Pin(26, mode=Pin.IN)

# MQTT publish function for the pico to adafruit
def publish_data(client, feed, data):
    try:
        client.connect()
        client.publish(feed, str(data))
        client.disconnect()
    except Exception as e:
        print('Failed to publish data:', e)

# Read temperature from the DHT11 sensor
def read_temperature_and_humidity():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
        return temp, humidity
    except Exception as e:
        print('Failed to read from DHT sensor:', e)
        return None, None

def readMagnet():
    try:
        value = magnetSensor.value()
        print(f"Magnet Sensor Value : {value}")
        whitelight.value(1 if value else 0)
        return value
    except Exception as e:
        print("Failed to print the data from magnet sensor")
        return None

def lightstemp(temp):
    if temp > 20:
        redLight.value(1)
        yellowLight.value(0)
        blueLight.value(0)
    elif temp < 0:
        yellowLight.value(1)
        redLight.value(0)
        blueLight.value(0)
    elif temp > 10 and temp < 20:
        blueLight.value(1)
        redLight.value(0)
        yellowLight.value(0)
    elif temp == 0:
        redLight.value(1)
        yellowLight.value(1)
    else:
        redLight.value(0)
        yellowLight.value(0)

def main():
    client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)
    client.connect()
    print('Connected to MQTT broker')
    
    while True:
        temp, humidity = read_temperature_and_humidity()
        if temp is not None:
            lightstemp(temp)
            publish_data(client, keys.AIO_TEMP_FEED, temp)
            publish_data(client, keys.AIO_humidity_FEED, humidity)

        magnet_value = readMagnet()
        if magnet_value:
            publish_data(client, keys.AIO_MAGNET_FEED, magnet_value)

        time.sleep(10)  # Publish data every 10 seconds
        gc.collect()

if __name__ == '__main__':
    main()

Explanation

    publish_data: Connects to the MQTT broker and publishes data.
    read_temperature_and_humidity: Reads temperature and humidity from the DHT11 sensor.
    readMagnet: Reads the value from the magnet sensor and controls the white LED.
    lightstemp: Controls the LEDs based on the temperature.
    main: Main function that initializes the MQTT client and continuously reads sensor data and publishes it.

Transmitting the Data / Connectivity
Data Transmission

    Frequency: Data is sent every 10 seconds.
    Protocols:
        Wireless: WiFi
        Transport: MQTT

Design Choices

Choosing WiFi and MQTT ensures reliable data transmission over the internet and is suitable for real-time applications.
Presenting the Data
Dashboard

Data is visualized on Adafruit IO with customizable dashboards. Data is preserved for historical analysis.
Visual Example

Finalizing the Design
Final Results

The project successfully monitors and publishes temperature and humidity data. The LEDs provide a quick visual indication of temperature ranges.
Final Thoughts

The project was successful and can be extended with additional sensors or functionality. Future improvements could include adding a web interface for easier monitoring and control.
