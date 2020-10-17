# WhatsApp-Date-Splitter is a program that takes large exported WhatsApp
# chats and splits them into months to make the zip files more manageable
# for WhatsApp-Formatter <https://github.com/DoctorDalek1963/WhatsApp-Formatter>.
#
# Copyright (C) 2020 Doctor Dalek <https://github.com/DoctorDalek1963>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from shutil import make_archive
from datetime import datetime
from zipfile import ZipFile
from glob import glob
import os
import re

# ===== Initial Setup

cwd = os.getcwd()

print("Welcome to the WhatsApp Date Splitter!")
print()
print(f"Please move the selected zip file to {cwd}")
print()
inputFile = input("Please enter the name of the input zip file: ")
if not inputFile.endswith(".zip"):
    inputFile += ".zip"
print()
outputDir = input("Please enter a full output directory: ")
print()
recipName = input("Please enter the name of the recipient: ")
print()

# Make dir if it doesn't exist
try:
    os.mkdir(f"{outputDir}\\{recipName}")
except OSError:
    pass

outputDir = f"{outputDir}\\{recipName}"  # Change outputDir for convenience

# Extract selected zip file to /full_temp/
try:
    zipRef = ZipFile(inputFile)
    print(f"Unzipping {inputFile}...")
    zipRef.extractall(f"{outputDir}\\full_temp")
    zipRef.close()
    print(f"Unzipped!")
except OSError:
    print(f"{inputFile} not found")
    input("Press enter to exit")
    exit(0)

print()

# Creates chat_txt_list as list of lines in _chat.txt
with open(f"{outputDir}\\full_temp\\_chat.txt", encoding="utf-8") as attachment:
    chat_txt_list = attachment.read().splitlines()

# Initialise time variables
month = ""
year = ""

print(f"Splitting {inputFile} into months...")


# ===== Define functions


def message_date_parse(string):  # Split _chat.txt into months
    """Copy messages from _chat.txt to the correct month folder."""
    global month, year

    string = string.replace("\u200e", "")  # Clear left-to-right mark
    string_bak = string

    # If blank line, just write "\n"
    if string == "":
        with open(f"{outputDir}\\{recipName} - {month} {year}\\_chat.txt", "a", encoding="utf-8") as file:
            file.write("\n")
        return

    if re.match(r"^\[\d{2}/\d{2}/\d{4},", string):  # If date
        # Parse year and month
        date_raw = string.split(",")[0]
        date_obj = datetime.strptime(date_raw, "[%d/%m/%Y")
        year = datetime.strftime(date_obj, "%Y")
        month = datetime.strftime(date_obj, "%m")

        if month.startswith("0"):
            month = month.replace("0", "")

        month_dir = f"{outputDir}\\{recipName} - {month} {year}"

        # If dir doesn't exist, make dir and file
        if not os.path.exists(month_dir):
            os.mkdir(month_dir)
            open(f"{month_dir}\\_chat.txt", "x", encoding="utf-8")

    # Write string to _chat.txt in correct folder
    with open(f"{outputDir}\\{recipName} - {month} {year}\\_chat.txt", "a", encoding="utf-8") as file:
        file.write(string_bak + "\n")


def non_dated_attachment_parse(file_full_directory):
    """Parse and move attachments that aren't properly dated."""
    global month, year

    filename = file_full_directory.split("\\")[-1]

    for chat_line in chat_txt_list:
        if chat_line.find(f"<attached: {filename}>"):

            date_raw = re.match(r"\[\d{2}/(\d{2}/\d{4})", chat_line).group(1)
            date_obj = datetime.strptime(date_raw, "%m/%Y")
            year = datetime.strftime(date_obj, "%Y")
            month = datetime.strftime(date_obj, "%m")

            # Remove leading zero to turn "02" into "2" but not turn "10" into "1"
            if month.startswith("0"):
                month = month.replace("0", "")

            month_dir = f"{outputDir}\\{recipName} - {month} {year}"

            try:
                os.rename(file_full_directory, f"{month_dir}\\{filename}")
            except OSError:
                print(f"{filename} was not found (NON DATED)")

            break  # Break from for loop


def attachment_date_parse(file_full_directory):
    """Move correctly dated attachments to the correct month folder."""
    global month, year

    # Use RegEx to parse date
    file_date_match = re.search(r"\d{8}-\w+-(\d{4}-\d{2})-\d{2}-\d{2}-\d{2}-\d{2}\.\w+$", file_full_directory)

    if not file_date_match:  # Separate func for non-dated attachments
        non_dated_attachment_parse(file_full_directory)
        return

    date_raw = file_date_match.group(1)
    date_obj = datetime.strptime(date_raw, "%Y-%m")
    year = datetime.strftime(date_obj, "%Y")
    month = datetime.strftime(date_obj, "%m")

    # Remove leading zero to turn "02" into "2" but not turn "10" into "1"
    if month.startswith("0"):
        month = month.replace("0", "")

    month_dir = f"{outputDir}\\{recipName} - {month} {year}"

    filename = file_full_directory.split("\\")[-1]

    try:
        os.rename(file_full_directory, f"{month_dir}\\{filename}")
    except OSError:
        print(f"{filename} was not found (DATED)")


# ===== Copy text messages of _chat.txt to month folders

for message in chat_txt_list:
    message_date_parse(message)

os.remove(f"{outputDir}\\full_temp\\_chat.txt")

# ===== Copy attachments to month folders

files = glob(f"{outputDir}\\full_temp\\*")
for attachment in files:
    attachment_date_parse(attachment)

print("Split complete!")
print()

os.rmdir(f"{outputDir}\\full_temp")

print("Zipping...")

folders = glob(f"{outputDir}\\*")
for folder in folders:  # For all folders in outputDir
    make_archive(folder, "zip", folder)  # Create zip file from folder

    files = glob(f"{folder}\\*")
    for f in files:  # For all files in folder
        os.remove(f)

    os.rmdir(folder)

print("Zipping complete!")
print()
input("Press enter to exit the program...")
