from src.utils.common_utils import calculate_angle,calculate_eq_distance,mind_point_finder,convert_seconds,get_workout_plans 
from src.utils.workout_reps_set_rest import core_body_plan
from src.pose_estimator.warm_up import WarmUp
import mediapipe as mp 
import time,datetime

class CoreWorkout:
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
        self.core_workout={"Plank Hold":self.plank,
                           "Side Plank(RIGHT)":self.right_side_plank,
                           "Side Plank(LEFT)":self.left_side_plank,
                           "Russian Twists":self.russian_twist,
                           "Hollow Body Hold":self.hollow_body_hold,
                           "Mountain Climber":self.mountian_climber}
        
        
    def get_landmarks(self,landmarks,pose_part):
        """ This method retruns the landmarks cordinates."""
        return [
            landmarks[self.mp_pose.PoseLandmark[pose_part].value.x],
                landmarks[self.mp_pose.PoseLandmark[pose_part].value.y]
                ]
    
    def warm_up(self,landmarks):
        pass

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
        
        return self.workout_time , self.step
    
    def right_side_plank(self,landmarks):
        """This will detect and record the side plank. """
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")

        #calculating angle
        right_shoulder_angle=calculate_angle(a=right_hip,b=right_shoulder,c=right_elbow)
        right_hip_angle=calculate_angle(a=right_knee,b=right_hip,c=right_shoulder)



        if 175 < right_hip_angle < 185 and 45 < right_shoulder_angle < 50:
            self.step="RIGHT PLANK HOLD STARTED"
            self.start_time=time.time()
        if self.step == "RIGHT PLANK HOLD STARTED" and 45 > right_shoulder_angle > 50:
            end_time=time.time() - self.start_time
        
            self.workout_time += end_time

        return self.workout_time  , self.step
    
    def left_side_plank(self,landmarks):
        """This will detect and record the side plank. """
        left_elbow=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ELBOW")
        left_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_SHOULDER")
        left_hip=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_HIP")
        left_knee=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_KNEE")

        #calculating angle
        left_shoulder_angle=calculate_angle(a=left_hip,b=left_shoulder,c=left_elbow)
        left_hip_angle=calculate_angle(a=left_knee,b=left_hip,c=left_shoulder)



        if 175 < left_hip_angle < 185 and 45 < left_shoulder_angle < 50:
            self.step="LEFT PLANK HOLD STARTED"
            self.start_time=time.time()
        if self.step == "LEFT PLANK HOLD STARTED" and 45 > left_shoulder_angle > 50:
            end_time=time.time() - self.start_time
        
            self.workout_time += end_time
        return self.workout_time , self.step
    

    def russian_twist(self, landmarks):
        """This method detects and records the Russian Twist movement."""

        left_shoulder = self.get_landmarks(landmarks=landmarks, pose_part="LEFT_SHOULDER")
        right_shoulder = self.get_landmarks(landmarks=landmarks, pose_part="RIGHT_SHOULDER")
        left_hip = self.get_landmarks(landmarks=landmarks, pose_part="LEFT_HIP")
        right_hip = self.get_landmarks(landmarks=landmarks, pose_part="RIGHT_HIP")

        # Calculate torso rotation angle
        torso_angle = calculate_angle(a=left_shoulder, b=right_shoulder, c=right_hip)

        # Detect left and right twists
        if torso_angle > 45:  # Rotating to the right
            self.step = "TWIST RIGHT"
        elif torso_angle < -45:  # Rotating to the left
            self.step = "TWIST LEFT"
        elif -10 < torso_angle < 10:  # Returning to center
            if self.step in ["TWIST RIGHT", "TWIST LEFT"]:
                self.workout_index += 1  # Count one rep when back to center
                self.step = "CENTER"

        return self.workout_index, self.step
    

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
        if self.step == "HOLLOW BODY HOLD STARTED" and (right_shoulder_angle >  135 or right_hip_angle > 135):
            self.step="HOLLOW BODY HOLD STOPED"
            end_time=time.time() - self.start_time

            self.workout_time += end_time

        return self.workout_time , self.step
    
    def mountian_climber(self,landmarks):
        """This will detect and record the mountain climber."""
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHTSHOULDER")
        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        right_ankle=self.get_landmarks(landmarks=landmarks,pose_part="RIGHTANKLE")
        left_knee=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_KNEE")
        left_hip=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_HIP")
        left_ankle=self.get_landmarks(landmarks=landmarks,pose_part="LEFT_ANKLE")

        #calculating angle
        right_shoulder_angle=calculate_angle(a=right_elbow,b=right_shoulder,c=right_hip)
        right_knee_angle=calculate_angle(a=right_hip,b=right_knee,c=right_ankle)
        left_knee_angle=calculate_angle(a=left_hip,b=left_knee,c=left_ankle)
        
        if 85 < right_shoulder_angle < 95 and right_knee_angle >=140 and left_knee_angle >= 140:
            self.step="MOUTAIN CLIMBER STARTED"
            self.start_time=time.time()
        if self.step == "MOUTAIN CLIMBER STARTED" and right_knee_angle <= 80 and left_knee_angle >= 140:
            self.step="RIGHT LEG AHEAD"
        if self.step== "RIGHT LEG AHEAD" and right_knee_angle >=140 and left_knee_angle >= 140 :
            self.step="NORMAL"
        if self.step=="NORMAL" and right_knee_angle >= 140 and left_knee_angle <= 0:
            self.step="LEFT LEG AHEAD"
            end_time=time.time() - self.start_time

            self.workout_time+= end_time
        return self.workout_time , self.step
    
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
        """Initate the core workout function.."""
        self.rest_time=0
        workouts=list(self.core_workout.items())
        workout_type,workout_function =workouts[self.current_workout_index]
        self.updates=workout_type

        workout_data = core_body_plan.get(workout_type, {})
        reps_required = workout_data.get("reps", 0)
        total_sets = workout_data.get("sets", 1)
        rest_time = workout_data.get("rest_time", 0)

        workout_plan=get_workout_plans(workouts,core_body_plan,self.current_workout_index)
       

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


            

