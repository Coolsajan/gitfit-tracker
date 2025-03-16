from src.utils.common_utils import calculate_angle,calculate_eq_distance
from src.constant import *
import mediapipe as mp
import time

class WarmUp:
    def __init__(self):
        self.mp_pose=mp.solutions.pose
        self.warm_up={"left_head_roll":self.left_head_roll,
                      "right_head_roll":self.right_head_roll,
                      "jumping_jack":self.jumping_jack,
                      "double_arm_stretch":self.double_arm_stretch,
                      "right_leg_forward_swing":self.right_leg_forward_swing,
                      "left_leg_forward_swing":self.left_leg_forward_swing,
                      "right_leg_side_swing":self.right_leg_side_swing,
                      "left_leg_side_swing":self.left_leg_side_swing}
        self.step="Relaxed"
        self.counter=0
        self.warmup_drill_index=0
        self.start_time=time.time()
        self.next_warmup=""

    def get_landmarks(self,landmarks,pose_parts):
        """Get normalized coordinates of specific body part"""
        return [
            landmarks[self.mp_pose.PoseLandmark[pose_parts].value].x,
            landmarks[self.mp_pose.PoseLandmark[pose_parts].value].y
        ]



     #-----------------------------------------------------------------------------------------------#
    def left_head_roll(self, landmarks):        
        """Detect head roll and record""" 
        # collecting the landmarks
        right_ear = self.get_landmarks(landmarks=landmarks, pose_parts= "RIGHT_EAR")
        left_ear = self.get_landmarks(landmarks=landmarks, pose_parts="LEFT_EAR")
        right_shoulder = self.get_landmarks(landmarks=landmarks, pose_parts="RIGHT_SHOULDER")
        left_shoulder = self.get_landmarks(landmarks=landmarks,pose_parts= "LEFT_SHOULDER")
        # calculating distances
        shoulder_width = calculate_eq_distance(a=left_shoulder, b=right_shoulder)
        right_ear_shoulder = (calculate_eq_distance(a=right_ear, b=right_shoulder)) / shoulder_width
        left_ear_shoulder = (calculate_eq_distance(a=left_ear, b=left_shoulder)) / shoulder_width    

        if right_ear_shoulder > SIDE_HIGH_THRESHOLD_HEADROLL and left_ear_shoulder < SIDE_LOW_THRESHOLD_HEADROLL:
            self.step="LEFT"
        elif right_ear_shoulder < HEAD_FORWARD_THRESHOLD_HEADROLL and left_ear_shoulder < HEAD_FORWARD_THRESHOLD_HEADROLL and self.step =="LEFT":
            self.step="FRONT"
        elif right_ear_shoulder < SIDE_LOW_THRESHOLD_HEADROLL and left_ear_shoulder > SIDE_HIGH_THRESHOLD_HEADROLL and self.step =="FRONT":
            self.step="RIGHT"
        elif right_ear_shoulder > HEAD_BACK_THRESHOLD_HEADROLL and left_ear_shoulder > HEAD_BACK_THRESHOLD_HEADROLL and self.step =="RIGHT":
            self.step="BACK"
            self.counter += 1
            self.total_time=time.time()-self.start_time

        return  self.counter,self.step
    
     #-----------------------------------------------------------------------------------------------#

    def right_head_roll(self, landmarks,):        
        """Detect head left roll and record"""
        # collecting the landmarks point.
        right_ear = self.get_landmarks(landmarks=landmarks,pose_parts= "RIGHT_EAR")
        left_ear = self.get_landmarks(landmarks=landmarks, pose_parts="LEFT_EAR")
        right_shoulder = self.get_landmarks(landmarks=landmarks,pose_parts= "RIGHT_SHOULDER")
        left_shoulder = self.get_landmarks(landmarks=landmarks,pose_parts= "LEFT_SHOULDER")
        # calculating distance
        shoulder_width = calculate_eq_distance(a=left_shoulder, b=right_shoulder)
        right_ear_shoulder = (calculate_eq_distance(a=right_ear, b=right_shoulder)) / shoulder_width
        left_ear_shoulder = (calculate_eq_distance(a=left_ear, b=left_shoulder)) / shoulder_width        

        if right_ear_shoulder < SIDE_LOW_THRESHOLD_HEADROLL and left_ear_shoulder > SIDE_HIGH_THRESHOLD_HEADROLL :
            self.step="RIGHT"
        elif right_ear_shoulder < HEAD_FORWARD_THRESHOLD_HEADROLL and left_ear_shoulder < HEAD_FORWARD_THRESHOLD_HEADROLL and self.step =="RIGHT":
            self.step="FRONT"
        elif right_ear_shoulder > SIDE_HIGH_THRESHOLD_HEADROLL and left_ear_shoulder < SIDE_LOW_THRESHOLD_HEADROLL and self.step=="FRONT":
            self.step="LEFT"
        elif right_ear_shoulder > HEAD_BACK_THRESHOLD_HEADROLL and left_ear_shoulder > HEAD_BACK_THRESHOLD_HEADROLL and self.step =="LEFT":
            self.step="Back"
            self.counter += 1

        return  self.counter,self.step

     #-----------------------------------------------------------------------------------------------#
       
    def jumping_jack(self,landmarks):
        """Record Jumping Jacks"""
        #collecting the landmarks points..
        elbow=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_ELBOW")
        shoulder=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_SHOULDER")
        hip=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_HIP")
        knee=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_KNEE")

        #calculating angle
        shoulder_angle=calculate_angle(a=elbow,b=shoulder,c=hip)
        lower_angle=calculate_angle(a=shoulder,b=hip,c=knee)

        if lower_angle < HIGH_THRESHOLD_JUMPING_JACK and shoulder_angle > LOW_THRESHOLD_JUMPING_JACK :
                self.step="UP"                          
        if  shoulder_angle < LOW_THRESHOLD_JUMPING_JACK and lower_angle > HIGH_THRESHOLD_JUMPING_JACK  and self.step =="UP":
                self.step="DOWN"
                self.counter +=1

        return self.counter,self.step
     #-----------------------------------------------------------------------------------------------#

    def double_arm_stretch(self,landmarks):
        """This is the strteching for chest"""
        #getting the landmarks of wrist
        right_wrist=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_WRIST")
        left_wrist=self.get_landmarks(landmarks=landmarks,pose_parts="LEFT_WRIST")

        #getting the landmark of shoulder
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_SHOULDER")
        left_shoulder=self.get_landmarks(landmarks=landmarks,pose_parts="LEFT_SHOULDER")

        #calculating the distance between the bodypart
        dist_between_shoulder=calculate_eq_distance(a=right_shoulder,b=left_shoulder)
        dist_between_wrist=calculate_eq_distance(a=right_wrist,b=left_wrist)

        if dist_between_wrist < dist_between_shoulder/2:
             self.step="Hands Closed"
        if self.step=="Hands Closed" and dist_between_wrist>dist_between_shoulder*3:
             self.step="Hands Open"
             self.counter+=1

        return self.counter,self.step
     #-----------------------------------------------------------------------------------------------#
  
    def right_leg_forward_swing(self,landmarks):
         """ Recording right leg swing...."""
         #collecting the landmarks points..
         right_shoulder=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_SHOULDER")
         right_hip=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_HIP")
         right_knee=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_KNEE")

         #calcualting the angle
         hip_angle=calculate_angle(a=right_knee,b=right_hip,c=right_shoulder)

         if hip_angle<LOW_THRESHOLD_LEG_SWING:
              self.step="LEG RAISED"
         if hip_angle>HIGH_THRESHOLD_LEG_SWING and self.step=="LEG RAISED":
              self.step="LEG LOWERED"
              self.counter+=1

         return self.counter,self.step
        #-----------------------------------------------------------------------------------------------#
         
    def left_leg_forward_swing(self,landmarks):
         """ Recording right leg swing...."""
         #collecting the landmarks points..
         left_shoulder=self.get_landmarks(landmarks=landmarks,pose_parts="LEFT_SHOULDER")
         left_hip=self.get_landmarks(landmarks=landmarks,pose_parts="LEFT_HIP")
         left_knee=self.get_landmarks(landmarks=landmarks,pose_parts="LEFT_KNEE")

         #calculating the angle...
         hip_angle=calculate_angle(a=left_knee,b=left_hip,c=left_shoulder)

         if hip_angle<LOW_THRESHOLD_LEG_SWING:
              self.step="LEG RAISED"
         if hip_angle>HIGH_THRESHOLD_LEG_SWING and self.step=="LEG RAISED":
              self.step="LEG LOWERED"
              self.counter+=1

         return self.counter,self.step
          #-----------------------------------------------------------------------------------------------#
   
    def right_leg_side_swing(self,landmarks):
         """ Recording right leg swing...."""   
         #collecting the landmarks points..
         right_shoulder=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_SHOULDER")
         right_hip=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_HIP")
         right_knee=self.get_landmarks(landmarks=landmarks,pose_parts="RIGHT_KNEE")

         hip_angle=calculate_angle(a=right_knee,b=right_hip,c=right_shoulder)

         if hip_angle<SIDE_LOW_THRESHOLD_HEADROLL:
              self.step="LEG RAISED"
         if hip_angle>SIDE_HIGH_THRESHOLD_HEADROLL and self.step=="LEG RAISED":
              self.step="LEG LOWERED"
              self.counter+=1

         return self.counter,self.step
        #-----------------------------------------------------------------------------------------------#
        
    def left_leg_side_swing(self,landmarks):
         """ Recording right leg swing...."""
         #collecting the landmarks points..       
         left_shoulder=self.get_landmarks(landmarks=landmarks,pose_parts="LEFT_SHOULDER")
         left_hip=self.get_landmarks(landmarks=landmarks,pose_parts="LEFT_HIP")
         left_knee=self.get_landmarks(landmarks=landmarks,pose_parts="LEFT_KNEE")
        
         #calculating angle
         hip_angle=calculate_angle(a=left_knee,b=left_hip,c=left_shoulder)

         if hip_angle<LOW_THRESHOLD_LEG_SIDE_SWING:
              self.step="LEG RAISED"
         if hip_angle>HIGH_THRESHOLD_LEG_SIDE_SWING and self.step=="LEG RAISED":
              self.step="LEG LOWERED"
              self.counter+=1

         return self.counter,self.step


        
    def initiate_warmup(self, landmarks):
        """Starts warmup, tracks time and reps, and switches activity based on conditions"""
        #collecting all warmup drills into a list
        warmup_drills = list(self.warm_up.items())
        warmup_type, warmup_function = warmup_drills[self.warmup_drill_index]

        elapsed_time = time.time() - self.start_time
        execution_count, step = warmup_function(landmarks)
        if execution_count >= 2 :
            self.next_warmup = warmup_drills[self.warmup_drill_index+1][0]

        # this is the logic to switch the warmup 
        if execution_count >= 3 and elapsed_time >= 10:
            self.warmup_drill_index = (self.warmup_drill_index + 1) % len(warmup_drills)  
            self.start_time = time.time()
            self.counter=0
            self.step="Relaxed"
            self.next_warmup=None 
            print("WARM UP COMPLETED....") 
 
        return {
           "Warmup Type": warmup_type,
            "Repetitions Completed": execution_count,
            "Time Elapsed (seconds)": round(elapsed_time, 2),
            "Current Step": step,
            "Next warmup": self.next_warmup
        },warmup_type , step , execution_count , elapsed_time ,self.next_warmup