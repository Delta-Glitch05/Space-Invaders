import cx_Freeze
from cx_Freeze import *

exe = [cx_Freeze.Executable("Space Invaders.py", base="Win32GUI")]

cx_Freeze.setup(
    name="Space Invaders",
    author="D3LT4_GL1TCH",
    version="1.0",
    options={'build_exe': {'packages': ['pygame', 'math', 'random', 'sys', 'os'],
                           "include_files": ["Assets"]}},
    executables=exe
    )
