import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
include_files = ["engine", "engine/question", "data"]  # include any files here that you wish
includes = ["tkinter"]
excludes = []
packages = []

# if creating a GUI instead of a console app, type "Win32GUI"
# only possible if the system is win32
base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(
    # what to build
    script="main.py",           # the name of your main python script goes here
    init_script=None,
    base=base,
    target_name="perfume.exe",   # this is the name of the executable file
    icon=None                   # if you want to use an icon file, specify the file name here
)

setup(
    # the actual setup & the definition of other misc. info
    name="PerfumeFinder",  # program name
    version="0.1",
    description='Find your perfect perfume!',
    author="Amber, Lonneke, Barbera",
    author_email="l.c.pulles@student.rug.nl",
    options={"build_exe": {"excludes": excludes, "packages": packages,
                           "include_files": include_files}},
    executables=[exe]
)
