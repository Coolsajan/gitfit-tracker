from src.utils.common_utils import fullbody_moderate_intensity

workout_data = fullbody_moderate_intensity.get("Standard Pushup", {})
reps_required = workout_data.get("reps", 0)
total_sets = workout_data.get("set", 1)
rest_time = workout_data.get("rest_time", 0)


print(workout_data,reps_required,total_sets,rest_time)


session_data=fullbody_moderate_intensity.get("Standerd Pushup",{})
reps_required=session_data.get("reps",0)
total_sets=session_data.get("set",1)
rest_time=session_data.get("rest_time",0)
print(f"reps:{reps_required},total_set:{total_sets},rest:{rest_time}")