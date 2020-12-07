from cx_Freeze import setup, Executable
 
includefiles = [] # include any files here that you wish
includes = []
excludes = []
packages = []
 
exe = Executable(
 # what to build
   script = "user_interface.py", # the name of your main python script goes here 
   initScript = None,
   base = None, # if creating a GUI instead of a console app, type "Win32GUI"
   targetName = "perfume.exe", # this is the name of the executable file
   icon = None # if you want to use an icon file, specify the file name here
)
 
setup(
 # the actual setup & the definition of other misc. info
    name = "PerfumeFinder", # program name
    version = "0.1",
    description = 'Find your perfect perfume!',
    author = "Amber, Lonneke, Barbera",
    author_email = "b.c.de.mol@student.rug.nl",
    options = {"build_exe": {"excludes":excludes,"packages":packages,
      "include_files":includefiles}},
    executables = [exe]
)