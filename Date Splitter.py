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
recipName = input("Please enter the name of the recipient: ")
# print()
# outputDir = input("Please enter a full output directory: ")
outputDir = "C:/Users/joshu/Documents/GitHub/WhatsApp-Date-Splitter/venv/Output"
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
    """Parse the year and month of each line of _chat.txt."""
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

        # If dir doesn't exist, make dir and file
        if not os.path.exists(f"{outputDir}/{recipName} - {month} {year}"):
            os.mkdir(f"{outputDir}/{recipName} - {month} {year}")
            _ = open(f"{outputDir}/{recipName} - {month} {year}/_chat.txt", "x", encoding="utf-8")

    with open(f"{outputDir}/{recipName} - {month} {year}/_chat.txt", "a", encoding="utf-8") as file:
        file.write(string_bak + "\n")


for message in chat_txt_list:
    message_date_parser(message)

#
print()
print("Complete!")

#
