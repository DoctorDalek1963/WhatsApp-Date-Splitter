from zipfile import ZipFile
import os
from glob import glob
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
# print()
# outputDir = input("Please enter a full output directory: ")
outputDir = os.getcwd() + "Output"
print()

# Make dir if it doesn't exist
try:
    os.mkdir(f"{outputDir}/{recipName}")
except OSError:
    pass

outputDir = f"{outputDir}/{recipName}"

# Extracts selected zip file to /full_temp/
zip_ref = ZipFile(input_file)
print("Unzipping...")
zip_ref.extractall(f"{outputDir}/full_temp")
zip_ref.close()
print("Unzipped!")
print()

with open(f"{outputDir}/full_temp/_chat.txt", encoding="utf-8") as f:
    chat_txt_list = f.read().splitlines()


# ===== Define functions


def date_parser(string):
    pass


#
print()
print("Complete!")

#
