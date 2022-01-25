# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import asyncio
import os
import base64
import hmac
import hashlib
import dotenv
import time
import socket
import math

# Azure IoT Device SDK imports
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import exceptions
from azure.iot.device import Message
from azure.iot.device import MethodResponse

dotenv.load_dotenv('./.env')

device_id = 'Raspberry_Pi'
model_id = 'dtmi:RaspberryPi;1'

SCOPE_ID = os.getenv("SCOPE_ID")
GROUP_SYMMETRIC_KEY = os.getenv("GROUP_SYMMETRIC_KEY")

provisioning_host = 'global.azure-devices-provisioning.net'
use_websockets = True
terminate = False
client = None


##
# Utility functions for getting information about the Raspberry Pi device
##

# get the Raspberry Pi hardware model information
def get_pi_model_info():
    f = open('/proc/cpuinfo')
    pi_info_raw = f.read()
    f.close()
    pi_info_lines = pi_info_raw.splitlines()
    pi_info = {}
    pi_info['model'] = [i for i in pi_info_lines if i.startswith('Model')][0].split(':')[1].strip()
    pi_info['cpu_architecture'] = [i for i in pi_info_lines if i.startswith('CPU architecture')][0].split(':')[1].strip()
    pi_info['cpu_model'] = [i for i in pi_info_lines if i.startswith('model name')][0].split(':')[1].strip()
    pi_info['cpu_revision'] = [i for i in pi_info_lines if i.startswith('CPU revision')][0].split(':')[1].strip()
    pi_info['estimated_mips'] = float([i for i in pi_info_lines if i.startswith('BogoMIPS')][0].split(':')[1].strip())
    pi_info['hardware'] = [i for i in pi_info_lines if i.startswith('Hardware')][0].split(':')[1].strip()
    pi_info['hardware_revision'] = [i for i in pi_info_lines if i.startswith('Revision')][0].split(':')[1].strip()
    pi_info['serial_number'] = [i for i in pi_info_lines if i.startswith('Serial')][0].split(':')[1].strip()
    return pi_info


# get the current, min, and max CPU frequency information
def get_cpu_frequency_statistics():
    f = open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq')
    current_cpu_frequency = f.readline()
    f.close()
    f = open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq')
    min_cpu_frequency = f.readline()
    f.close()
    f = open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq')
    max_cpu_frequency = f.readline()
    f.close()
    return {"current": float(current_cpu_frequency) / 1000, "min": float(min_cpu_frequency) / 1000, "max": float(max_cpu_frequency) / 1000}


# get current CPU temperature
def get_current_cpu_temp():
    f = open('/sys/class/thermal/thermal_zone0/temp')
    current_cpu_temp = f.readline()
    f.close()
    return float(current_cpu_temp) / 1000


# get memory information in KB
def get_memory_statistics():
    p = os.popen('free')
    line = p.readline()  # we throw away the header information
    line = p.readline()
    memory_info = line.split()
    return {"total": int(memory_info[1]), "used": int(memory_info[2]), "free": int(memory_info[3])}


# get CPU usage
def get_cpu_usage():
    cpu_usage = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())
    return float(cpu_usage)


# get disk space information - includes unit
def get_disk_statistics():
    p = os.popen('df -h /')
    line = p.readline()  # we throw away the header information
    line = p.readline()
    disk_info = line.split()
    return {"total": disk_info[1], "used": disk_info[2], "remaining": disk_info[3], "percentage_used": disk_info[4]}


# get the current IP address
def get_ip_address():
    testIP = '8.8.8.8'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((testIP, 0))
    return s.getsockname()[0]


# handler for the cloud to device messages
def c2d_message_handler(message):
    if message.custom_properties['method-name'] == 'apply_cpu_load':
        t_end = time.time() + int(message.data.decode())
        while time.time() < t_end:
            # this will use 100% of a single core so the CPU usage will
            # increase by ~25% over the norm
            math.factorial(100)
    else:
        print('Error: Unknown C2D command')


# handler for direct method messages
async def direct_method_handler(method_request):
    print(f'executing direct method: {method_request.name}({method_request.payload})')

    if method_request.name == 'speak_to_me':
        # speaks the message via the Raspberry Pi onboard sound
        # plug in a pair of headphones to the 3.5mm jack to hear
        # uses espeak, install on the Pi with 'sudo apt install espeak'
        os.system(f'espeak "{method_request.payload}"')
        # send response - echo back the sent text message
        method_response = MethodResponse.create_from_method_request(method_request, 200, method_request.payload)
    else:
        # send bad request status code
        method_response = MethodResponse.create_from_method_request(method_request, 400, 'unknown command')

    await client.send_method_response(method_response)


# handler for desired property patches
async def desired_property_handler(patch):
    if 'red_led_control' in patch.keys():
        # toggle the red power LED of the Raspberry Pi on or off
        os.system('echo gpio | sudo tee /sys/class/leds/led1/trigger > /dev/null 2>&1')
        if patch['red_led_control'] == 'on':
            os.system('echo 1 | sudo tee /sys/class/leds/led1/brightness > /dev/null 2>&1')  # led on
        elif patch['red_led_control'] == 'off':
            os.system('echo 0 | sudo tee /sys/class/leds/led1/brightness > /dev/null 2>&1')  # led off

        # acknowledge the desired property back to IoT Central
        reported_payload = {"red_led_control": {"value": patch['red_led_control'], "ac": 200, "ad": "completed", "av": patch['$version']}}
        await client.patch_twin_reported_properties(reported_payload)
    else:
        print('Error: Unknown desired porprty patch')


# coroutine that sends telemetry on a set frequency until terminated
async def send_telemetry(send_frequency):
    while not terminate:
        payload = f'{{"cpu_temp": {get_current_cpu_temp()}, "cpu_freq": {get_cpu_frequency_statistics()["current"]}, "cpu_usage": {get_cpu_usage()}, "ram_usage": {get_memory_statistics()["used"]}}}'
        print(f'sending message:{payload}')
        msg = Message(payload)
        # these message properties are important if you intend to export data from IoT Central
        msg.content_type = 'application/json'
        msg.content_encoding = 'utf-8'
        await client.send_message(msg)
        print('completed sending telemetry message')
        await asyncio.sleep(send_frequency)


# coroutine that sends reported properties on a set frequency until terminated
async def send_reportedProperty(send_frequency):
    while not terminate:
        reported_payload = {"remaining_disk_space": get_disk_statistics()['remaining']}
        print(f'Sending reported property: {reported_payload}')
        try:
            await client.patch_twin_reported_properties(reported_payload)
        except Exception:
            print('Error: Unable to send the reported property value')
        await asyncio.sleep(send_frequency)


# define behavior for halting the application
def stdin_listener():
    global terminate
    while True:
        selection = input('Press Q to quit\n')
        if selection == 'Q' or selection == 'q':
            terminate = True
            print('Quitting...')
            break


# derives a symmetric device key for a device id using the group symmetric key
def derive_device_key(device_id, group_symmetric_key):
    message = device_id.encode("utf-8")
    signing_key = base64.b64decode(group_symmetric_key.encode("utf-8"))
    signed_hmac = hmac.HMAC(signing_key, message, hashlib.sha256)
    device_key_encoded = base64.b64encode(signed_hmac.digest())
    return device_key_encoded.decode("utf-8")


# main routine for connecting to IoT Central via Device Provisioning Service (DPS)
# then sends telemetry and reported properties whilst monitoring incoming messages
async def main():
    global client

    # calculate the device
    device_symmetric_key = derive_device_key(device_id, GROUP_SYMMETRIC_KEY)

    # create a provisioning client that uses a symmetric device key
    provisioning_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=device_id,
        id_scope=SCOPE_ID,
        symmetric_key=device_symmetric_key,
        websockets=use_websockets
    )

    # register the device via DPS (with a specific device model) 
    # and obtain the hostname of the Azure IoT hub to connect to
    provisioning_client.provisioning_payload = f'{{"iotcModelId":"{model_id}"}}'
    registration_result = None
    try:
        registration_result = await provisioning_client.register()
    except exceptions.CredentialError:
        print('Credential Error')
    except exceptions.ConnectionFailedError:
        print('Connection Failed Error')
    except exceptions.ConnectionDroppedError:  # error if the key is wrong
        print('Connection Dropped Error')
    except exceptions.ClientError:  # error if the device is blocked
        print('Client Error')
    except Exception:
        print('Unknown Exception')

    # create the IoT hub device client and connect
    client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=device_symmetric_key,
        hostname=registration_result.registration_state.assigned_hub,
        device_id=device_id,
        websockets=use_websockets
    )

    await client.connect()

    # send the Raspberry Pi device information as a reported property
    pi_info = get_pi_model_info()
    reported_payload = {"pi_info": {
                            "cpu_architecture": pi_info['cpu_architecture'],
                            "cpu_model": pi_info['cpu_model'],
                            "cpu_revision": pi_info['cpu_revision'],
                            "estimated_mips": pi_info['estimated_mips'],
                            "hardware": pi_info['hardware'],
                            "hardware_revision": pi_info['hardware_revision'],
                            "ip_address": get_ip_address(),
                            "min_cpu_frequency": get_cpu_frequency_statistics()["min"],
                            "max_cpu_frequency": get_cpu_frequency_statistics()["max"],
                            "model": pi_info['model'],
                            "serial_number": pi_info['serial_number'],
                       }}
    try:
        await client.patch_twin_reported_properties(reported_payload)
    except Exception:
        print('Error: Unable to send the Raspberry Pi model information')

    # set up the cloud to device message listener
    client.on_message_received = c2d_message_handler

    # set up the direct method message listener
    client.on_method_request_received = direct_method_handler
    
    # set up the twin desired property patch message listener
    client.on_twin_desired_properties_patch_received = desired_property_handler

    # start the telemetry loop with a send frequency of 5 seconds
    telemetry_loop = asyncio.create_task(send_telemetry(5))

    # start the reported property loop with a send frequency of 20 seconds
    reported_loop = asyncio.create_task(send_reportedProperty(20))

    # start the keyboard monitor looking for Q to be pressed to clean exit
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, stdin_listener)

    # do not exit until the telemetry and reported property loops exit
    await asyncio.gather(telemetry_loop, reported_loop)

    # disconnect cleanly from the IoT hub
    await client.disconnect()

# lets start the party!!
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Leaving so soon :-(')
