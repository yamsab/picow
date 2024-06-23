import lib
import lib.wifiConnection
import main

# WiFi Connection
try:
    ip = lib.wifiConnection.connect()
    print(f"Connected to WiFi, IP: {ip}")

    # Start the main script
    main.main()

except KeyboardInterrupt:
    print("Keyboard interrupt")
except Exception as e:
    print(f"Failed to connect to WiFi or run the main script: {e}")
