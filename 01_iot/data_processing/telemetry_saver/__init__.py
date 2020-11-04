# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import List
import logging
import uuid
import json

import azure.functions as func


def main(events: List[func.EventHubEvent], telemetry: func.Out[str]):
    for event in events:
        logging.info('Python EventHub trigger processed an event: %s',
                     event.get_body().decode('utf-8'))

        message = json.loads(event.get_body().decode('utf-8'))
        rowKey = str(uuid.uuid4())

        data = {
            "Name": message['id'],
            "Value": message['value'],
            "PartitionKey": message['id'],
            "RowKey": rowKey
        }

        telemetry.set(json.dumps(data))
