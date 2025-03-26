from src.utils.common_utils import calculate_angle,calculate_eq_distance,mind_point_finder ,convert_seconds,get_workout_plans
from src.utils.workout_reps_set_rest import fullbody_moderate_intensity
from src.pose_estimator.warm_up import WarmUp
import mediapipe as mp 
import time

class FullBodyWorkout:
    def __init__(self):
        self.mp_pose=mp.solutions.pose
        self.step="REST"
        self.counter=0
        self.current_workout_index=0
        self.start_time=time.time()
        self.updates=None
        self.end_time=0.0
        self.set=1
        self.total_set=0
        self.next_workout=None
        self.timeout_counter=0
        self.rest_start_time=None
        self.rest_time=0
        self.total_reps_completed=0       
        self.full_body_workout={"Standard PushUp":self.Standard_Pushup,
                                "Standard Squart":self.squart,
                                "Hollow Body Hold":self.hollow_body_hold,
                                "Inverted Rows":self.inverted_rows,
                                "Plank Hold":self.plank,
                                "Forward Lunges":self.forward_lunges,
                                }
        
        
    def get_landmarks(self,landmarks,pose_part):
        """ This method retruns the landmarks cordinates."""
        return [
            landmarks[self.mp_pose.PoseLandmark[pose_part].value].x,
                landmarks[self.mp_pose.PoseLandmark[pose_part].value].y
                ]
           
    
    """def warm_up(self,landmarks):
                pass"""

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
        if elbow_angle < 60 and self.step == "UP":
            self.step="DOWN"
            self.counter+=1

        return self.step , self.counter
    

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
    
    
    def hollow_body_hold(self,landmarks):
        """This will detect and record the hollow body hold . """
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")

        #calculating angle
        right_shoulder_angle=calculate_angle(a=right_hip,b=right_shoulder,c=right_elbow)
        right_hip_angle=calculate_angle(a=right_knee,b=right_hip,c=right_shoulder)

        if right_shoulder_angle <=  135 and right_hip_angle <= 135:
            self.step="HOLLOW BODY HOLD STARTED"
            self.start_time=time.time()
        if self.step == "HOLLOW BODY HOLD STARTED" and ((right_shoulder_angle >  135) or (right_hip_angle > 135)):
            self.step="HOLLOW BODY HOLD STOPED"
            end_time=time.time() - self.start_time

            self.workout_time += end_time

        return  self.step , self.workout_time

    def inverted_rows(self,landmarks):
        """This method will detect and record the inverted row. """
        right_wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        left_wrist=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_WRIST")
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        left_elbow=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ELBOW")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        left_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_SHOULDER")

        #calculating angle

        right_elbow_angle=calculate_angle(a=right_shoulder,b=right_elbow,c=right_wrist)
        left_elbow_angle=calculate_angle(a=left_shoulder,b=left_elbow,c=left_wrist)

        if right_elbow_angle >= 175 and left_elbow_angle >= 175:
            self.step = "HANG"
        if self.step == "HANG" and right_elbow_angle <= 45 and left_elbow_angle <= 45:
            self.step = "PULLED UP"
            self.counter += 1
        
        return self.step , self.counter

    def plank(self,landmarks):
        """This will detect and record the plank hold."""
        right_wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")

        #calculating angle
        right_hip_angle=calculate_angle(a=right_knee,b=right_hip,c=right_shoulder)
        right_elbow_angle=calculate_angle(a=right_wrist,b=right_elbow,c=right_shoulder)

        if 85 < right_elbow_angle < 95 and 175 < right_hip_angle < 185 :
            self.step="HOLD START"
            self.start_time=time.time()
        
        if self.step == "HOLD START" and right_elbow_angle < 85 :
            end_time=time.time() - self.start_time

            self.workout_time += end_time
        
        return   self.step ,self.workout_time

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
    

    def initiate_workout(self, landmarks):
        """ This will initialize the workout , record and retrun the reps,set,time..."""
        self.rest_time=0
        workouts=list(self.full_body_workout.items())
        workout_type,workout_function =workouts[self.current_workout_index]
        self.updates=workout_type

        workout_data = fullbody_moderate_intensity.get(workout_type, {})
        reps_required = workout_data.get("reps", 0)
        total_sets = workout_data.get("sets", 1)
        rest_time = workout_data.get("rest_time", 0)

        workout_plan=get_workout_plans(workouts,fullbody_moderate_intensity,self.current_workout_index)
       

        step,counter=workout_function(landmarks)
        self.total_reps_completed = counter
        end_time=time.time()-self.start_time

        

        if (counter == reps_required and self.step !="POST WORKOUT REST") :
            self.step="REST"
            self.updates=self.step
            if self.rest_start_time is None:
                self.rest_start_time=time.time()           
            
        if self.step == "REST" :
            self.end_time=time.time() -  self.rest_start_time
            self.rest_time = self.end_time

            if self.end_time >= rest_time :
                self.rest_start_time = None
                print("rest complete moving to next set..")
                self.updates=workout_type
                self.set+=1
                self.counter=0
                self.step="WORKOUT BEGINS"
                
          

        if ((counter == reps_required) and (self.set == total_sets) and (self.step!="POST WORKOUT REST")) :
            self.step="REST"
            self.updates=self.step
            self.rest_start_time=time.time()

            if self.step=='REST':
                self.end_time=time.time()-self.rest_start_time
                self.rest_time += self.end_time

                if self.end_time >= rest_time:
                    self.total_reps_completed=0
                    self.rest_start_time=None
                    self.updates=workout_type
                    self.set=1
                    self.counter=0
                    self.current_workout_index+=1


        #self.rest_end_time=round(self.rest_end_time)
        end_time=round(end_time)                
        end_time=convert_seconds(end_time)
        self.rest_time=convert_seconds(round((self.rest_time)))

        return (self.updates , end_time, self.counter ,reps_required ,self.set , total_sets ,self.end_time ,rest_time,self.rest_time,self.total_reps_completed , workout_plan)