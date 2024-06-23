import lib
import lib.wifiConnection
import main

# WiFi Connection
try:
    ip = lib.wifiConnection.connect()
    #main.main

except KeyboardInterrupt:
    print("Keyboard interrupt")


# WiFi Disconnect
# wifiConnection.disconnect().