from flask import Flask, render_template, Response, request
import cv2
from flask_socketio import SocketIO
import numpy as np
from threading import Thread
from camera import manage_contours, find_max_index
from time import sleep

sleep(2)

app = Flask(__name__, template_folder='./templates')
socketio = SocketIO(app) 

camera = cv2.VideoCapture(0)

kernel = np.ones((5, 5), np.uint8)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():  # generate frame by frame from camera

    global out, capture,rec_frame
    frame_number = 0
    shape_count = [0] * 10 
    while True:
        if frame_number == 45:
            max_index = find_max_index(shape_count)
            # print(max_index)
            if(max_index == 1):
                print("Blue Triangle") 
                socketio.emit('update', {'data': 'Blue Triangle'})
            elif(max_index == 2):
                print("Green Triangle") 
                socketio.emit('update', {'data': 'Green Triangle'})
            elif(max_index == 3):
                print("Red Triangle")
                socketio.emit('update', {'data': 'Red Triangle'})
            elif(max_index == 4):
                print("Blue Rectangle")
                socketio.emit('update', {'data': 'Blue Rectangle'})
            elif(max_index == 5):
                print("Green Rectangle")
                socketio.emit('update', {'data': 'Green Rectangle'})
            elif(max_index == 6):
                print("Red Rectangle")
                socketio.emit('update', {'data': 'Red Rectangle'})
            elif(max_index == 7):
                print("Blue Circle")
                socketio.emit('update', {'data': 'Blue Circle'})
            elif(max_index == 8):
                print("Green Circle")
                socketio.emit('update', {'data': 'Green Circle'})  
            elif(max_index == 9):
                print("Red Circle")
                socketio.emit('update', {'data': 'Red Circle'})
            else:
                socketio.emit('update', {'data': 'None'})
                
            frame_number = 0
            shape_count = [0] * 10 
                
        _, frame = camera.read()

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        blue_vals = [88, 147, 144, 132, 255, 115]
        green_vals = [67, 152, 91, 87, 210, 229]
        red_vals = [106, 243, 0, 180, 255, 231]

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

        shape_count_index = manage_contours(contours_blue, frame, "blue")
        if(shape_count_index > -1):
            shape_count[shape_count_index] += 1

        shape_count_index = manage_contours(contours_green, frame, "green")
        if(shape_count_index > -1):
            shape_count[shape_count_index] += 1

        shape_count_index = manage_contours(contours_red, frame, "red")
        if(shape_count_index > -1):
            shape_count[shape_count_index] += 1
        
        frame_number += 1
        sleep(0.015)
        try:
             frame = cv2.flip(frame, 1)
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