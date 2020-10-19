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

import os
from splitter_functions import extract_zip, date_split, zip_up_split_folders

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

try:
    print(f"Unzipping {inputFile}...")
    extract_zip(inputFile, outputDir, recipName)
    print(f"Unzipped!")
except OSError:
    print(f"{inputFile} not found")
    input("Press enter to exit")
    exit(0)

print()

print(f"Splitting {inputFile} into months...")

date_split()

print("Split complete!")
print()

print("Zipping...")

zip_up_split_folders()

print("Zipping complete!")
print()
input("Press enter to exit the program...")