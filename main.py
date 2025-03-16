from src.pose_estimator.pose_detector import PoseDetector
from src.pose_estimator.warm_up import WarmUp
from src.pose_estimator.full_body_workout import FullBodyWorkout
import pandas as pd
from config import Config
from datetime import datetime
import cv2

# Initialize FullBodyWorkoutq
full_body = FullBodyWorkout()
full_report = []

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
            report, warmup_type, step, execution_count, elapsed_time, next_warmup ,current_set = (
                full_body.initiate_full_body(landmarks=landmarks)
            )

            # Store the report
            full_report.append(report)
            print(f"Report: {report}")

            # Get current time
            current_time = datetime.now().strftime('%H:%M:%S')



            cv2.rectangle(image,(800,00),(540,700),(93,84,75),-1)
            cv2.rectangle(image,(00,400),(800,700),(93,84,75),-1)

            # Overlay text on video
            cv2.putText(image, f"{warmup_type} : Reps: {execution_count}, Current Set: {current_set}", 
                        (10,430), cv2.FONT_HERSHEY_TRIPLEX, 0.9, (225, 225, 225), 1)
            cv2.putText(image, f"{step}", 
                        (10, 460), cv2.FONT_HERSHEY_TRIPLEX , 0.9, (225, 225, 225), 1)
            
            cv2.putText(image, f"Workout Time:{round(elapsed_time)} sec", 
                        (10, 30), cv2.FONT_HERSHEY_TRIPLEX , 0.9, (225, 225, 225), 1)

        except Exception as e:
            print(f"Error: {e}")

        cv2.namedWindow("Exercise Tracker",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Exercise Tracker",800,700)
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
        print(df)
    else:
        print("No report data collected.")

if __name__ == "__main__":
    main()
