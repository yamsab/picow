import time
from machine import ADC, unique_id
import ubinascii
from lib.umqtt_simple import MQTTClient
import lib.keys as keys

# Initialize ADC
adc = ADC(27)
sf = 4095 / 65535  # Scale factor
volt_per_adc = (3.3 / 4095)

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

# Calculate temperature from the sensor
def read_temperature():
    millivolts = adc.read_u16()
    adc_12b = millivolts * sf
    volt = adc_12b * volt_per_adc
    shift = volt - 0.5
    temp = shift / (50 / 0.5)
    return temp

# Main function
def main():
    client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)
    
    while True:
        temp = read_temperature()
        print('Temperature:', temp)
        publish_data(client, keys.AIO_TEMP_FEED, temp)
        time.sleep(10)  # Publish data every 10 seconds
        time.sleep(2)
        millivolts = adc.read_u16()

        adc_12b = millivolts * sf

        volt = adc_12b * volt_per_adc

        """# MCP9700 characteristics
        dx = abs(50 - 0)
        dy = abs(0 - 0.5)

        shift = volt - 0.5

        temp = shift / (dy / dx)
        print(temp)
        time.sleep(1)
"""
if __name__ == '__main__':
    main()