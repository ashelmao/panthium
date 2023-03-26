import numpy as np
import cv2
from mss import mss
from PIL import Image
import ctypes
import pyautogui
import time
import keyboard
import numpy
import cv2 as cv
import win32api
import threading
import os
import signal
import multiprocessing
import sys
import random
import win32con
from win32con import MOUSEEVENTF_WHEEL
import asyncio
R, G, B = (250, 100, 250)

view = 300

#view = int(view2)/2
half_view = view / 2

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

screensize_x = screensize[0]
screensize_y = screensize[1]

middle_x = screensize_x / 2
middle_y = screensize_y / 2

top_left_x = middle_x - half_view
top_left_y = middle_y - half_view

bounding_box = {'top': int(top_left_y), 'left': int(top_left_x), 'width': view, 'height': view}

sct = mss()

while True:
    sct_img = sct.grab(bounding_box)

    img = np.array(sct_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)


    lower_pink = np.array([139, 95, 154])
    upper_pink = np.array([153, 255, 255])
    mask = cv2.inRange(img, lower_pink, upper_pink)


    #replace all the pink pixels with black pixels
    img[mask != 0] = (0, 0, 0)

    #replace all non pink pixels with white pixels
    img[mask == 0] = (255, 255, 255)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold grayscale image to isolate black pixels
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    # Apply morphological opening to remove small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Calculate pixel concentration around black pixels
    heatmap = cv2.distanceTransform(opening, cv2.DIST_L1, 3)
    heatmap = cv2.normalize(heatmap, None, 0, 1, cv2.NORM_MINMAX)
    gamma = 0.2
    heatmap = np.power(heatmap, gamma)

    


    #draw a rectangle around the concentration of black pixels
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(heatmap, (x, y), (x + w, y + h), (0, 255, 0), 2)





    # Display images
    cv2.imshow('Original Image', img)
    cv2.imshow('Heatmap', heatmap)

    # Check for user input
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break