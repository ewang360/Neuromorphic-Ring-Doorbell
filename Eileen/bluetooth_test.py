import asyncio
from bleak import BleakClient
from PIL import Image
import cv2 as cv

async def send_message(address, message):
    async with BleakClient(address) as client:
        # Connect to the BLE device (your iPhone)
        await client.connect()

        # Encode the message as bytes
        message_bytes = message.encode("utf-8")

        # Write the message to a specific characteristic on the BLE device
        await client.write_gatt_char("0000ffe1-0000-1000-8000-00805f9b34fb", message_bytes)

        # Disconnect from the BLE device
        await client.disconnect()

async def send_image(address, image):
    async with BleakClient(address) as client:
        # Connect to the BLE device (your iPhone)
        await client.connect()

        # Read the image file
        with open(image, "rb") as file:
            image_data = file.read()

        chunk_size = 32  # Adjust the chunk size as needed
        num_chunks = (len(image_data) + chunk_size - 1) // chunk_size

        # Send each chunk of the image data
        for i in range(num_chunks):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, len(image_data))
            chunk = image_data[start:end]
        
            # Write the chunk of image data to the characteristic
            await client.write_gatt_char("0000ffe2-0000-1000-8000-00805f9b34fb", chunk)

            # Introduce a delay if needed
            await asyncio.sleep(0.1)

            break

        # Disconnect from the BLE device
        await client.disconnect()

address = "07F01346-B4E3-CDB7-789F-6F9FBAD10333"
message = "Hello, j!"

# Run the function to send the message
asyncio.run(send_message(address, message))
asyncio.run(send_image(address, "example.jpg"))
