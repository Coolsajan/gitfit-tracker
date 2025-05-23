from datetime import datetime
import ast
import cv2
import pandas as pd
import time
from flask import Flask, render_template, Response, url_for
from flask_socketio import SocketIO, emit

from config import Config
from src.pose_estimator.full_body_workout import FullBodyWorkout
from src.pose_estimator.core_workout import CoreWorkout
from src.pose_estimator.intensed_leg_workout import LegWorkout
from src.pose_estimator.intensed_upper_body_pull_workout import UpperBodyPullWorkout
from src.pose_estimator.intensed_upper_body_push import UpperBodyPush
from src.pose_estimator.pose_detector import PoseDetector

# Define workout schedule
workout_schedule = {
    "Sunday": UpperBodyPush(),
    "Monday": LegWorkout(),
    "Tuesday": CoreWorkout(),
    "Wednesday": UpperBodyPullWorkout(),
    "Friday": FullBodyWorkout()
}

# Initialize Flask app
app = Flask(__name__, template_folder="src/web/templates", static_folder="src/web/static")
socketio = SocketIO(app, cors_allowed_origins="*",async_mode="eventlet")

# Initialize workout function and tracking variables
workout_function = FullBodyWorkout()
full_report = []
prev_counter, prev_set = -1, -1
enable_recording = False

# Initialize pose detector
detector = PoseDetector(
    Config.MIN_DETECTION_CONFIDENCE,
    Config.MIN_TRACKING_CONFIDENCE
)

# Start webcam capture with error handling
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

def generate_frames():
    global prev_counter, prev_set, enable_recording

    while True:
        if not enable_recording:
            #time.sleep(0.5)  # Prevent infinite loop from using CPU unnecessarily
            continue

        success, frame = cap.read()
        if not success:
            print("Error: Could not read frame from camera.")
            break

        # Pose detection
        image, results = detector.detect_pose(frame)

        try:
            landmarks = results.pose_landmarks.landmark
            workout_data = workout_function.initiate_workout(landmarks=landmarks)
            (
                workout_updates, total_time, counter, reps_required, current_set,
                total_sets, resting_time, rest_time, total_rest_time, reps_completed, workoutplan
            ) = workout_data
            
            # Convert workout plan string to dictionary
            try:
                workoutplan = ast.literal_eval(workoutplan)  # Ensure it's safe
            except (SyntaxError, ValueError):
                print("Warning: Invalid workout plan format.")
                workoutplan = {}

            socketio.emit("workoutplan", workoutplan)

            # Emit real-time workout data
            current_time = datetime.now().strftime('%H:%M:%S')
            workout_status = {
                "workout_type": workout_updates,
                "current_rep_total_reps": f"{counter}/{reps_required}",
                "current_rep": counter,
                "total_reps": reps_required,
                "total_time": total_time,
                "total_sets": total_sets,
                "total_set_completed": 0,
                "current_set_total_sets": f"{current_set}/{total_sets}",
                "current_set": current_set,
                "current_time": current_time,
                "current_rest_time": resting_time,
                "rest_time": round(rest_time - resting_time),
                "set_rest_time": rest_time,
                "total_rest_time": total_rest_time,
                "total_reps_done": reps_completed
            }
            socketio.emit("update_workout", workout_status)
            # Track workout progress

            if prev_counter != counter or prev_set != current_set:
                report = {
                    "Workout Name": workout_updates,
                    "Reps": counter,
                    "Set": current_set,
                    "Time": total_time,
                    "Rest Time": resting_time
                }
                full_report.append(report)
                prev_counter, prev_set = counter, current_set
                print(full_report)

                # Save workout report to CSV
                df = pd.DataFrame(full_report)
                df.to_csv("workout.csv", index=False)
            
            
            
        except Exception as e:
            print(f"Error: {e}")
        
        _, buffer = cv2.imencode('.jpg', image)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# Flask routes
@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/recordworkout')
def record_workout():
    global enable_recording
    enable_recording = True
    return render_template('index.html')

@socketio.on("submit_workout")
def handle_submit(data):
    name = data["name"]
    emit('redirect', {'url': url_for('record_workout')}, broadcast=False)  # Redirecting to the workout page

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("Starting Exercise Tracker UI...")
    socketio.run(app, debug=True)
