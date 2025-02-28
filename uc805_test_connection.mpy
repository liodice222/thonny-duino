from machine import Pin, I2C

# Initialize I2C with correct GPIOs for ESP8266
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)  # 400 kHz speed

# Scan for connected devices
devices = i2c.scan()

if devices:
    print("I2C devices found:", [hex(device) for device in devices])
else:
    print("No I2C devices found, check wiring!")
