from src.pose_estimator.pose_detector import PoseDetector
from src.pose_estimator.warm_up import WarmUp
from src.pose_estimator.full_body_workout import FullBodyWorkout
from src.pose_estimator.intensed_leg_workout import LegWorkout
from src.workout_logic import date_wise_plan
import pandas as pd
from flask_socketio import SocketIO
from config import Config
import datetime,time
import cv2
import os

from src.pose_estimator.warm_up import WarmUp
from src.pose_estimator.full_body_workout import FullBodyWorkout
from src.pose_estimator.intensed_upper_body_push import UpperBodyPush
import pandas as pd
from config import Config
from datetime import datetime 
import cv2
import os
from flask import Flask, render_template, Response ,url_for ,jsonify

# Initialize Flask
app = Flask(__name__, template_folder="src/web/templates", static_folder="src/web/static")
socketio = SocketIO(app, cors_allowed_origins="*")


workout_function=LegWorkout()
full_body = FullBodyWorkout()
upper_body_push = UpperBodyPush()
full_report = []
cwd = os.getcwd()
counter=0

# Initialize Pose Detector
detector = PoseDetector(
    Config.MIN_DETECTION_CONFIDENCE,
    Config.MIN_TRACKING_CONFIDENCE
)

cap = cv2.VideoCapture(1)  # Using webcam


prev_counter, prev_set = -1, -1  # Track previous values

def generate_frames():
    global prev_counter, prev_set
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

            # Only emit if values change
            if counter != prev_counter or set != prev_set:
                workout_data = {
                    "workout_type": workout_type,  # Match the key expected in JavaScript
                    "current_rep": f"{counter}/{reps_required}",
                    "total_reps": reps_required,
                    "total_time": end_time,
                    "total_set": total_sets,
                    "current_set": f"{set}/{total_sets}",
                    "current_time": time.strftime("%H:%M:%S", time.localtime())
                }
                socketio.emit("update_workout",workout_data)
                prev_counter, prev_set = counter, set  # Update previous values

            print(counter)

        except Exception as e:
            print(f"Error: {e}")

        _, buffer = cv2.imencode('.jpg', image)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    

if __name__ == "__main__":
    print("Starting Exercise Tracker UI...")
    socketio.start_background_task(target=generate_frames)
    socketio.run(app,debug=True,allow_unsafe_werkzeug=True)
