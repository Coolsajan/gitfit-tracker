import mediapipe as mp
from src.utils.common_utils import calculate_angle

class ExerciseClassifier:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.exercise_types = {
            'bicep_curl': self.detect_bicep_curl,
            'squat': self.detect_squat,
            'shoulder_press': self.detect_shoulder_press,
            'lateral_raise': self.detect_lateral_raise
        }
    
    def get_landmarks(self, landmarks, pose_part):
        """Get normalized coordinates of specific body part"""
        return [
            landmarks[self.mp_pose.PoseLandmark[pose_part].value].x,
            landmarks[self.mp_pose.PoseLandmark[pose_part].value].y
        ]

    def detect_bicep_curl(self, landmarks):
        """Detect bicep curl form"""
        left_shoulder = self.get_landmarks(landmarks, 'LEFT_SHOULDER')
        left_elbow = self.get_landmarks(landmarks, 'LEFT_ELBOW')
        left_wrist = self.get_landmarks(landmarks, 'LEFT_WRIST')
        
        
        right_shoulder = self.get_landmarks(landmarks, 'RIGHT_SHOULDER')
        right_elbow = self.get_landmarks(landmarks, 'RIGHT_ELBOW')
        right_wrist = self.get_landmarks(landmarks, 'RIGHT_WRIST')
        
        angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        angle = calculate_angle(right_shoulder, right_elbow, right_wrist)


        return angle, 'bicep_curl'

    def detect_squat(self, landmarks):
        """Detect squat form"""
        left_hip = self.get_landmarks(landmarks, 'LEFT_HIP')
        left_knee = self.get_landmarks(landmarks, 'LEFT_KNEE')
        left_ankle = self.get_landmarks(landmarks, 'LEFT_ANKLE')
        
        angle = calculate_angle(left_hip, left_knee, left_ankle)
        return angle, 'squat'

    def detect_shoulder_press(self, landmarks):
        """Detect shoulder press form"""
        left_shoulder = self.get_landmarks(landmarks, 'LEFT_SHOULDER')
        left_elbow = self.get_landmarks(landmarks, 'LEFT_ELBOW')
        left_wrist = self.get_landmarks(landmarks, 'LEFT_WRIST')
        
        # Vertical angle calculation
        angle = calculate_angle(left_elbow, left_shoulder, left_wrist)
        return angle, 'shoulder_press'

    def detect_lateral_raise(self, landmarks):
        """Detect lateral raise form"""
        left_shoulder = self.get_landmarks(landmarks, 'LEFT_SHOULDER')
        left_elbow = self.get_landmarks(landmarks, 'LEFT_ELBOW')
        left_wrist = self.get_landmarks(landmarks, 'LEFT_WRIST')
        
        # Horizontal angle calculation
        angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        return angle, 'lateral_raise'

    def classify_exercise(self, landmarks, previous_type=None ):
        """Main classification function"""
        if not landmarks:
            return None, 0
        
        max_confidence = 0
        detected_exercise = 'Rest'
        
        # Check all exercise types
        for exercise, detector in self.exercise_types.items():
            angle, exercise_type = detector(landmarks)
            
            # Define confidence thresholds for each exercise
            confidence = self._calculate_confidence(exercise_type, angle)
            
            if confidence > max_confidence:
                max_confidence = confidence
                detected_exercise = exercise_type
        
        return detected_exercise, max_confidence 

    def _calculate_confidence(self, exercise_type, angle):
        """Calculate confidence score based on exercise-specific thresholds"""

        thresholds = {
            'bicep_curl': (40, 160),
            'squat': (80, 170),
            'shoulder_press': (160, 180),
            'lateral_raise': (75, 150)
        }

        lower, upper = thresholds.get(exercise_type, (0, 0))

        normalized = max(0, min(1, (angle - lower) / (upper - lower)))
        return 1 - abs(0.5 - normalized) * 2
        


    
