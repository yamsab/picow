
import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

# Wireless network
WIFI_SSID =  "Kabul_2G_Guest"
WIFI_PASS = "Sabit786" # No this is not our regular password. :)

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "yamsab"
AIO_KEY = "aio_UpHG73p68JmtGIoP4GY9OuKvZ6Wl"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_LIGHTS_FEED = "yamsab/feeds/picow-lights"
AIO_RANDOMS_FEED = "yamsab/feeds/picow-randoms"
AIO_TEMP_FEED = "yamsab/feeds/picow"
