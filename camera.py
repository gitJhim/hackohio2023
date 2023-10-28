#!/usr/bin/env python3
import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX
kernel = np.ones((5, 5), np.uint8)

# Junk Paramater for createTrackbar
def nothing(x):
    pass

def find_max_index(arr):
    max_index = 0
    if(arr[1] > arr[0]): max_index = 1
    if(arr[2] > arr[1]): max_index = 2
    return max_index

# init sliders for all colors
def create_trackbars(name):
    if(name == "Blue"):
        cv2.createTrackbar("L-H-B", name, 102, 180, nothing)
        cv2.createTrackbar("L-S-B", name, 123, 255, nothing)
        cv2.createTrackbar("L-V-B", name, 0, 255, nothing)
        cv2.createTrackbar("U-H-B", name, 113, 180, nothing)
        cv2.createTrackbar("U-S-B", name, 255, 255, nothing)
        cv2.createTrackbar("U-V-B", name, 188, 255, nothing)
    elif(name == "Green"):
        cv2.createTrackbar("L-H-G", name, 72, 180, nothing)
        cv2.createTrackbar("L-S-G", name, 99, 255, nothing)
        cv2.createTrackbar("L-V-G", name, 73, 255, nothing)
        cv2.createTrackbar("U-H-G", name, 134, 180, nothing)
        cv2.createTrackbar("U-S-G", name, 255, 255, nothing)
        cv2.createTrackbar("U-V-G", name, 121, 255, nothing)

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

    return hsv_arr

def manage_contours(contour, frame, color):
    for cnt in contour:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.025*cv2.arcLength(cnt, True), True)

        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (160, 255, 0), 2)

            if len(approx) == 3:
                if(color == "blue"):
                    cv2.putText(frame, "Blue Triangle", (x, y), font, 1, (160, 255, 0))
                    print("Blue Triangle") 
                elif(color == "green"):
                    cv2.putText(frame, "Green Triangle", (x, y), font, 1, (160, 255, 0))
                    print("Green Triangle") 
            elif len(approx) == 4:
                if(color == "blue"):
                    cv2.putText(frame, "Blue Rectangle", (x, y), font, 1, (160, 255, 0))
                    print("Blue Rectangle")
                elif(color == "green"):
                    cv2.putText(frame, "Green Rectangle", (x, y), font, 1, (160, 255, 0))
                    print("Green Rectangle")
            elif len(approx) >= 8:
                if(color == "blue"):
                    cv2.putText(frame, "Blue Circle", (x, y), font, 1, (160, 255, 0))
                    print("Blue Circle")
                elif(color == "green"):
                    cv2.putText(frame, "Green Circle", (x, y), font, 1, (160, 255, 0))
                    print("Green Circle")


def start_camera():
    # init video
    video_capture = cv2.VideoCapture(0)

    # blue slider window
    cv2.namedWindow("Blue")
    create_trackbars("Blue")

    # green slider window
    cv2.namedWindow("Green")
    create_trackbars("Green")



    # frame_number = 0
    # shape_count = [0] * 3
    while True:
        # if(frame_number == 75):
        #    max_index = find_max_index(shape_count) 
        #    if max_index == 1:
        #        print("")
        _, frame = video_capture.read()

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        blue_vals = get_all_trackbar_positions("Blue")
        green_vals = get_all_trackbar_positions("Green")
        
        lower_blue = np.array([blue_vals[0], blue_vals[1], blue_vals[2]])
        upper_blue = np.array([blue_vals[3], blue_vals[4], blue_vals[5]])

        lower_green= np.array([green_vals[0], green_vals[1], green_vals[2]])
        upper_green= np.array([green_vals[3], green_vals[4], green_vals[5]])

        mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        mask_blue = cv2.erode(mask_blue, kernel)

        mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
        mask_green= cv2.erode(mask_green, kernel)

       # Countour detection
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        manage_contours(contours_blue, frame, "blue")
        manage_contours(contours_green, frame, "green")

        # cv2.imshow("Frame", frame)
        # cv2.imshow("Blue Mask", mask_blue)
        # cv2.imshow("Green Mask", mask_green)

        key = cv2.waitKey(1)
        if(key == 27):
            break

    video_capture.release()
    cv2.destroyAllWindows()


