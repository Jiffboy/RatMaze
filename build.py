import sys
import os
from cx_Freeze import setup, Executable

python_dll_path = os.path.join(os.path.dirname(sys.executable), "python310.dll")

setup(
    name="RatMaze",
    version="1.0",
    description="A maze for rats",
    options={"build_exe": {
        "include_files": [python_dll_path, "config.ini", "resources"],
        "build_exe": "build/RatMaze"
    }},
    executables=[Executable("main.py", target_name="RatMaze.exe")]
)
