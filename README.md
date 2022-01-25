# Raspberry Pi Recipes for Azure

## Overview

Raspberry Pi recipes for Azure is a collection of samples that use use a Raspberry Pi and one or more Azure services. All the recipes included here represent end to end scenarios rather than just documenting how to interface with a single service. These are all written to get you up and running fast. Most take between 5 and 30 minutes to complete and require the least amount of hardware. All is code is designed to be adapted into other project, and many of these recipes can be combined.

If there is something you'd like to know how to do using Azure and a Raspberry Pi and you don't see it here open an issue and let us know. If you know how to do something cool with Azure and a Raspberry Pi open a PR and show us what you got!

> Note: We do our best to minimize the cost of services, but some of these samples will incur a small charge on your Azure account.

## Prerequisites

1. Free Azure Account
1. Basic understanding on Python
1. Raspberry Pi 3 or 4
1. Monitor/keyboard/mouse or ability to SSH into the Pi

## Contents

| Recipe | Description | Time | Prerequisites |
|--------|-------------|------|---------------|
| [01 IoT Hub d2c](./01_iot) | Send telemetry to Azure table storage using IoT Hub and Azure functions. | 25 Mins | None |
| [02 IoT Hub c2d](./02_c2d_messages) | Trigger events on your Raspberry Pi using Azure functions and IoT Hub | 15 mins | None |
| [03 Computer Vision](./03_cv) | Use the computer vision cognitive service to detect objects in an image | 20 Mins | None |
| [04 IoT Central](./04_iot_central) | Connect and control a Raspberry Pi with IoT Central | 30 Mins | None |

## Resources

[Raspberry Pi Resources Repo](https://github.com/microsoft/rpi-resources)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

If you know how to do something cool with a Raspberry Pi and Azure we'd love to see it! To contribute open a PR with your additions and someone from the team will review it.

### Guidelines

- Keep all of the file for each example in it own directory. Using this format: ```01_example_name```
- Include a readme with instructions on how to setup the example
- If you would like to use images in your readme they should referenced not uploaded to this repo
- Include an estimated cost for the Azure resources
- When possible and practical use one programing language for the whole example
- Use flake8 to lint Python code
- Examples should be secure by default, meaning connection strings and api key can't be checked in by accident. To do this we wrote a shell script that generate .env files that the user populates with their keys.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
