import time
from machine import ADC, unique_id, Pin
import ubinascii
from lib.umqtt_simple import MQTTClient
import lib.keys as keys

# Initialize Pins
redLight = Pin(2, Pin.OUT)
yellowLight = Pin(3, Pin.OUT)


# Initialize ADC
adc = ADC(27)

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
    # ADC to Voltage conversion
    adc_value = adc.read_u16()
    voltage = adc_value * (3.3 / 65535)  # 16-bit ADC value
    print(f"ADC Reading: {adc_value}, Voltage: {voltage:.5f}")

    # Temperature calculation
    reference_voltage = 0.5  # Voltage at 0°C (500mV)
    temperature_per_volt = 100  # 100°C per Volt (10mV/°C)
    temp = (voltage - reference_voltage) * temperature_per_volt
    return temp


# Main function
def main():
    client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)
    
    while True:
        temp = read_temperature()
        print('Temperature:', temp)
        lightstemp(temp)
        publish_data(client, keys.AIO_TEMP_FEED, temp)
        time.sleep(10)  # Publish data every 10 seconds
        
        time.sleep(2)
        millivolts = adc.read_u16()

        adc_12b = millivolts * sf

        volt = adc_12b * volt_per_adc

        # MCP9700 characteristics
        dx = abs(50 - 0)
        dy = abs(0 - 0.5)

        shift = volt - 0.5

        temp = shift / (dy / dx)
        print(temp)
        time.sleep(1)

# Lights for the temperature
def lightstemp(temp):

    if temp < 0:
        redLight.value(1)
        yellowLight.value(0)
    elif temp > 0:
        yellowLight.value(1)
        redLight.value(0)
    elif temp == 0:
        redLight.value(1)
        yellowLight.value(1)
    else:
        redLight.value(0)
        yellowLight.value(0)
    

if __name__ == '__main__':
    main()