from zipfile import ZipFile
import os
from glob import glob
import datetime as dt
import re
import shutil

# ===== Initial Setup

print()
print("Welcome to the WhatsApp Date Splitter!")
print()
print("Please move the selected zip file to /venv/")
print()
input_file = input("Please enter the name of the input zip file (including .zip extension): ")
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

month = ""
year = ""


# ===== Define functions


def message_date_parser(string):
    """Copy messages from _chat.txt to the correct month folder."""
    global month
    global year

    string_bak = string
    string = string.replace("\u200e", "")  # Clear left-to-right mark

    if string == "":
        with open(f"{outputDir}/{recipName} - {month} {year}/_chat.txt", "a", encoding="utf-8") as file:
            file.write("\n")
        return

    if string[0] == "[":  # If date
        # Parse year and month
        string = string.split(",")[0]
        date = dt.datetime.strptime(string, "[%d/%m/%Y")
        year = dt.datetime.strftime(date, "%Y")
        month = dt.datetime.strftime(date, "%m").replace("0", "")
        month_dir = f"{outputDir}/{recipName} - {month} {year}"
        
        # If dir doesn't exist, make dir and file
        if not os.path.exists(month_dir):
            os.mkdir(month_dir)
            _ = open(f"{month_dir}/_chat.txt", "x", encoding="utf-8")

    with open(f"{outputDir}/{recipName} - {month} {year}/_chat.txt", "a", encoding="utf-8") as file:
        file.write(string_bak + "\n")


def attachment_date_parse(file):
    """Move attachments to the correct month folder."""
    global month
    global year

    # Use RegEx to parse date
    tuple_list = re.findall(r"\d+-\w+-(\d{4})-(\d{2})", file)
    # TODO: Fix non-dated file handling
    if not tuple_list:  # If file isn't properly dated, skip it
        return

    tup = tuple_list[0]

    string = f"{tup[0]} {tup[1]}"
    date = dt.datetime.strptime(string, "%Y %m")

    year = dt.datetime.strftime(date, "%Y")
    month = dt.datetime.strftime(date, "%m").replace("0", "")
    month_dir = f"{outputDir}/{recipName} - {month} {year}"

    filename = file.split("\\")[1]
    os.rename(file, f"{month_dir}/{filename}")


print(f"Splitting {input_file} into months...")

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
    shutil.make_archive(folder, "zip", folder)  # Create zip file from folder

    files = glob(f"{folder}/*")
    for file in files:  # For all files in every folder
        os.remove(file)

    os.rmdir(folder)

print("Zipping complete!")
print()
print("You may now exit the program")

#
