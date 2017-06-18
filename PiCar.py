import cv2
import numpy as np
from matplotlib import pyplot as plt
import PiCamera as cam
from time import sleep
import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
from skimage.measure import structural_similarity as ssim

# accesses stored images for cross-checking with the feed
stopS = cv2.imread('/assets/images/stopBW.png', 0)
leftS = cv2.imread('/assets/images/left.jpeg', 0)
rightS = cv2.imread('/assets/images/right.jpeg', 0)

# starts camera and captures image
camera = PiCamera()

camera.start_preview()
camera.capture('capture.png')
cap = cv2.imgread('capture.png', 0)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# defines motors
left = mh.getMotor(1)
right = mh.getMotor(3)

# processes image for cross comparison with capture
# returns black and white image after Gaussian blur
def thresholdImage(img):
    img = cv2.medianBlur(img,5)

    ret,th1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    return img

# returns true if imgA is similar to a certain degree to imgB, i.e. if they are different images of the same sign
# uses the Structural Similarity Index (SSIM) method
# research done here: http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/ 
def isSimilar(imgA, imgB):
    return ssim(imgA, imgB) > 0


# print image img
def plot(img):
    plt.subplot(2, 2, 2)
    plt,imshow(img, 'gray')
    plt.title('processed image')
    plt.xticks([])
    plt.yticks([])
    plt.show
    
# motor functions
def forward():
    left.run(Adafruit_MotorHAT.FORWARD)
    right.run(Adafruit_MotorHAT.FORWARD)
    
    left.setSpeed(100)
    right.setSpeed(100)

def left():
    left.run(Adafruit_MotorHAT.BACKWARD)
    right.run(Adafruit_MotorHAT.FORWARD)

    left.setSpeed(100)
    right.setSpeed(100)
    
def right():
    left.run(Adafruit_MotorHAT.FORWARD)
    right.run(Adafruit_MotorHAT.BACKWARD)

    left.setSpeed(100)
    right.setSpeed(100)

def stop():
    left.setSpeed(0)
    right.setSpeed(0)

    left.run(Adafruit_MotorHAT.RELEASE)
    right.run(Adafruit_MotorHAT.RELEASE)

# recommended for auto-disabling motors on shutdown
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# 'main' functionality, will need to adjust delays during testing
# moves forward by default
# stops on a stop sign, turns left at a left arrow, and turns right at a right arrow
if(isSimilar(cap, stopS)):
    stop()
elif(isSimilar(cap, leftS)):
    left()
    time.sleep(1)
    forward()
elif(isSimilar(cap, rightS)):
    right()
    time.sleep(1)
    forward()
else:
    forward()
    
    

atexit.register(turnOffMotors)
