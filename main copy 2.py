from src.pose_estimator.pose_detector import PoseDetector
from src.pose_estimator.full_body_workout import FullBodyWorkout
from src.pose_estimator.intensed_upper_body_push import UpperBodyPush
from src.pose_estimator.intensed_leg_workout import LegWorkout

from config import Config
from datetime import datetime,time 
import cv2 ,os
from flask import Flask, render_template, Response 
from flask_sockets import Sockets



# Initialize Flask
app = Flask(__name__, template_folder="src/web/templates", static_folder="src/web/static")
sockets=Sockets(app)
# Initialize FullBodyWorkout
workout_function=LegWorkout()
counter=0

# Initialize Pose Detector
detector = PoseDetector(
    Config.MIN_DETECTION_CONFIDENCE,
    Config.MIN_TRACKING_CONFIDENCE )

cap = cv2.VideoCapture(1)  # Using webcam

def generate_frames():
    global prev_set ,prev_counter
    prev_set ,prev_counter = -1,-1
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Pose detection
        image, results = detector.detect_pose(frame)

        try:
            landmarks = results.pose_landmarks.landmark
            workout_type, counter, reps_required, set, total_sets, end_time, workout_list = (
                workout_function.initiate_workout(landmarks=landmarks)
            )

            # Get current time
            current_time = datetime.now().strftime('%H:%M:%S')

            if prev_counter!=counter or prev_set!=set:
                workout_data = {
                    "workout_type": workout_type,  # Match the key expected in JavaScript
                    "current_rep": f"{counter}/{reps_required}",
                    "total_reps": reps_required,
                    "total_time": end_time,
                    "total_set": total_sets,
                    "current_set": f"{set}/{total_sets}",
                    "current_time": current_time
                }
                sockets.send("update_workout",workout_data)
                prev_set,prev_counter=set,counter  
                print(counter,prev_counter)
                
            
        except Exception as e:
            print(f"Error: {e}")



print(counter)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print("Starting Exercise Tracker UI...")
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server=pywsgi.WSGIServer(("0.0.0.0",5000),app,handler_class=WebSocketHandler)
    server.serve_forever()