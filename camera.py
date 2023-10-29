#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep

font = cv2.FONT_HERSHEY_COMPLEX
kernel = np.ones((5, 5), np.uint8)

# Junk Paramater for createTrackbar
def nothing(x):
    pass

def find_max_index(arr):
    max_index = -1
    first_iteration = True
    for i in range (len(arr)):
        if(first_iteration):    
            if(arr[i] > arr[0]):
                max_index = i
            max_index = 0
        else:
            if(arr[i] > arr[max_index]):
                max_index = i
    return max_index

# init sliders for all colors
def create_trackbars(name):
    if(name == "Blue"):
        cv2.createTrackbar("L-H-B", name, 112, 180, nothing)
        cv2.createTrackbar("L-S-B", name, 110, 255, nothing)
        cv2.createTrackbar("L-V-B", name, 56, 255, nothing)
        cv2.createTrackbar("U-H-B", name, 124, 180, nothing)
        cv2.createTrackbar("U-S-B", name, 169, 255, nothing)
        cv2.createTrackbar("U-V-B", name, 115, 255, nothing)
    elif(name == "Green"):
        cv2.createTrackbar("L-H-G", name, 67, 180, nothing)
        cv2.createTrackbar("L-S-G", name, 152, 255, nothing)
        cv2.createTrackbar("L-V-G", name, 91, 255, nothing)
        cv2.createTrackbar("U-H-G", name, 87, 180, nothing)
        cv2.createTrackbar("U-S-G", name, 210, 255, nothing)
        cv2.createTrackbar("U-V-G", name, 121, 255, nothing)
    elif(name == "Red"):
        cv2.createTrackbar("L-H-R", name, 106, 180, nothing)
        cv2.createTrackbar("L-S-R", name, 243, 255, nothing)
        cv2.createTrackbar("L-V-R", name, 0, 255, nothing)
        cv2.createTrackbar("U-H-R", name, 180, 180, nothing)
        cv2.createTrackbar("U-S-R", name, 255, 255, nothing)
        cv2.createTrackbar("U-V-R", name, 231, 255, nothing)

def get_all_trackbar_positions(name):
    # 0-2 are the lower hsv values 3-5 are the upper vals
    hsv_arr = [0] * 6 
    if(name == "Blue"):
        hsv_arr[0] = cv2.getTrackbarPos("L-H-B", name)
        hsv_arr[1] = cv2.getTrackbarPos("L-S-B", name)
        hsv_arr[2] = cv2.getTrackbarPos("L-V-B", name)
        hsv_arr[3] = cv2.getTrackbarPos("U-H-B", name)
        hsv_arr[4] = cv2.getTrackbarPos("U-S-B", name)
        hsv_arr[5] = cv2.getTrackbarPos("U-V-B", name)
    elif(name == "Green"):
        hsv_arr[0] = cv2.getTrackbarPos("L-H-G", name)
        hsv_arr[1] = cv2.getTrackbarPos("L-S-G", name)
        hsv_arr[2] = cv2.getTrackbarPos("L-V-G", name)
        hsv_arr[3] = cv2.getTrackbarPos("U-H-G", name)
        hsv_arr[4] = cv2.getTrackbarPos("U-S-G", name)
        hsv_arr[5] = cv2.getTrackbarPos("U-V-G", name)
    elif(name == "Red"):
        hsv_arr[0] = cv2.getTrackbarPos("L-H-R", name)
        hsv_arr[1] = cv2.getTrackbarPos("L-S-R", name)
        hsv_arr[2] = cv2.getTrackbarPos("L-V-R", name)
        hsv_arr[3] = cv2.getTrackbarPos("U-H-R", name)
        hsv_arr[4] = cv2.getTrackbarPos("U-S-R", name)
        hsv_arr[5] = cv2.getTrackbarPos("U-V-R", name)

    return hsv_arr

def manage_contours(contour, frame, color):
    ret_val = -1
    for cnt in contour:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.025*cv2.arcLength(cnt, True), True)

        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 1500:
            cv2.drawContours(frame, [approx], 0, (160, 255, 0), 2)

            if len(approx) == 3:
                if(color == "blue"):
                    cv2.putText(frame, "Blue Triangle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 0
                    # print("Blue Triangle") 
                elif(color == "green"):
                    cv2.putText(frame, "Green Triangle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 1
                    # print("Green Triangle") 
                elif(color == "red"):
                    cv2.putText(frame, "Red Triangle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 2
                    # print("Green Triangle") 

            elif len(approx) == 4:
                if(color == "blue"):
                    cv2.putText(frame, "Blue Rectangle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 3
                elif(color == "green"):
                    cv2.putText(frame, "Green Rectangle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 4
                elif(color == "red"):
                    cv2.putText(frame, "Red Rectangle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 5

            elif len(approx) >= 8:
                if(color == "blue"):
                    cv2.putText(frame, "Blue Circle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 6
                    # print("Blue Circle")
                elif(color == "green"):
                    cv2.putText(frame, "Green Circle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 7
                    # print("Green Circle")
                elif(color == "red"):
                    cv2.putText(frame, "Red Circle", (x, y), font, 1, (160, 255, 0))
                    ret_val = 8

    print(ret_val)
    return ret_val


def start_camera():
    # init video
    video_capture = cv2.VideoCapture('static/final-video.mp4')

    # blue slider window
    cv2.namedWindow("Blue")
    create_trackbars("Blue")

    # green slider window
    cv2.namedWindow("Green")
    create_trackbars("Green")

    # red slider window
    cv2.namedWindow("Red")
    create_trackbars("Red")

    # frame_number = 0
    # shape_count = [0] * 3
    while True:
        # if(frame_number == 75):
        #    max_index = find_max_index(shape_count) 
        #    if max_index == 1:
        #        print("")
        _, frame = video_capture.read()

        frame = cv2.resize(frame, (800, 480))

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        blue_vals = get_all_trackbar_positions("Blue")
        green_vals = get_all_trackbar_positions("Green")
        red_vals = get_all_trackbar_positions("Red")
        
        lower_blue = np.array([blue_vals[0], blue_vals[1], blue_vals[2]])
        upper_blue = np.array([blue_vals[3], blue_vals[4], blue_vals[5]])

        lower_green= np.array([green_vals[0], green_vals[1], green_vals[2]])
        upper_green= np.array([green_vals[3], green_vals[4], green_vals[5]])

        lower_red= np.array([red_vals[0], red_vals[1], red_vals[2]])
        upper_red= np.array([red_vals[3], red_vals[4], red_vals[5]])

        mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        mask_blue = cv2.erode(mask_blue, kernel)

        mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
        mask_green= cv2.erode(mask_green, kernel)

        mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
        mask_red = cv2.erode(mask_red, kernel)

       # Countour detection
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        manage_contours(contours_blue, frame, "blue")
        manage_contours(contours_green, frame, "green")
        manage_contours(contours_red, frame, "red")

        cv2.imshow("Frame", frame)
        # cv2.imshow("Blue Mask", mask_blue)
        # cv2.imshow("Green Mask", mask_green)
        cv2.imshow("Red Mask", mask_red)

        sleep(0.015)
        key = cv2.waitKey(1)
        if(key == 27):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera()


