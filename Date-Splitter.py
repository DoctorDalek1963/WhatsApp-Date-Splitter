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
input_file = input("Please enter the name of the input zip file: ")
if not input_file.endswith(".zip"):
    input_file = f"{input_file}.zip"
print()
recipName = input("Please enter the name of the recipient: ")
print()
outputDir = input("Please enter a full output directory: ")
print()

# Make dir if it doesn't exist
try:
    os.mkdir(f"{outputDir}/{recipName}")
except OSError:
    pass

outputDir = f"{outputDir}/{recipName}"  # Change outputDir for convenience

# Extracts selected zip file to /full_temp/
zip_ref = ZipFile(input_file)
print("Unzipping...")
zip_ref.extractall(f"{outputDir}/full_temp")
zip_ref.close()
print("Unzipped!")
print()

# Creates chat_txt_list as list of _chat.txt
with open(f"{outputDir}/full_temp/_chat.txt", encoding="utf-8") as f:
    chat_txt_list = f.read().splitlines()

# Initialise time variables
month = ""
year = ""

print(f"Splitting zip into months...")


# ===== Define functions


def message_date_parser(string):  # Split _chat.txt into months
    """Copy messages from _chat.txt to the correct month folder."""
    # Import global variables
    global month, year

    string = string.replace("\u200e", "")  # Clear left-to-right mark
    string_bak = string

    # If blank line, just write "\n"
    if string == "":
        with open(f"{outputDir}/{recipName} - {month} {year}/_chat.txt", "a", encoding="utf-8") as file:
            file.write("\n")
        return

    if re.match(r"^\[\d{2}/\d{2}/\d{4},", string):  # If date
        # Parse year and month
        string = string.split(",")[0]
        date = datetime.strptime(string, "[%d/%m/%Y")
        year = datetime.strftime(date, "%Y")
        month = datetime.strftime(date, "%m").replace("0", "")
        month_dir = f"{outputDir}/{recipName} - {month} {year}"

        # If dir doesn't exist, make dir and file
        if not os.path.exists(month_dir):
            os.mkdir(month_dir)
            _ = open(f"{month_dir}/_chat.txt", "x", encoding="utf-8")

    # Write string to _chat.txt in correct folder
    with open(f"{outputDir}/{recipName} - {month} {year}/_chat.txt", "a", encoding="utf-8") as file:
        file.write(string_bak + "\n")


def attachment_date_parse(file):  # Move attachments to the correct folder
    """Move attachments to the correct month folder."""
    global month, year

    # Use RegEx to parse date
    tuple_list = re.findall(r"\d{8}-\w+-(\d{4}-\d{2})", file)

    # TODO: Fix non-dated file handling
    if not tuple_list:  # If file isn't properly dated, skip it
        return

    string = tuple_list[0]
    date = datetime.strptime(string, "%Y-%m")

    # Format year and month
    year = datetime.strftime(date, "%Y")
    month = datetime.strftime(date, "%m").replace("0", "")
    month_dir = f"{outputDir}/{recipName} - {month} {year}"

    # Move file
    filename = file.split("\\")[-1]
    os.rename(file, f"{month_dir}/{filename}")


# ===== Copy text messages of _chat.txt to month folders

for message in chat_txt_list:
    message_date_parser(message)

os.remove(f"{outputDir}/full_temp/_chat.txt")

# ===== Copy attachments to month folders

files = glob(f"{outputDir}/full_temp/*")
for f in files:
    attachment_date_parse(f)

print("Split complete!")
print()
print(f"There may be some files left in {outputDir}/full_temp")
print("Please move them to their correct folders if possible")
print()
input("Press enter to finalise...")
print()
print("Zipping...")

os.rmdir(f"{outputDir}/full_temp")

folders = glob(f"{outputDir}/*")
for folder in folders:  # For all folders in outputDir
    make_archive(folder, "zip", folder)  # Create zip file from folder

    files = glob(f"{folder}/*")
    for f in files:  # For all files in every folder
        os.remove(f)

    os.rmdir(folder)

print("Zipping complete!")
print()
input("Press enter to exit the program...")
