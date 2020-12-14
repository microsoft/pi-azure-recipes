from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from time import sleep
from dotenv import load_dotenv

from picamera import PiCamera

# Create a camera object
camera = PiCamera()

load_dotenv('.env')

# Add your Computer Vision subscription key and endpoint to your environment
# variables in the .env file.
subscription_key = os.getenv('SUBSCRIPTION_KEY')
endpoint = os.getenv('ENDPOINT')

computervision_client = ComputerVisionClient(
                        endpoint,
                        CognitiveServicesCredentials(subscription_key)
                        )


def take_picture(image_path='./image.jpg'):
    '''Returns path to picture, stores picture in the same directory as code.

    Parameter:
    ---------
    image_path: str
        path to save image to. Default is './image.jpg'

    Returns:
    --------
    image_path: str
        path to image
    '''

    camera.start_preview(alpha=200)
    # Pi Foundation recommends waiting 2s for light adjustment
    sleep(2)
    # Change or comment out as needed
    camera.rotation = 180
    # Input image file path here
    camera.capture(image_path)
    # Stop camera
    camera.stop_preview()

    return(image_path)


def detect_objects(image_path):
    ''' Prints objects detected in an image and returns the ImageDescription
    from computer vision API

    Parameters
    ----------
    image_path: str
        path to the location of the image file to use in object detection

    Returns
    -------
    detected_objects: ImageDescription
        ImageDescription class created by the computer vision api

    '''

    # Open image from path
    local_image = open(image_path, "rb")
    # Call API with URL
    detected_objects = computervision_client.detect_objects_in_stream(
                       local_image
                       )

    # Print detected objects results with bounding boxes
    print("Detecting objects in image:")
    if len(detected_objects.objects) == 0:
        print("No objects detected.")
    for object in detected_objects.objects:
        print(object.object_property)

    return(detected_objects)


def frame_objects(detected_objects, image_path):

    '''Creates frames around the object detected in an image and plots the
    frame over that image.

    Parameters
    ----------
    detected_objects : ImageDescription
        ImageDescription that was returned from the computer vision api

    image_path: str
        path to the location of the image file that was used in object
        detection
    '''

    # Create figure and plot
    fig, ax = plt.subplots(1)

    if len(detected_objects.objects) == 0:
        print("No objects detected.")
    else:
        for object in detected_objects.objects:
            rect = patches.Rectangle(
                (object.rectangle.x, object.rectangle.y),
                object.rectangle.w, object.rectangle.h,
                linewidth=1,
                edgecolor='r',
                facecolor='none'
                )
            plt.text(
                object.rectangle.x,
                object.rectangle.y,
                object.object_property,
                color='w'
                )
            ax.add_patch(rect)

    local_image = open(image_path, "rb")
    image = Image.open(local_image)
    ax.imshow(image)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    try:
        path_to_image = take_picture()
        detected_objects = detect_objects(path_to_image)
        frame_objects(detected_objects, path_to_image)
    except KeyboardInterrupt:
        print('Script Stopped')
