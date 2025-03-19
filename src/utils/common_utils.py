import math
import numpy as np
import yaml


def calculate_angle(a,b,c):
    """Calculate angle between three points"""
    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    angle = abs(math.degrees(radians))
    return angle if angle <= 180 else 360 - angle

    
def calculate_eq_distance(a,b):
    a=np.array(a)
    b=np.array(b)

    distance = math.hypot(a[0] - b[0], a[1] - b[1])
    return distance

def mind_point_finder(a,b):
    a=list(a)
    b=list(b)
    result={}
    if len(a) == len(b):
        for i in range(0,len(a)):
            result[i]=(a[i]+b[i])/2
    return list(result.values()) 

def convert_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds}"



def get_workout_plan(workouts,workout_data):
    global workout_plan
    workout_plan=[]
    for i in range(len(workouts)):
        name,_=workouts[i]
        data=workout_data.get(name,{})
        reps= data.get("reps", 0)
        sets = data.get("set", 1)

        plan={"name":name,"set":sets,"reps":reps,"status":"upcoming"}

        workout_plan.append(plan)

    return str(workout_plan)
