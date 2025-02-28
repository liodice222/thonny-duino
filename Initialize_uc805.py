from machine import Pin, I2C
import time

# Initialize I2C
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)  # ESP8266 I2C at 400 kHz

# UC-805 I2C address (from our scan result)
UC805_ADDR = 0x24  

# Function to write data to the camera
def write_register(register, value):
    i2c.writeto(UC805_ADDR, bytes([register, value]))

# Function to read data from the camera
def read_register(register, num_bytes=1):
    i2c.writeto(UC805_ADDR, bytes([register]))  # Tell the camera which register to read
    return i2c.readfrom(UC805_ADDR, num_bytes)  # Read the requested number of bytes

# Step 1: Reset the camera
write_register(0x01, 0x01)  # Sending reset command
time.sleep(0.1)  # Wait for camera to reset

# Step 2: Check if the camera is ready
status = read_register(0x00, 1)  # Read status register
print("Camera Status:", status)

# Step 3: Set resolution (example: 160x120)
write_register(0x02, 0x10)  # Set resolution (you may need to adjust this)

# Step 4: Start an image capture
write_register(0x03, 0x01)  # Capture command
time.sleep(1)  # Wait for image capture

# Step 5: Read image size
image_size = read_register(0x04, 2)  # Read 2 bytes of image size
image_size = int.from_bytes(image_size, 'big')  # Convert bytes to integer
print("Image Size:", image_size, "bytes")

# Step 6: Read the image data
if image_size > 0:
    image_data = []
    for i in range(0, image_size, 32):  # Read in chunks of 32 bytes
        chunk = read_register(0x05, 32)
        image_data.extend(chunk)
        print(f"Read {len(chunk)} bytes...")

    print("Image Capture Complete!")
else:
    print("Error: No image data received.")
