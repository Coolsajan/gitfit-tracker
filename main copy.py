from src.pose_estimator.pose_detector import PoseDetector
from src.pose_estimator.warm_up import WarmUp
from src.pose_estimator.full_body_workout import FullBodyWorkout
from src.pose_estimator.intensed_upper_body_push import UpperBodyPush
from src.pose_estimator.intensed_leg_workout import LegWorkout
import pandas as pd
from config import Config
from datetime import datetime 
import cv2
import os

# Initialize FullBodyWorkoutq
leg=LegWorkout()
full_body = FullBodyWorkout()
upper_body_push=UpperBodyPush()
full_report = []
cwd=os.getcwd()

def main():
    # Initialize pose detector
    detector = PoseDetector(
        Config.MIN_DETECTION_CONFIDENCE,
        Config.MIN_TRACKING_CONFIDENCE
    )

    cap = cv2.VideoCapture(1)  # Using webcam

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Error: Could not read frame")
            break

        # Pose detection
        image, results = detector.detect_pose(frame)

        

        try:
            landmarks = results.pose_landmarks.landmark
            workout_name,counter , reps_required ,set,total_sets,end_time ,workout_list = (
                leg.initiate_workout(landmarks=landmarks)
            )

            report={"Workout Name":{workout_name},
                "Current Rep":f"{counter}/{reps_required}",
                    "Current Set":f"{set}/{total_sets}",
                    "workout time":{end_time},
                    }
            full_report.append(report)
            print(f"Report: {report}")

            # Get current time
            current_time = datetime.now().strftime('%H:%M:%S')


            cv2.rectangle(image,(800,00),(540,700),(225,0,0),5)
            cv2.rectangle(image,(800,00),(540,700),(93,84,75),-1)
            cv2.rectangle(image,(00,400),(800,700),(93,84,75),-1)

            # Overlay text on video
            cv2.putText(image, f"Current Rep : {counter}/{reps_required}", 
                        (10, 420), cv2.FONT_HERSHEY_TRIPLEX , 0.9, (225, 225, 225), 1)
            cv2.putText(image, f"Current Set : {set}/{total_sets}", 
                        (10, 460), cv2.FONT_HERSHEY_TRIPLEX , 0.9, (225, 225, 225), 1)
            
            
            cv2.putText(image, f"Workout Time:{round(end_time)} sec", 
                        (10, 30), cv2.FONT_HERSHEY_TRIPLEX , 0.9, (225, 0, 225), 1)

        except Exception as e:
            print(f"Error: {e}")

        cv2.namedWindow("Exercise Tracker",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Exercise Tracker",900,700)
        # Display the video
        cv2.imshow('Exercise Tracker', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

    # Save and display full report
    if full_report:
        df = pd.DataFrame(full_report)
        df.to_csv("sunday.csv",index=False)
        print(df)
    else:
        print("No report data collected.")

if __name__ == "__main__":
    main()
