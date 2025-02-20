import os

from pathlib import Path

project_name="src"

list_of_files=[
    f"{project_name}/__init__.py",
    f"{project_name}/pose_estimator/__init__.py",
    f"{project_name}/pose_estimator/pose_detector.py",
    f"{project_name}/workout_logic/__init__.py",
    f"{project_name}/workout_logic/rep_counter.py",
    f"{project_name}/database/__init__.py",
    f"{project_name}/database/db_connector.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/common_utils.py",
    'config.py',
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