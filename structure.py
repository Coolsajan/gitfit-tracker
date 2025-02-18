import os

from pathlib import Path

project_name="src"

list_of_files=[
    f"{project_name}/__init__.py",
    f"{project_name}/camera/__init__.py",
    f"{project_name}/camera/video_capture.py",
    f"{project_name}/camera/frame_processing.py",
    f"{project_name}/pose_estimator/__init__.py",
    f"{project_name}/pose_estimator/mediapipe_wrapper.py",
    f"{project_name}/pose_estimator/joint_angles.py",
    f"{project_name}/workout_logic/__init__.py",
    f"{project_name}/workout_logic/rep_counter.py",
    f"{project_name}/workout_logic/form_analyzer.py",
    f"{project_name}/database/__init__.py",
    f"{project_name}/database/db_connector.py",
    f"{project_name}/database/queries.py",
    f"{project_name}/visualization/__init__.py",
    f"{project_name}/visualization/realtime_overlay.py.py",
    f"{project_name}/visualization/dashboard.py",
    'data/workout_db',
    'data/workout_history',
    'config/excercise_config.yaml',
    'config/database_config.py',
    'test.py',
    'requirements.txt',
    'main.py'

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")