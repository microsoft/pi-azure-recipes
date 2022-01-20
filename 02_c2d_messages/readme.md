# Getting message from Azure to Raspberry Pi

## Overview

Getting messages from Azure to your Raspberry Pi is a useful tool for many IoT scenarios. You can turn on a fan in a greenhouse, start a machine in a production line, or change the type of telemetry being captured at a remote location. In this tutorial we'll show you how to setup an IoT Hub and us an Azure Function to send a simple message to your Raspberry Pi. We then parse the message on the Pi and print out the message. You can use this project as a starting point for you next IoT project!

## Prerequisites

1. An active Azure account. If you don't have one, you can sign up for a [free account](https://azure.microsoft.com/free/).
1. [VS Code](https://code.visualstudio.com/Download)
2. [Azure IoT Tools](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-tools) and [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) extensions for VS Code
3. [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
4. [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools)
5. [Python 3](https://www.python.org/downloads/)
6. Hardware listed below


### Hardware

| Item                              | Description                    | Link                                              |
| --------------------------------- | ------------------------------ | ------------------------------------------------- |
| Raspberry Pi 3 or 4               | Single board computer          | [Adafruit](https://www.adafruit.com/product/4292) |
| USB C power supply (Pi 4)         | Power cable for Raspberry Pi 4 | [Adafruit](https://www.adafruit.com/product/4298) |
| Micro USB USB power supply (Pi 3) | Power cable for Raspberry Pi 3 | [Adafruit](https://www.adafruit.com/product/1995) |
| SD Card with Raspberry Pi OS      | Operating system for the Pi    | [Adafruit](https://www.adafruit.com/product/2820) |

## Setup Azure Resources

First we'll provision the Azure resources we need for this sample. We're going to use IoT Hub, Azure Functions, and Table Storage. We'll also setup a budget, so you can get a warning if your services are racking up a big bill. We provide two ways to provision the resources, you can walk through the step by step instructions or deploy all the resources at once using an Azure Resource Manager template.

| Resource        | Description                        | Link                                                                |
| --------------- | ---------------------------------- | ------------------------------------------------------------------- |
| IoT Hub         | Two way IoT communication platform | [Azure](https://azure.microsoft.com/en-us/services/iot-hub/)        |
| Azure Functions | Serverless compute platform        | [Azure](https://azure.microsoft.com/en-us/services/storage/tables/) |

### Preparing your environment

1. If you haven't already, clone this repo to your computer

1. Open command prompt or terminal and navigate to *pi-azure-recipes*

1. Add the IoT devices capability to your subscription. In your terminal execute each of the following commands, replacing `<VARIABLE>` as needed:
   ```bash
   az login
   az account set -s '<YOUR SUBCRIPTION NAME>'
   az provider register --namespace Microsoft.Devices
   ```
1. In command prompt or terminal type and run ```code 02_c2d```. This will open the project folder in VS Code.

1. Navigate to the Azure Extension by typing **CTRL + SHIFT + A** or by selecting the Azure logo in the left navigation

1. In the Functions Tab select *create new project*

1. Choose browse, and select the folder named *messenger*

1. Select *Python* for programing language and then select the interpreter path
    > *Note: Only python version 3.6, 3.7, and 3.8 are supported*

1. Select *Skip for now* for template

1. Select *No* for all the prompts in the creation process

1. Your function is now initialized in VS Code

### Setup IoT Hub

1. Next you'll set up and IoT Hub. This will deploy a resource on Azure.

1. Navigate back the explorer by typing **Ctrl + Shift + E** or selecting the pages icon from the left navigation

1. In the *Azure Iot Hub* tab select the options menu in the top right

1. Select *Create new IoT Hub*

1. From the drop menu select your subscription the select *+ Create Resource Group*

1. The IoT Hub should now appear in the *Azure IoT Hub* tab

1. From the options menu select *Copy IoT Hub Connection String*

1. Open the *local.settings.json* file that was created with your function.

1. Add the connection string to *Values* with the variable **"IoTHubConnectionString"**
    ```json
    "IoTHubConnectionString": "<YOUR-CONNECTION-STRING>"
    ```
1. We also need to add your **device ID** to the *local.settings.json* file. This is the name you gave your device upon creation. If you don't remember it, it should be listed in the side bar in the *Azure IoT Hub* pane.
   ```json
   "DeviceId": "<DEVICE_ID>"
   ```
1. Once you're finished your *local.settings.json* should look like this:
    ```json
    {
        "IsEncrypted": false,
        "Values": {
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "FUNCTIONS_EXTENSION_VERSION": "~3",
            "IoTHubConnectionString": "HostName=<IOT_HUB_NAME>.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=<IOTHUB_ACCESSKEY>",
            "DeviceId": "<IOT_DEVICE_ID>"
        }
    }
    ```

#### Setup you Raspberry Pi Device

1. From the IoT Hub options menu select *Create Device*

1. Give the device a name

1. The connection string for the device should print in the Output window, note this connection string, you'll need later on your Raspberry Pi

1. Connect your raspberry Pi to a monitor and keyboard or use the the instructions [here](https://github.com/microsoft/rpi-resources/tree/master/headless-setup) to setup your pi for SSH

1. Using a USB drive or an SSH file transfer software move the files in the *client* folder to the Pi

1. Run the *python_environment_setup.sh* shell script

1. Once the script finishes open the sample *.env* file

1. Paste the device connection string there
    ```
    CONNECTION_STRING='<YOUR-DEVICE-CONNECTION-STRING>'
    ```

1. In the client folder on your Pi type
    ```sh
    source ./.venv/bin/activate
    ```

1. Then type to start your client
    ```sh
    python raspberry_pi_client.py
    ```

1. Your device is now ready to receive telemetry from IoT Hub

### Test your function locally

1. On your computer with vs code open to the 02_c2d_messages workspace open the file named *__init\__\.py* in *messenger/message_trigger*

1. Press *F5* to start debugging your azure function locally

1. Once your function has started you'll see a url that look like
    ```sh
    Functions:

        message_trigger: [GET,POST] http://localhost:7071/api/message_trigger
    ```

1. Copy the url and add **?status=on** to the end of it so it reads
    ```
    http://localhost:7071/api/message_trigger?status=on
    ```

1. This is your trigger to activate an action on your Raspberry Pi

    > Make sure that *raspberry_pi_client.py* is still running on your Pi

1. Open a web browser and past the url from the previous step

1. Your Pi should print out ```Device is on```

### Deploy your function to Azure

1. Press *F1* to open the command palette, search for and select *Azure Functions: Deploy to function app*

    > Note: this will create a few resources in your azure subscription

1. Give your function app a name

1. Select Python 3.8

1. Select a region near where you are located

1. When the function deployment completes you will be given the option to upload your local settings. Select *Upload settings* to upload your connection string to the App settings in Azure

## Clean up Resources

If you keep the resources you provisioned you'll continue to incur costs on them. The steps below will

1. In Visual Studio Code, press *F1* to open the command palette. In the command palette, search for and select *Azure Functions: Open in portal*

1. Choose your function app, and press Enter. The function app page opens in the Azure portal

1. In the Overview tab, select the named link next to *Resource group*

1. Select the resource group to delete from the function app page

1. In the Resource group page, review the list of included resources, and verify that they are the ones you want to delete

1. Select Delete resource group, and follow the instructions.

Deletion may take a couple of minutes. When it's done, a notification appears for a few seconds. You can also select the bell icon at the top of the page to view the notification.
