#!/usr/bin/env python

"""Fully compile the GUI version of the date splitter with pyinstaller."""

import shutil
import os

# Create temporary directory to hold everything
os.mkdir('compile_temp')

# Copy dependencies to temporary directory
shutil.copy('icon.ico', 'compile_temp')

# Run pyinstaller with correct flags from command prompt (I'm on Windows and haven't tested this on Linux or MacOS)
os.system('cmd /c "pyinstaller date_splitter_gui.py -wF -n WhatsApp_Date_Splitter --distpath ./compile_temp -i '
          'icon.ico"')

# Remove spec file (I don't think there's a flag to tell pyinstaller to not generate this)
os.remove('WhatsApp_Date_Splitter.spec')

# Zip up compiled program with dependencies
shutil.make_archive('WhatsApp_Date_Splitter', 'zip', 'compile_temp')

# Clear and remove unnecessary directories
shutil.rmtree('build')
shutil.rmtree('compile_temp')
shutil.rmtree('__pycache__')
