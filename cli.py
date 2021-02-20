#!/usr/bin/env python

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

from library import extract_zip, date_split, zip_up_split_folders
import os


def run_cli():
    cwd = os.getcwd()

    print("Welcome to the WhatsApp Date Splitter!")
    print()
    print(f"Please move the selected zip file to {cwd}")
    print()
    input_file = input("Please enter the name of the input zip file: ")
    if not input_file.endswith(".zip"):
        input_file += ".zip"
    print()
    output_dir = input("Please enter a full output directory: ")
    print()
    recip_name = input("Please enter the name of the recipient: ")
    print()

    try:
        print(f"Unzipping {input_file}...")
        extract_zip(input_file, output_dir, recip_name)
        print(f"Unzipped!")
    except OSError:
        print(f"{input_file} not found")
        input("Press enter to exit")
        exit(0)

    print()

    print(f"Splitting {input_file} into months...")

    date_split()

    print("Split complete!")
    print()

    print("Zipping...")

    zip_up_split_folders()

    print("Zipping complete!")
    print()
    input("Press enter to exit the program...")


if __name__ == "__main__":
    run_cli()
