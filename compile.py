#!/usr/bin/env python

"""Fully compile the GUI version of the date splitter with pyinstaller."""

import shutil
import os
import subprocess


def compile_date_splitter(gui=True):
    """Compile the WhatsApp Date Splitter using pyinstaller.

This function takes one argument, gui, which is true by default. If it's true, this function will compile the GUI version of the formatter, if false, it will compile the command line version."""
    # Get filename from gui boolean
    filename = 'gui.py' if gui else 'cli.py'

    # Create temporary directory to hold everything
    os.mkdir('compile_temp')

    # Copy dependencies to temporary directory
    shutil.copy('icon.ico', 'compile_temp')

    # Run pyinstaller with correct flags from the shell
    subprocess.call(f'pyinstaller {filename} -wF -n WhatsApp_Date_Splitter --distpath ./compile_temp -i icon.ico', shell=True)

    # Remove spec file (I don't think there's a flag to tell pyinstaller to not generate this)
    os.remove('WhatsApp_Date_Splitter.spec')

    # Zip up compiled program with dependencies
    shutil.make_archive('WhatsApp_Date_Splitter', 'zip', 'compile_temp')

    # Clear and remove unnecessary directories
    shutil.rmtree('build')
    shutil.rmtree('compile_temp')
    shutil.rmtree('__pycache__')


if __name__ == '__main__':
    compile_date_splitter()
