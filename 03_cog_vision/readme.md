# Getting telemetry from a Raspberry Pi to Azure

## Overview

## Prerequisites

1. An active Azure account. If you don't have one, you can sign up for a [free account](https://azure.microsoft.com/free/).
1. [VS Code](https://code.visualstudio.com/Download)
1. Hardware listed below

### Hardware

| Item | Description | Link |
|-|-|-|
| Raspberry Pi 3 or 4 | Single board computer | [Adafruit](https://www.adafruit.com/product/4292) |
| Raspberry Pi Camera V2 | Ribbon camera for the Pi | |
| USB C power supply (Pi 4) | Power cable for Raspberry Pi 4 | [Adafruit](https://www.adafruit.com/product/4298) |
| Micro USB USB power supply (Pi 3) | Power cable for Raspberry Pi 3 | [Adafruit](https://www.adafruit.com/product/1995) |
| SD Card with Raspberry Pi OS | Operating system for the Pi | [Adafruit](https://www.adafruit.com/product/2820) |

## Setup Azure Resources

First you'll provision the Azure resources needed for this sample. You're going to use IoT Hub, Azure Functions, and Table Storage.

| Resource | Description | Link |
|-|-|-|
| Computer Vision | Computer vision API from Azure | [Azure](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/) |

### Preparing your environment

1. If you haven't already, clone this repo to your computer

1. Open command prompt or terminal and navigate to *pi-azure-recipes*

1. In command prompt or terminal type and run ```code 03_cv```. This will open the project folder in VS Code

### Create a computer vision resource

1. Fist you'll need to create [a computer vision resource](https://ms.portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision)

1. Select your subscription 

1. For your resource group select *Create new*, and give your resource group a name

1. Select a Location that is located near you

1. Give your computer vision resource a name

1. Select *Free F0* for the pricing tier
    > Note: You can only have one free tier active per account

1. After your resource is deployed, select *Go to resource*

1. You will need the key and endpoint from this resource to connect your Raspberry Pi to it. Select *Keys and Endpoints* from the left navigation.

1. Make a note of the key and endpoint for your resource, you'll use these later on your Pi.

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

1. Connect your Raspberry Pi to a monitor and keyboard or use the the instructions [here](https://github.com/microsoft/rpi-resources/tree/master/headless-setup) to setup your pi for SSH

1. Set up your Pi camera using [this guide](https://www.raspberrypi.org/documentation/configuration/camera.md)

1. Using a USB drive or an SSH file transfer software copy the *client* folder to the Pi

1. Run the *python_environment_setup.sh* shell script

1. Once the script finishes navigate to the *client* folder press **Ctrl + H* to show hidden files.

1. Open the newly created *.env* file in a text editor and fill in you key and endpoint
    ```
    SUBSCRIPTION_KEY='YOUR-SUBSCRIPTION-KEY'
    ENDPOINT='YOUR-ENDPOINT'
    ```

1. Then type
    ```sh
    python3 cv_pi_client.py
    ```

1. You should see the picture the camera took and what the Computer Vision service was able to identify in it.

## Clean up Resources

If you keep the resources you provisioned you'll continue to incur costs on them. The steps below will walk you through how to clean up your resources.

1. In the Azure portal navigate to the resource group you created earlier

1. In the Resource group page, review the list of included resources, and verify that they are the ones you want to delete

1. Select Delete resource group, and follow the instructions.

Deletion may take a couple of minutes. When it's done, a notification appears for a few seconds. You can also select the bell icon at the top of the page to view the notification.
