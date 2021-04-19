# Getting telemetry from a Raspberry Pi to Azure

## Overview

Get started with Azure IoT Hub and Raspberry Pi! This sample projects has everything you need to get data from your Raspberry Pi to Table Storage in Azure. The code here is meant to be a starting point for your project. In this sample we set up 3 Azure resources, an IoT Hub, Functions, and Table Storage. IoT Hub connects internet enabled devices to other Azure services, Functions offers serverless compute which we use to process and save the data, and Table Storage is a no SQL database so we have somewhere to keep the data. The only services in this sample that does not offer a free tier is Table Storage.

## Prerequisites

1. An active Azure account. If you don't have one, you can sign up for a [free account](https://azure.microsoft.com/free/).
1. [VS Code](https://code.visualstudio.com/Download)
1. [Azure IoT Hub](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-toolkit), [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions), and [Azure Storage](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurestorage) extension for VS Code
1. Hardware listed below

### Hardware

| Item | Description | Link |
|-|-|-|
| Raspberry Pi 3 or 4 | Single board computer | [Adafruit](https://www.adafruit.com/product/4292) |
| USB C power supply (Pi 4) | Power cable for Raspberry Pi 4 | [Adafruit](https://www.adafruit.com/product/4298) |
| Micro USB USB power supply (Pi 3) | Power cable for Raspberry Pi 3 | [Adafruit](https://www.adafruit.com/product/1995) |
| SD Card with Raspberry Pi OS | Operating system for the Pi | [Adafruit](https://www.adafruit.com/product/2820) |

## Setup Azure Resources

First you'll provision the Azure resources needed for this sample. You're going to use IoT Hub, Azure Functions, and Table Storage. We'll also setup a budget, so you can get a warning if your services are racking up a big bill.

| Resource | Description | Link |
|-|-|-|
| IoT Hub | Two way IoT communication platform | [Azure](https://azure.microsoft.com/en-us/services/iot-hub/) |
| Azure Functions | Serverless compute platform | [Azure](https://azure.microsoft.com/en-us/services/functions/) |
| Table Storage | No SQL database | [Azure](https://azure.microsoft.com/en-us/services/storage/tables/) |

### Preparing your environment

1. If you haven't already, clone this repo to your computer

1. Open command prompt or terminal and navigate to *pi-azure-recipes*

1. In command prompt or terminal type and run ```code 01_iot```. This will open the project folder in VS Code

1. Press *F1* to open the command palette, search for and select **Azure Functions: Create New Project**

1. Choose *browse*, and select the folder named *data_processing*

1. Select *Python* for programing language and then select the interpreter path
    > *Note: Only python version 3.6, 3.7, and 3.8 are supported*

1. Select *Skip for now* for template

1. Select *No* for all the prompts in the creation process

1. Your function is now initialized in VS Code

### Create IoT Hub

1. Next you'll set up and IoT Hub. This will deploy a resource on Azure

1. Press *F1* to open the command palette, search for and select **Azure IoT Hub: create IoT Hub**

1. Select your subscription, then select *+ Create Resource Group*

1. Give your resource group a name

1. Select a Location that is located near you

1. Select *F1: Free* for the pricing tier
    > Note: You can only have one free tier active per account

1. The IoT Hub should now appear in the *Azure IoT Hub* tab

1. Open the command palette, search for and select **Azure IoT Hub: Copy IoT Hub Connection String**

1. Open the *local.settings.json* file that was created with your function

1. Add the connection string to *Values* with the variables name **"IoTHubConnectionString"**
    ```json
    "IoTHubConnectionString": "YOUR-CONNECTION-STRING"
    ```

### Create storage account

1. Press *F1* to open the command palette, search for and select **Azure Storage: Create Storage Account**

1. Select your subscription

1. Give you storage account a name
    > Note: this name has to be globally unique

1. Open the command palette, search for and select **Azure Storage: Copy Connection String**

1. Open the *local.settings.json* file that was created with your function.

1. Add the connection string to *Values* with the variables name **"AzureWebJobsStorage"**
    ```json
    "AzureWebJobsStorage": "YOUR-CONNECTION-STRING"
    ```

### Setup you Raspberry Pi Device

1. Press *F1* to open the command palette, search for and select **Azure IoT Hub: Create Device**

1. Give the device a name

1. The connection string for the device should print in the Output window, note this connection string, you'll need later on your Raspberry Pi

1. Connect your raspberry Pi to a monitor and keyboard or use the the instructions [here](https://github.com/microsoft/rpi-resources/tree/master/headless-setup) to setup your pi for SSH

1. Using a USB drive or an SSH file transfer software move the files in the *client* folder to the Pi

1. Run the *python_environment_setup.sh* shell script

1. Once the script finishes open the newly created *.env* file

1. Paste the device connection string there
    ```
    CONNECTION_STRING='YOUR-DEVICE-CONNECTION-STRING'
    ```

1. In the client folder on your Pi type
    ```sh
    source ./.venv/Scripts/activate
    ```

1. Then type
    ```sh
    python3 raspberry-pi-client.py
    ```

1. Your device is now sending telemetry to IoT Hub

### Test your function locally

1. In the VS Code on you computer open **__init\__\.py** from  *01_iot\data_processing\telemetry_saver*

1. Press *F5* to begin debugging

1. You should see the telemetry from the Pi in the terminal windows

### Deploying your function

1. Press *F1* to open the command palette, search for and select *Azure Functions: Deploy to function app*

    > Note: this will create a few resources in your azure subscription

1. Give your function app a name

1. Select Python 3.8

1. Select a region near where you are located

1. When the function deployment completes you will be given the option to upload your local settings. Select *Upload settings* to upload your connection string to the App settings in Azure

## Clean up Resources

If you keep the resources you provisioned you'll continue to incur costs on them. The steps below

1. In Visual Studio Code, press *F1* to open the command palette. In the command palette, search for and select *Azure Functions: Open in portal*

1. Choose your function app, and press Enter. The function app page opens in the Azure portal

1. In the Overview tab, select the named link next to *Resource group*

1. Select the resource group to delete from the function app page

1. In the Resource group page, review the list of included resources, and verify that they are the ones you want to delete

1. Select Delete resource group, and follow the instructions.

1. Repeat these steps for the storage account you created, except in step 1 search for and select *Azure Storage: Open in portal*

Deletion may take a couple of minutes. When it's done, a notification appears for a few seconds. You can also select the bell icon at the top of the page to view the notification.
