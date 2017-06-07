import cv2
import numpy as np
from matplotlib import pyplot as plt
import PiCamera as cam
from time import sleep
import RPi.GPIO as GPIO

# accesses stored images for cross-checking with the feed
# TODO: store processed versions of these images
stop = cv2.imread('/assets/images/stop.png', 0)
left = cv2.imread('/assets/images/left.jpeg', 0)
right = cv2.imread('/assets/images/right.jpeg', 0)

camera = PiCamera()

# starts camera and captures image
camera.start_preview()
camera.capture('capture.png')
cap = cv2.imgread('capture.png', 0)

# processes image for cross comparison with capture
# returns black and white image after Gaussian blur
def process(img):
    img = cv2.medianBlur(img,5)
    

def forward():


def left():


def right():
