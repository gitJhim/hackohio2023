from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from camera import manage_contours, find_max_index

app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)

kernel = np.ones((5, 5), np.uint8)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():  # generate frame by frame from camera

    global out, capture,rec_frame
    frame_number = 0;
    shape_count = [0] * 6
    while True:
        if frame_number == 75:
            max_index = find_max_index(shape_count)
            if(max_index == 0):
                print("Blue Triangle") 
            elif(max_index == 1):
                print("Green Triangle") 
            elif(max_index == 2):
                print("Blue Rectangle")
            elif(max_index == 3):
                print("Green Rectangle")
            elif(max_index == 4):
                print("Blue Circle")
            elif(max_index == 5):
                print("Green Circle")
            frame_number = 0
            shape_count = [0] * 6
                
        _, frame = camera.read()

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        blue_vals = [102, 123, 0, 113, 255, 188]
        green_vals = [72, 99, 73, 134, 255, 121]

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

        shape_count_index = manage_contours(contours_blue, frame, "blue")
        if(shape_count_index > -1):
            shape_count[shape_count_index] += 1

        shape_count_index = manage_contours(contours_green, frame, "green")
        if(shape_count_index > -1):
            shape_count[shape_count_index] += 1
        
        frame_number += 1

        try:
             ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
             frame = buffer.tobytes()
             yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
             pass
                
        else:
            pass

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()