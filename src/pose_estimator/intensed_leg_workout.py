from src.utils.common_utils import calculate_angle,calculate_eq_distance,mind_point_finder 
from src.utils.workout_reps_set_rest import lowerbody_high_intensity
from src.pose_estimator.warm_up import WarmUp
import mediapipe as mp 
import time,datetime

class LegWorkout:
    def __init__(self):
        self.mp_pose=mp.solutions.pose
        self.step="REST"
        self.counter=0
        self.current_workout_index=0
        self.start_time=time.time()
        self.set=1
        self.next_workout=None
        self.timeout_counter=0
        self.rest_start_time=None
        self.rest_time=0
        self.lower_body_workout={"Standard Squarts":self.squart,
                                 "Forward Lunges":self.forward_lunges,
                                 "Single_leg Romanian Deadlift":self.single_leg_romanian_deadlift,
                                 "Bulgerain Split Squarts(RIGHT)":self.right_bulgerain_split_squart,
                                 "Bulgerain Split Squarts(LEFT)":self.left_bulgerain_split_squart}
        
        
    def get_landmarks(self,landmarks,pose_part):
        """ This method retruns the landmarks cordinates."""
        return [
            landmarks[self.mp_pose.PoseLandmark[pose_part].value.x],
                landmarks[self.mp_pose.PoseLandmark[pose_part].value.y]
                ]
    
    def warm_up(self,landmarks):
        pass

    def squart(self,landmarks):
        #COLLECTING LANDMARKS
        shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        ankle=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ANKLE")
        #CALCULATING ANGLE
        hip_angle=calculate_angle(a=shoulder,b=hip,c=knee)
        knee_angle=calculate_angle(a=hip,b=knee,c=ankle)

        if hip_angle < 140 and knee_angle < 120:
            self.step="DOWN"
        if hip_angle > 175 and knee_angle > 175 and self.step=="DOWN":
            self.step="UP"
            self.counter+=1

        return self.step , self.counter
    
    def forward_lunges(self,landmarks):
        """ This method withh detect and record the reverse lunges."""
        right_ankle=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ANKLE")
        left_ankle=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ANKLE")

        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        left_knee=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_KNEE")

        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        left_hip=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_HIP")

        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        left_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_SHOULDER")

        #calculating angle
        right_knee_angle=calculate_angle(a=right_ankle,b=right_knee,c=right_hip)
        left_knee_angle=calculate_angle(a=left_ankle,b=left_knee,c=left_hip)
        right_hip_angle=calculate_angle(a=right_shoulder,b=right_hip,c=right_knee)
        left_hip_angle=calculate_angle(a=left_shoulder,b=left_hip,c=left_knee)


        if right_knee_angle <= 90 and left_knee_angle <= 90 and right_hip_angle <=110:
            self.step="RIGHT LEG DOWN"
        if self.step=="RIGHT LEG DOWN" and right_knee_angle >= 175 and left_knee_angle >= 175 and right_hip_angle >=175:
            self.step="UP"
        if self.step=="UP" and right_knee_angle <= 90 and left_knee_angle <= 90 and left_hip_angle <=110:
            self.step="LEFT LEG DOWN"
        if self.step=="LEFT LEG DOWN" and right_knee_angle >= 175 and left_knee_angle >= 175 and right_hip_angle >=175:
            self.step="UP"
            self.counter += 1
        
        return self.step , self.counter 
    
    def single_leg_romanian_deadlift(self,landmarks):
        """This method will detect and  record single leg deadlift.."""
        #collecting landmarks
        right_ankle=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ANKLE")
        left_ankle=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ANKLE")

        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        left_knee=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_KNEE")

        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        left_hip=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_HIP")

        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        left_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_SHOULDER")

        right_knee_angle=calculate_angle(a=right_ankle,b=right_knee,c=right_hip)
        left_knee_angle=calculate_angle(a=left_ankle,b=left_knee,c=left_hip)

        right_hip_angle=calculate_angle(a=right_shoulder,b=right_hip,c=right_knee)
        left_hip_angle=calculate_angle(a=left_shoulder,b=left_hip,c=left_knee)

        if right_hip_angle >=175 and right_knee_angle >= 175 and left_hip_angle >= 175 and left_knee_angle >= 175:
            self.step="READY"
        if self.step == "READY" and right_hip_angle >=175 and right_knee_angle >= 175 and left_hip_angle <= 100 and left_knee_angle <= 150 :
            self.step = "RIGHT LEG UP"
        if  self.step =="RIGHT LEG UP" and right_hip_angle >=175 and right_knee_angle >= 175 and left_hip_angle >= 175 and left_knee_angle >= 175:
            self.step="NORMAL"
        if self.step == "READY" and right_hip_angle <=100 and right_knee_angle <= 150 and left_hip_angle >= 175 and left_knee_angle >= 175:
            self.step ="LEFT LEG UP"
            self.counter += 1

        return self.step , self.counter 
    
    def right_bulgerain_split_squart(self,landmarks):
        """This method will detect and record """
        #collecting landmarks
        right_ankle=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ANKLE")
        left_ankle=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ANKLE")

        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        left_knee=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_KNEE")

        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        left_hip=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_HIP")

        #calculating angle
        right_knee_angle=calculate_angle(a=right_ankle,b=right_knee,c=right_hip)
        left_knee_angle=calculate_angle(a=left_ankle,b=left_knee,c=left_hip)

        if right_knee_angle >= 175 and left_knee_angle >= 85 :
            self.step="UP"
        if self.step == "UP" and right_knee_angle <=90 and left_knee_angle <= 40:
            self.step="DOWN"
            self.counter += 1
        
        return self.step , self.counter
    

    def left_bulgerain_split_squart(self,landmarks):
        """This method will detect and record """
        #collecting landmarks
        right_ankle=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ANKLE")
        left_ankle=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ANKLE")

        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        left_knee=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_KNEE")

        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        left_hip=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_HIP")

        #calculating angle
        right_knee_angle=calculate_angle(a=right_ankle,b=right_knee,c=right_hip)
        left_knee_angle=calculate_angle(a=left_ankle,b=left_knee,c=left_hip)

        if right_knee_angle >= 85 and left_knee_angle >= 175 :
            self.step="UP"
        if self.step == "UP" and right_knee_angle <=40 and left_knee_angle <= 90:
            self.step="DOWN"
            self.counter += 1
        
        return self.step , self.counter
    
    def _skip_workout(self,landmarks):
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
    
    def initiate_workout(self,landmarks):
        """Initate the full body workout function.."""
        workouts=list(self.lower_body_workout.items())
        workout_type,workout_function =workouts[self.current_workout_index]

        workout_data = lowerbody_high_intensity.get(workout_type, {})
        reps_required = workout_data.get("reps", 0)
        total_sets = workout_data.get("set", 1)
        rest_time = workout_data.get("rest_time", 0)

        step,counter=workout_function(landmarks)
        end_time=time.time()-self.start_time

        

        if (counter == reps_required and self.step !="POST SET WORKOUT REST") or self._skip_workout(landmarks=landmarks) is True:
            self.step="POST SET WORKOUT REST"
            if self.rest_start_time is None:
                self.rest_start_time=time.time()           
            
        if self.step == "POST SET WORKOUT REST" :
            self.end_time=time.time()-self.rest_start_time

            if self.end_time >= (rest_time-5):
                self.step="WORKOUT BEGINS SHORTLY...."

            if self.end_time >= rest_time :
                print("rest complete moving to next set..")
                self.set+=1
                self.counter=0
                self.step="WORKOUT BEGINS"
      
        if counter >= (reps_required *2/3) and self.set==total_sets:
            self.next_workout,_=workouts[(self.current_workout_index + 1) % len(workouts)]    

        if ((counter == reps_required) and (self.set == total_sets) and (self.step!="POST WORKOUT REST")) or ((self.set == total_sets) and(self._skip_workout(landmarks=landmarks)) and (self.step!="POST WORKOUT REST")):
            self.step="POST WORKOUT REST"
            self.rest_start_time=time.time()

            if self.step=='POST WORKOUT REST':
                self.end_time=time.time()-self.rest_start_time
                print("rest time started..")

                if self.end_time >= rest_time:
                    self.start_time=time.time()
                    self.set=1
                    self.counter=0
                    self.current_workout_index+=1

        

        return {
            "Workout Type": workout_type,
            "Repetitions Completed": self.counter,
            "Time Elapsed (seconds)": end_time,
            "Current Step": step,
            "Next Workout": self.next_workout,
            "Set": self.set
        }, workout_type, self.step, self.counter, end_time, self.next_workout,self.set