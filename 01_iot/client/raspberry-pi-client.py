# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from azure.iot.device import IoTHubDeviceClient, Message
import os
import json
import random
from dotenv import load_dotenv
from time import sleep

load_dotenv('./.env')

device_id = 'Raspberry Pi'

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

if __name__ == '__main__':

    try:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        while True:
            # Generate a random value to send.
            value = random.randrange(0, 100)

            # Build a json string
            data_to_send = json.dumps({'id': device_id, 'value': value})

            message = Message(data_to_send)
            client.send_message(message)
            print('message sent')

            # Wait 30 seconds between data points
            sleep(30)

    except KeyboardInterrupt:
        print("Sample Stopped")
