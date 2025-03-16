from src.utils.common_utils import calculate_angle,calculate_eq_distance,mind_point_finder
from src.constant import *
import mediapipe as mp
import datetime , time


class BegginerWorkout:
    def __init__(self):
        self.mp_pose=mp.solutions.pose
        self.counter=0
        self.set=1
        self.step="Relaxed"
        self.workout_index=0
        self.start_time=time.time()
        self.next_workout=" "
        self.bigginer_workout={
            "Knee Push Up":self.push_up,
            "Tricep Push UP":self.tricep_pushup,
            "Shoulder Tap":self.shoulder_taps,
            "Box Squat":self.box_squarts,
            "Crunches":self.crunches
        }

    def get_landmarks(self,landmarks,pose_part):
        """This will retrun the pose landmarks..."""
        return [
            landmarks[self.mp_pose.PoseLandmark[pose_part].value].x,
            landmarks[self.mp_pose.PoseLandmark[pose_part].value].y
        ]
       
    def box_squarts(self,landmarks):
        #COLLECTING LANDMARKS
        shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        ankle=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ANKLE")
        #CALCULATING ANGLE
        hip_angle=calculate_angle(a=shoulder,b=hip,c=knee)
        knee_angle=calculate_angle(a=hip,b=knee,c=ankle)

        if hip_angle < HIP_LOW_THRESHOLD_BOX_SQUART and knee_angle < KNEE_LOW_THRESHOLD_BOX_SQUART:
            self.step="DOWN"
        if hip_angle > HIP_HIGH_THRESHOLD_BOX_SQUART and knee_angle > KNEE_HIGH_THRESHOLD_BOX_SQUART and self.step=="DOWN":
            self.step="UP"
            self.counter+=1

        return self.step , self.counter
    
    def push_up(self,landmarks):
        """This will detect and record the pushup.."""
        #collecting landmarks
        shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        #calculating angle
        elbow_angle=calculate_angle(a=shoulder,b=elbow,c=wrist)

        if elbow_angle > 175:
            self.step="UP"
        if elbow_angle < 60 and self.step=="UP":
            self.step="DOWN"
            self.counter+=1

        return self.step , self.counter
    
    def tricep_pushup(self,landmarks):
        """This will detect and record the tricep pushup.."""
        #collecting landmarks
        shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        #calculating angle
        elbow_angle=calculate_angle(a=shoulder,b=elbow,c=wrist)

        if elbow_angle <= ELBOW_LOW_THRESHOLD_TRICEP_PUSH_UP:
            self.step="DOWN"
        if elbow_angle > ELBOW_HIGH_THRESHOLD_TRICEP_PUSH_UP and self.step=="DOWN":
            self.step="UP"
            self.counter+=1
            
        return self.step , self.counter
    
    def shoulder_taps(self,landmarks):
        """This will detect and record the shoulder taps..."""
        # collecting landmarks
        right_wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")

        left_wrist=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_WRIST")
        left_elbow=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ELBOW")
        left_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_SHOULDER")
        #calculating angle
        right_elbow_angle=calculate_angle(a=right_wrist,b=right_elbow,c=right_shoulder)
        left_elbow_angle=calculate_angle(a=left_wrist,b=left_elbow,c=left_shoulder)
        #calculating distance
        shoulder_dist=calculate_eq_distance(a=right_shoulder,b=left_shoulder)
        r_wrist_l_shoulder=calculate_eq_distance(a=right_wrist,b=left_shoulder)/shoulder_dist
        l_wrist_r_shoulder=calculate_eq_distance(a=left_wrist,b=right_shoulder)/shoulder_dist


        if right_elbow_angle > ELBOW_ANGLE_THRESHOLD_SHOULDER_TAP and r_wrist_l_shoulder < WRIST_SHOULDER_DISTANCE_SHOULDER_TAP :
            self.step="RIGHT SHOULDER TAPED"
        if left_elbow_angle > ELBOW_ANGLE_THRESHOLD_SHOULDER_TAP and l_wrist_r_shoulder < WRIST_SHOULDER_DISTANCE_SHOULDER_TAP  and self.step=="RIGHT SHOULDER TAPED":
            self.step="LEFT SHOULDER TAPED"
            self.counter+=1
        
        return self.step , self.counter
    
    def crunches(self,landmarks):
        """This will detect and record the russian twister"""

        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        right_wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")

        left_hip=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_HIP")
        left_wrist=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_WRIST")
        left_knee=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_KNEE")
        left_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_SHOULDER")

        right_hip_angle=calculate_angle(a=right_knee,b=right_hip,c=right_shoulder)
        left_hip_angle=calculate_angle(a=left_knee,b=left_hip,c=left_shoulder)

        if right_hip_angle > HIP_HIGH_THRESHOLD_CRUNCHES:
            self.step="OUT"
        if self.step=="OUT" and right_hip_angle < HIP_LOW_THRESHOLD_CRUNCHES:
            self.step="IN"
            self.counter+=1

        return self.step , self.counter 
    
    def skip_workout(self,landmarks):
        """This method with help us if we wanna to skip workout"""
        right_wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")

        left_wrist=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_WRIST")
        left_elbow=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ELBOW")

        right_mid_point=mind_point_finder(a=right_elbow,b=right_wrist)
        left_mid_point=mind_point_finder(a=left_elbow,b=left_wrist)

        distance_between_midpoint=calculate_eq_distance(a=right_mid_point,b=left_mid_point)
        if not hasattr(self,"timeout_counter"):
            self.timeout_counter=0

        if distance_between_midpoint <= 0.06:
            self.timeout_counter += 1
        else:
            self.timeout_counter = 0

        if self.timeout_counter == 10:
            return True 

        return False

    def initiate_begginer_workout(self,landmarks):
        """This will initiate the begginer workout tracking."""
        begginer_workouts=list(self.bigginer_workout.items())

        workout_type,workout_function=begginer_workouts[self.workout_index]

        step,executed_counts=workout_function(landmarks)
        elapsed_time = time.time() - self.start_time

        if executed_counts > 3 and self.set == 2 :
            self.next_workout= begginer_workouts[self.workout_index+1][0]

        if executed_counts > 5 : 
            self.start_time = time.time()
            self.counter=0
            self.step="Relaxed"
            self.set+=1
            self.next_workout=None 

        if (executed_counts > 5 and self.step ==3) or self.skip_workout(landmarks=landmarks) is True :
            self.workout_index = (self.workout_index +1) % len(begginer_workouts) 
            self.start_time = time.time()
            self.counter=0
            self.step="Relaxed"
             

        return {
           "Worlout Type": workout_type,
            "Repetitions Completed": executed_counts,
            "Time Elapsed (seconds)": round(elapsed_time, 2),
            "Current Step": step,
            "Next workout": self.next_workout,
            "set": self.set
        },workout_type , self.step , executed_counts , elapsed_time ,self.next_workout

        
        
          
