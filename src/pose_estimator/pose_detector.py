import cv2
import mediapipe as mp 
from src.constant import MIN_DETECTION_CONFIDENCE,MIN_TRACKING_CONFIDECNE


from src.logger import logging

class PoseDetector:
    def __init__(self,min_detection_confidence=MIN_DETECTION_CONFIDENCE,
                 min_tracking_confidence=MIN_TRACKING_CONFIDECNE):
        self.mp_pose=mp.solutions.pose
        self.pose=self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing=mp.solutions.drawing_utils
        logging.info("Initization of Mediapipe Pose detection....")

    def detect_pose(self,frame):
        """This function withh return the image ,result"""
        image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)   #conveting BGR2RGB for mediapipe to read.
        image.flags.writeable=False
        
        results=self.pose.process(image)

        image.flags.writeable=True
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)   #conveting RGB2BGR for display.

        logging.info("Image and result from pose-dectetor achived...")
        return image,results

        
    def draw_landmarks(self,image,results):
        """This function will drawlandmarks in image fotage."""
        self.mp_drawing.draw_landmarks(
            image,results.pose_landmarks,self.mp_pose.POSE_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2))
        return image,results


