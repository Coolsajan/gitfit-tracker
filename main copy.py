from src.pose_estimator.full_body_workout import FullBodyWorkout
from src.pose_estimator.core_workout import CoreWorkout
from src.pose_estimator.intensed_leg_workout import LegWorkout
from src.pose_estimator.intensed_upper_body_pull_workout import UpperBodyPullWorkout
from src.pose_estimator.intensed_upper_body_push import UpperBodyPush
from src.pose_estimator.pose_detector import PoseDetector

from config import Config
from datetime import datetime 
import ast  ,json
import cv2 ,os
from flask import Flask, render_template, Response 
from flask_socketio import SocketIO
import pandas as pd

workout_schedule={
    "Sunday": UpperBodyPush(),
    "Monday" : LegWorkout(),
    "Tuesday" : CoreWorkout(),
    "Wednesday" : UpperBodyPullWorkout(),
    "Friday" : FullBodyWorkout()
}
# Initialize Flask
app = Flask(__name__, template_folder="src/web/templates", static_folder="src/web/static")
socketio=SocketIO(app,cors_allowed_origins="*")


workout_function= FullBodyWorkout()


full_report=[] 
prev_counter ,prev_set = -1,-1


detector = PoseDetector(
    Config.MIN_DETECTION_CONFIDENCE,
    Config.MIN_TRACKING_CONFIDENCE )

cap = cv2.VideoCapture(1)  # Using webcam

def generate_frames():
    global prev_counter ,prev_set 
    
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Pose detection
        image, results = detector.detect_pose(frame)

        try:
            landmarks = results.pose_landmarks.landmark          
               
            (workout_updates , total_time, counter ,reps_required ,current_set , total_sets ,resting_time ,rest_time ,total_rest_time,reps_completed, workoutplan)= (workout_function.initiate_workout(landmarks=landmarks))
         
  
            workoutplan = ast.literal_eval(workoutplan)
            socketio.emit("workoutplan",workoutplan)

            if prev_counter != counter or prev_set != current_set:
                report = {
                    "Workout Name": workout_updates,
                    "Reps": counter,
                    "Set": current_set,
                    "Time": total_time,
                    "rest_time":resting_time
                }
                full_report.append(report)
                
                # Update previous values
                prev_counter, prev_set = counter, current_set

                print(full_report)
            
            current_time = datetime.now().strftime('%H:%M:%S')

            
            print(f"Emitting update: Counter={counter}, Set={current_set}")  # Debug print
            workout_data = {
                "workout_type": workout_updates,
                "current_rep_total_reps": f"{counter}/{reps_required}",
                "current_rep":counter,
                "total_reps": reps_required,
                "total_time": total_time,
                "total_sets": total_sets,
                "total_set_completed":0,
                "current_set_total_sets": f"{current_set}/{total_sets}",
                "current_set":current_set,
                "current_time": current_time,
                "current_rest_time":resting_time,
                "rest_time":round(rest_time - resting_time),
                "set_rest_time":rest_time,
                "total_rest_time":total_rest_time,
                "total_reps_done":reps_completed
                
            }
            socketio.emit("update_workout", workout_data)      
            
        except Exception as e:
            print(f"Error: {e}")

        _, buffer = cv2.imencode('.jpg', image)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

df=pd.DataFrame(full_report)
print(df)
df.to_csv("hi.csv")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print("Starting Exercise Tracker UI...")
    socketio.run(app,debug=True)
