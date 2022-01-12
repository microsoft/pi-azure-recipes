# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import os
import azure.functions as func

from azure.iot.hub import IoTHubRegistryManager

CONNECTION_STRING = os.getenv("IoTHubConnectionString")
DEVICE_ID = os.getenv("DeviceId")


def send_message(data):
    registry_manager = IoTHubRegistryManager.from_connection_string(CONNECTION_STRING)
    props = {}
    props.update(contentType="application/json")
    registry_manager.send_c2d_message(DEVICE_ID, data, properties=props)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    status = req.params.get('status')
    if not status:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            status = req_body.get('status')

    if status == "on":
        data = ('on')
        send_message(data)
        return func.HttpResponse("Device turned on", status_code=200)
    elif status == "off":
        data = ('off')
        send_message(data)
        return func.HttpResponse("Device turned off", status_code=200)
    else:
        return func.HttpResponse(
            "Send status on or off to change device status",
            status_code=200
            )
