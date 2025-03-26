from src.pose_estimator.full_body_workout import FullBodyWorkout
from src.pose_estimator.core_workout import CoreWorkout
from src.pose_estimator.intensed_leg_workout import LegWorkout
from src.pose_estimator.intensed_upper_body_pull_workout import UpperBodyPullWorkout
from src.pose_estimator.intensed_upper_body_push import UpperBodyPush

workout_schedule={
    "Sunday": UpperBodyPush(),
    "Monday" : LegWorkout(),
    "Tuesday" : CoreWorkout(),
    "Wednesday" : UpperBodyPullWorkout(),
    "Friday" : FullBodyWorkout()
}


print(workout_schedule.get("Sunday"))