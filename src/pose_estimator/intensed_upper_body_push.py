from src.utils.common_utils import calculate_angle,calculate_eq_distance,mind_point_finder ,convert_seconds,get_workout_plan
from src.utils.workout_reps_set_rest import upperbody_high_intensity_push
from src.pose_estimator.warm_up import WarmUp
import mediapipe as mp 
import time,datetime

class UpperBodyPush:
    def __init__(self):
        self.mp_pose=mp.solutions.pose
        self.step="REST"
        self.counter=0
        self.current_workout_index=0
        self.start_time=time.time()
        self.updates=None
        self.rest_end_time=0.0
        self.set=1
        self.next_workout=None
        self.timeout_counter=0
        self.rest_start_time=None
        self.rest_time=0
        self.upper_body_push={
                              "Standard PushUp":self.Standard_Pushup,
                              "Diamond PushUp":self.Diamond_PushUp,
                              "Pike PushUp":self.Pike_pushUp,
                              "Dips":self.Dips}

    def get_landmarks(self,landmarks,pose_part):
        """ This method retruns the landmarks cordinates."""
        return [
            landmarks[self.mp_pose.PoseLandmark[pose_part].value].x,
                landmarks[self.mp_pose.PoseLandmark[pose_part].value].y
                ]
    
    def warmup(self,landmarks):
         pass
    def Standard_Pushup(self,landmarks):
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
    
    def Diamond_PushUp(self,landmarks):
        """This will detect and record dimond pushup.."""
        #collecting landmarks
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        left_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_SHOULDER")
        elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        right_wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        left_wrist=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_WRIST")
  
        #calculating angle and distance
        elbow_angle=calculate_angle(a=right_shoulder,b=elbow,c=right_wrist)
        dist_wrist=calculate_eq_distance(a=right_wrist,b=left_wrist)

        self.correct_form = dist_wrist < 0.01 

        if self.correct_form is True and elbow_angle >= 175:
            self.step = "UP"

        if self.correct_form is True and self.step == "UP" and elbow_angle <=60:
            self.step = "DOWN"
            self.counter += 1

        return  self.step ,  self.counter

    def Pike_pushUp(self,landmarks):
        """This method will detect and record the pike push up.."""
        #collecting landmarks
        shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")

        #calculating angle
        elbow_angle=calculate_angle(a=shoulder,b=elbow,c=wrist)

        if elbow_angle >= 175 :
            self.step = "DOWN"
        if self.step == "DOWN" and elbow_angle <= 90:
            self.step = "UP"
            self.counter += 1

        return self.step , self.counter 
    
    def Dips(self,landmarks):
        """This method will detect and record the Dips.. """
         #collecting landmarks
        shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")

        #calculating angle
        elbow_angle=calculate_angle(a=shoulder,b=elbow,c=wrist)

        if elbow_angle >= 175 :
            self.step  = "UP"
        if self.step == "UP" and elbow_angle <= 90:
            self.step = "DOWN"
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
        """Initate the upperbody body workout function.."""
        workouts=list(self.upper_body_push.items())
        workout_type,workout_function =workouts[self.current_workout_index]
        self.updates=workout_type

        workout_data = upperbody_high_intensity_push.get(workout_type, {})
        reps_required = workout_data.get("reps", 0)
        total_sets = workout_data.get("set", 1)
        rest_time = workout_data.get("rest_time", 0)

        workout_plan=get_workout_plan(workouts,upperbody_high_intensity_push)

        step,counter=workout_function(landmarks)
        end_time=time.time()-self.start_time

        

        if (counter == reps_required and self.step !="POST SET WORKOUT REST") or self._skip_workout(landmarks=landmarks) is True:
            self.step="REST"
            self.updates=self.step
            if self.rest_start_time is None:
                self.rest_start_time=time.time()           
            
        if self.step == "POST SET WORKOUT REST" :
            self.end_time=self.rest_start_time -time.time()

            if self.end_time >= (rest_time-5):
                self.step="WORKOUT BEGINS SHORTLY...."

            if self.end_time >= rest_time :
                print("rest complete moving to next set..")
                self.updates=workout_type
                self.set+=1
                self.counter=0
                self.step="WORKOUT BEGINS"
      
        if counter >= (reps_required *2/3) and self.set==total_sets:
            self.next_workout,_=workouts[(self.current_workout_index + 1) % len(workouts)]    

        if ((counter == reps_required) and (self.set == total_sets) and (self.step!="POST WORKOUT REST")) or ((self.set == total_sets) and(self._skip_workout(landmarks=landmarks)) and (self.step!="POST WORKOUT REST")):
            self.step="REST"
            self.updates=self.step
            self.start_time=time.time()

            if self.step=='POST WORKOUT REST':
                self.end_time=time.time()-self.rest_start_time
                print("rest time started..")

                if self.end_time >= rest_time:
                    self.updates=workout_type
                    self.start_time=time.time()
                    self.set=1
                    self.counter=0
                    self.current_workout_index+=1


        #self.rest_end_time=round(self.rest_end_time)
        end_time=round(end_time)                
        end_time=convert_seconds(end_time)

        return (self.updates, self.counter , reps_required ,self.set,total_sets,end_time,self.rest_end_time ,self.step ,workout_plan)
              
