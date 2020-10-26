# https://github.com/Azure/azure-iot-sdk-python/blob/master/azure-iot-device/samples/async-hub-scenarios/receive_message.py

import threading
import asyncio
import time
import os
import json
from six.moves import input
import dotenv
from azure.iot.device.aio import IoTHubDeviceClient

dotenv.load_dotenv('./.env')

device_id = 'Raspberry Pi'

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

def message_receiver(message):
    print(message.data.decode())
    data = message.data.decode()
    if data == "on":
        print("is on")

# define behavior for halting the application
def stdin_listener():
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break

async def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        
    await client.connect()

    client.on_message_received = message_receiver

    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    await user_finished

    await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print ("Client Stopped")