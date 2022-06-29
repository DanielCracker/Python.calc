from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
includefiles = ['config.txt', 'forest-dark.tcl', 'forest-dark/', 'ik.ico']
includes = []
build_options = {'includes': includes, 'packages': [], 'excludes': [], 'include_files': includefiles}

import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('calc.py', base=base, target_name='calces', icon="ik.ico", shortcutName="SarmaCalc",
               shortcutDir="DesktopFolder", )
]

setup(name='SarmaCalc',
      version='1.0',
      author="DanielCrack",
      description='Sarma Culculating',
      options={'build_exe': build_options},
      executables=executables)
