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

month = year = ""
outputDir = chatTitle = ""
chat_txt_list = ""


def extract_zip(file: str, output: str, name: str):
    """The function to be called first.

Function number 1 in process pipeline.

Extracts the zip and sets up global variables for all other functions."""
    global outputDir, chatTitle
    outputDir = output
    chatTitle = name

    # Make dir if it doesn't exist
    try:
        os.mkdir(f"{outputDir}/{chatTitle}")
    except OSError:
        pass

    outputDir = f"{outputDir}/{chatTitle}"  # Change outputDir for convenience

    zip_file = ZipFile(file)
    zip_file.extractall(f"{outputDir}/temp")
    zip_file.close()


def date_split():
    """MUST CALL extract_zip() FIRST.

Function number 2 in process pipeline.

The main function to be called. Splits the zip into months."""
    global outputDir, chatTitle
    global chat_txt_list

    # Creates chat_txt_list as list of lines in _chat.txt
    with open(f"{outputDir}/temp/_chat.txt", encoding="utf-8") as attachment:
        chat_txt_list = attachment.read().splitlines()

    for message in chat_txt_list:
        message_date_parse(message)

    os.remove(f"{outputDir}/temp/_chat.txt")

    files = glob(f"{outputDir}/temp/*")
    for attachment in files:
        attachment_date_parse(attachment)

    os.rmdir(f"{outputDir}/temp")


def zip_up_split_folders():
    """MUST CALL date_split() FIRST.

Function number 3 in process pipeline.

Zip up all the folders created by date_split()."""
    folders = glob(f"{outputDir}/*")
    for folder in folders:  # For all folders in outputDir
        make_archive(folder, "zip", folder)  # Create zip file from folder

        files = glob(f"{folder}/*")
        for f in files:  # For all files in folder
            os.remove(f)

        os.rmdir(folder)


def message_date_parse(string: str):
    """Split _chat.txt into months by copying messages from _chat.txt to the correct month folder."""
    global month, year

    string = string.replace("\u200e", "")  # Clear left-to-right mark
    string_bak = string

    # If blank line, just write "\n"
    if string == "":
        with open(f"{outputDir}/{chatTitle} - {month} {year}/_chat.txt", "a", encoding="utf-8") as file:
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

        month_dir = f"{outputDir}/{chatTitle} - {month} {year}"

        # If dir doesn't exist, make dir and file
        if not os.path.exists(month_dir):
            os.mkdir(month_dir)
            open(f"{month_dir}/_chat.txt", "x", encoding="utf-8")

    # Write string to _chat.txt in correct folder
    with open(f"{outputDir}/{chatTitle} - {month} {year}/_chat.txt", "a", encoding="utf-8") as file:
        file.write(string_bak + "\n")


def non_dated_attachment_parse(file_full_directory: str):
    """Parse and move attachments that aren't properly dated."""
    global month, year

    filename = file_full_directory.split("/")[-1]

    for chat_line in chat_txt_list:
        if chat_line.find(f"<attached: {filename}>"):

            date_raw = re.match(r"\[\d{2}/(\d{2}/\d{4})", chat_line).group(1)
            date_obj = datetime.strptime(date_raw, "%m/%Y")
            year = datetime.strftime(date_obj, "%Y")
            month = datetime.strftime(date_obj, "%m")

            # Remove leading zero to turn "02" into "2" but not turn "10" into "1"
            if month.startswith("0"):
                month = month.replace("0", "")

            month_dir = f"{outputDir}/{chatTitle} - {month} {year}"

            os.rename(file_full_directory, f"{month_dir}/{filename}")

            break  # Break out of for loop


def attachment_date_parse(file_full_directory: str):
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

    month_dir = f"{outputDir}/{chatTitle} - {month} {year}"

    filename = file_full_directory.split("/")[-1]

    os.rename(file_full_directory, f"{month_dir}/{filename}")


def split_single_chat(input_file: str, output_dir: str, name: str):
    """Split a chat completely by calling all the necessary functions.

This is the only function that needs to be called to split one chat."""
    try:
        extract_zip(input_file, output_dir, name)
    except OSError:
        raise OSError('Zip file "' + input_file + '" not found')
    date_split()
    zip_up_split_folders()