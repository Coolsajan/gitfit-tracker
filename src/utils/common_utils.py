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
