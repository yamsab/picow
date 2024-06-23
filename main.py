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
#adc = ADC(27)
dht_sensor = dht.DHT11(Pin(27))
magnetSensor = Pin(26, mode=Pin.IN)

#adc = machine.ADC(27)
sf = 4095/65535 # Scale factor
volt_per_adc = (3.3 / 4095)




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
        print(magnetSensor)
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
        if value is not 0:
            whitelight.value(1)
        else:
            whitelight.value(0)
        return value
    except Exception as e:
        print("Failed to print the data from magnet sensor")
        return None

# Main function
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
        if magnet_value is not 0:
            publish_data(client, keys.AIO_MAGNET_FEED, magnet_value)

        time.sleep(10)  # Publish data every 10 seconds
        gc.collect()

# Lights for the temperature
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
    

if __name__ == '__main__':
    main()