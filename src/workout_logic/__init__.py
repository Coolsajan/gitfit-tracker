from datetime import datetime
from src.pose_estimator.intensed_upper_body_push import UpperBodyPush
from src.pose_estimator.intensed_leg_workout import LegWorkout
from src.pose_estimator.intensed_upper_body_pull_workout import UpperBodyPullWorkout
from src.pose_estimator.core_workout import CoreWorkout
from src.pose_estimator.full_body_workout import FullBodyWorkout


workout_schedule={"Sunday":UpperBodyPush(),
                  "Monday":LegWorkout(),
                  "Tuesday":CoreWorkout(),
                  "Wednesday":UpperBodyPullWorkout(),
                  "Friday":FullBodyWorkout()}



def date_wise_plan(current_date,workout_schedule=workout_schedule):
    """This method will check the current date and initite the  workout plan.."""
    current_day=current_date.strftime("%A")

    workout_function=workout_schedule.get(current_day)

    return workout_function



        
        