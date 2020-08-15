import zipfile as zf
import os
import glob as g
import datetime as dt
import shutil

# ===== Initial Setup

print()
print("Welcome to the WhatsApp Date Splitter!")
print()
print("Please move the selected zip file to /venv/")
print()
input_file = input("Please enter the name of the input zip file (including .zip extension): ")
print()
recipName = input("Please enter the name of the recipient (case sensitive): ")
print()
outputDir = input("Please enter a full output directory: ")
print()

# Extracts selected zip file to /full_temp/
zip_ref = zf.ZipFile(input_file)
print("Unzipping...")
zip_ref.extractall("full_temp")
zip_ref.close()
print("Unzipped!")
print()

# Make dir if it doesn't exist
try:
    os.mkdir(f"{outputDir}/{recipName}")
except OSError:
    pass

outputDir = f"{outputDir}/{recipName}"

#
print()
print("Complete!")

#
