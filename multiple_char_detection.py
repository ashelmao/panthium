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
import asyncio


exit_event = threading.Event()

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

def is_mouse_down():
    lmb_state = win32api.GetKeyState(0x06)
    return lmb_state < 0


def terminate_program():
    if win32api.GetKeyState(0x05):
        sys.exit()
        



def m_thread():
    while True:

        terminate_program()

        if is_mouse_down():

            terminate_program()

            while is_mouse_down(): #tabbed out of the game, the program will run until the key is pressed again

                terminate_program()




                sct_img = sct.grab(bounding_box)

                #return true if there is a pixel with the value "250, 100, 250" in the image using cv2
                def check_pink():
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
                
                    #add a white triangle in the bottom right corner of the screen
                    cv2.line(img, (600, 600), (300, 300), (255, 255, 255), thickness=200)


                    #------------------------------------------------------------stop the aiming when all corners are black------------------------------------------------------------
                    
                    middle = np.array([half_view, half_view])

                    
                    #get the color of a 1x1 pixel in (int(middle[0]) - 20, int(middle[1]) - 20), (int(middle[0]) + 20, int(middle[1]) + 20)
                    top_left2 = img[int(middle[0]) - 20, int(middle[1]) - 20]
                    top_right2 = img[int(middle[0]) + 20, int(middle[1]) - 20]
                    bottom_left2 = img[int(middle[0]) - 20, int(middle[1]) + 20]
                    bottom_right2 = img[int(middle[0]) + 20, int(middle[1]) + 20]



        
        


                    #print(top_left2, top_right2, bottom_left2, bottom_right2)

                    #if all corners are black print "all corners are black"
                    if (top_left2[0] == 0 and top_right2[0] == 0) and (bottom_left2[0] == 0 and bottom_right2[0] == 0) or (top_left2[0] == 0 and top_right2[0] == 0) or (bottom_left2[0] == 0 and bottom_right2[0] == 0):
                        al_corners_black = True
                        
                        cv2.line(img, (int(middle[0]) - 5, int(middle[1]) - 5), (int(middle[0]) - 80, int(middle[1]) - 80), (255, 255, 255), 15)
                        cv2.line(img, (int(middle[0]) + 5, int(middle[1]) - 5), (int(middle[0]) + 80, int(middle[1]) - 80), (255, 255, 255), 15)
                        cv2.line(img, (int(middle[0]) - 5, int(middle[1]) + 5), (int(middle[0]) - 80, int(middle[1]) + 80), (255, 255, 255), 15)
                        cv2.line(img, (int(middle[0]) + 5, int(middle[1]) + 5), (int(middle[0]) + 80, int(middle[1]) + 80), (255, 255, 255), 15)
                    else:
                        al_corners_black = False


                    #-----------------------------------------------------------------back to normal------------------------------------------------------------------------

    
                    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    ret, thresh = cv2.threshold(imgray, 127, 255, 0, cv2.THRESH_BINARY)
                    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    # create an empty mask
                    mask = np.zeros(img.shape[:2], dtype=np.uint8)

                    # loop through the contours
                    for i, cnt in enumerate(contours):
                        # if the contour has no other contours inside of it
                        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) # Use cv2.CCOMP for two level hierarchy
                        if hierarchy[0][i][3] != -1: # basically look for holes
                            # if the size of the contour is less than a threshold (noise)
                            if cv2.contourArea(cnt) < 30:
                                # Fill the holes in the original image with white
                                cv2.drawContours(mask, [cnt], 0, 255, -1)
                                cv2.drawContours(img, [cnt], 0, (255, 255, 255), -1)

                    #get the coordinates of all the black pixels
                    black_pixels = np.argwhere(img == [0, 0, 0])
                    #if there are no black pixels, return None
                    if len(black_pixels) == 0:
                        return None
                    #get the coordinates of the middle of the image
                    middle = np.array([half_view, half_view])

                    #get the coordinates of the closest black pixel
                    closest_black_pixel = black_pixels[np.argmin(np.linalg.norm(black_pixels, axis=1))]

                    #get the x value of closest_black_pixel
                    closest_black_pixel_x = closest_black_pixel[1]

                    #get the y value of closest_black_pixel
                    closest_black_pixel_y = closest_black_pixel[0]

                    #get the coordiantes of the cursor on the screen
                    c_cursor = pyautogui.position()

                    #print(f"cursor: {c_cursor}")

                    c_to_bp_x = closest_black_pixel_x - c_cursor[0]

                    c_to_bp_y = closest_black_pixel_y - c_cursor[1]



                    #draw a rectangle around a batch of blask pixels that is more than 2x2 pixels
                    cv2.rectangle(img, (int(black_pixels[0][1]), int(black_pixels[0][0])), (int(black_pixels[-1][1]), int(black_pixels[-1][0])), (0,0,255), thickness=1)


                    #get the length and width of the rectangle
                    length = int(black_pixels[-1][1]) - int(black_pixels[0][1])
                    width = int(black_pixels[-1][0]) - int(black_pixels[0][0])


                    #invert the image colors
                    img = cv2.bitwise_not(img)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # distance-transform
                    dist = cv2.distanceTransform(~gray, cv2.DIST_L1, 3)
                    # max distance
                    k = 10
                    bw = np.uint8(dist < k)
                    # remove extra padding created by distance-transform
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
                    bw2 = cv2.morphologyEx(bw, cv2.MORPH_ERODE, kernel)
                    # clusters
                    contours, hierarchy = cv2.findContours(bw2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    # draw clusters and bounding-boxes
                    i = 0
                    print(len(contours))
                    all_players = []
                    for cnt in contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.drawContours(img, contours, i, (0, 0, 255), 2)
                        i += 1
                        height = y+h
                        width = x+w
                        center_rect = np.array([int((x+width)/2), int((y+height)/2)])
                        all_players.append(center_rect)
                    #invert the image colors
                    img = cv2.bitwise_not(img)


                    for center_rect in all_players:
                        #draw a red line from every corner of the image to the center of all of the rectangles in the image
                        cv2.line(img, (0, 0), (center_rect[0], center_rect[1]), (0, 0, 255), 1)
                        cv2.line(img, (view, 0), (center_rect[0], center_rect[1]), (0, 0, 255), 1)
                        cv2.line(img, (0, view), (center_rect[0], center_rect[1]), (0, 0, 255), 1)
                        cv2.line(img, (view, view), (center_rect[0], center_rect[1]), (0, 0, 255), 1)


                
                    closest_black_pixel = np.array([closest_black_pixel[1], closest_black_pixel[0]])

                    #get the length of all the lines from the corners to the closest black pixel
                    top_left = np.linalg.norm(closest_black_pixel - np.array([0, 0]))
                    top_right = np.linalg.norm(closest_black_pixel - np.array([view, 0]))
                    bottom_left = np.linalg.norm(closest_black_pixel - np.array([0, view]))
                    bottom_right = np.linalg.norm(closest_black_pixel - np.array([view, view]))

                    #print(f"top left: {top_left}, top right: {top_right}, bottom left: {bottom_left}, bottom right: {bottom_right}")

                    #convert the 4 lines into a 300x300 plot with the 4 corners as the 4 corners of the plot
                    top_left = np.interp(top_left, (0, view), (0, view))
                    top_right = np.interp(top_right, (0, view), (0, view))
                    bottom_left = np.interp(bottom_left, (0, view), (0, view))
                    bottom_right = np.interp(bottom_right, (0, view), (0, view))

                    #print(f"top left: {top_left}, top right: {top_right}, bottom left: {bottom_left}, bottom right: {bottom_right}")

                    #draw a horizontal line with y=0 and x = center of the rectangle
                    cv2.line(img, (int(center_rect[0]), 0), (int(center_rect[0]), view), (0, 0, 255), 1)
                    #draw a vertical line with x=0 and y = center of the rectangle
                    cv2.line(img, (0, int(center_rect[1])), (view, int(center_rect[1])), (0, 0, 255), 1)

                    #pixels from center of square to bottom of the screen
                    bottom = np.linalg.norm(center_rect - np.array([int(center_rect[0]), view]))
                    #pixels from the center of the square to the left of the screen
                    left = np.linalg.norm(center_rect - np.array([0, int(center_rect[1])]))

                    #print(f"y: {bottom - 150}, x: {left - 150}")
                    #print(f"top left: {top_left}, top right: {top_right}, bottom left: {bottom_left}, bottom right: {bottom_right}")

                    c_cursor = pyautogui.position()

                    #if (int(bottom) - 150) is positive, make it negative, and vice versa
                    if (int(bottom) - 150) > 0:
                        bottom_new = (int(bottom) - 150) * -1

                    else:
                        bottom_new = (int(bottom) - 150) * -1

    


                    print(f"{(int(left) - 150)} and {bottom_new}")

                    win32api.mouse_event(0x0001,(int(left) - 150), bottom_new)
                    win32api.mouse_event(0x0001,(int(left) - 150), bottom_new)

                    

                    #resize output to 600x600
                    #img = cv2.resize(img, (600, 600))
                    # cv2.imshow('screen', img)

                check_pink()

                if not is_mouse_down():
                    break
                
                if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    cv2.destroyAllWindows()
                    break

