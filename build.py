import sys
import os
import shutil
from cx_Freeze import setup, Executable

python_dll_path = os.path.join(os.path.dirname(sys.executable), "python310.dll")

setup(
    name="RatMaze",
    version="1.0",
    description="A maze for rats",
    options={"build_exe": {"include_files": [python_dll_path]}},
    executables=[Executable("main.py")]
)

dir = os.listdir("build")[0]
shutil.copyfile("config.ini", f"build/{dir}/config.ini")
shutil.copytree("resources", f"build/{dir}/resources")
