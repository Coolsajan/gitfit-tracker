from src.utils.common_utils import calculate_angle,calculate_eq_distance,mind_point_finder ,convert_seconds,get_workout_plans
from src.utils.workout_reps_set_rest import upperbody_high_intensity_pull
from src.pose_estimator.warm_up import WarmUp
import mediapipe as mp 
import time,datetime

class UpperBodyPullWorkout:
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
        self.upper_body_pull_plan={"Inverted Rows":self.inverted_rows,
                                   "Pull-Ups":self.push_up,
                                   "Superman Hold":self.superman_hold,
                                   "Face Pull":self.face_pull_resistance_band}
        
        
    def get_landmarks(self,landmarks,pose_part):
        """ This method retruns the landmarks cordinates."""
        return [
            landmarks[self.mp_pose.PoseLandmark[pose_part].value].x,
                landmarks[self.mp_pose.PoseLandmark[pose_part].value].y
                ]
    
    def warm_up(self,landmarks):
        pass

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
    
    def push_up(self,landmarks):
        """ This method will detect and record the pushup."""
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
    
    def superman_hold(self,landmarks):
        """ This will detect and record your superman hold."""
        right_knee=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_KNEE")
        right_hip=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_HIP")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")

        #calculating angle
        right_hip_angle=calculate_angle(a=right_knee,b=right_hip,c=right_shoulder)
        right_shoulder_angle=calculate_angle(a=right_hip,b=right_shoulder,c=right_elbow)

        if right_shoulder_angle <=150 and right_hip_angle <= 170:
            self.step="SUPERMAN POSITON DETECTED"
            self.start_time=time.time()
        if self.step=="SUPERMAN POSITON DETECTED" and right_shoulder_angle >150 and right_hip_angle> 170:
            self.step="SUPERMAN POSTION FAIL"
            end_time=time.time() - self.start_time

            self.full_time += end_time

        return self.step , self.full_time
        

    def face_pull_resistance_band(self,landmarks):
        """ This method will detect and record face pull"""
        right_wrist=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_WRIST")
        right_elbow=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_ELBOW")
        right_shoulder=self.get_landmarks(landmarks=landmarks,pose_part="RIGHT_SHOULDER")

        right_elbow_angle=calculate_angle(a=right_wrist,b=right_elbow,c=right_shoulder)


        if right_elbow_angle >= 175 :
            self.step="RELEASED"
        if self.step=="RELEASED" and right_elbow_angle <=40:
            self.step="PULLED"
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
        self.rest_time=0
        workouts=list(self.upper_body_pull_plan.items())
        workout_type,workout_function =workouts[self.current_workout_index]
        self.updates=workout_type

        workout_data = upperbody_high_intensity_pull.get(workout_type, {})
        reps_required = workout_data.get("reps", 0)
        total_sets = workout_data.get("sets", 1)
        rest_time = workout_data.get("rest_time", 0)

        workout_plan=get_workout_plans(workouts,upperbody_high_intensity_pull,self.current_workout_index)
       

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


        end_time=round(end_time)                
        end_time=convert_seconds(end_time)
        self.rest_time=convert_seconds(round((self.rest_time)))

        return (self.updates , end_time, self.counter ,reps_required ,self.set , total_sets ,self.end_time ,rest_time,self.rest_time,self.total_reps_completed , workout_plan)
    

