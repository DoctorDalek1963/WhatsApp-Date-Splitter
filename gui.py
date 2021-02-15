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

from splitter_functions import split_single_chat
from tkinter import filedialog, StringVar
import tkinter as tk
import threading
import _tkinter
import os

cwd = os.getcwd()
inputZip = outputDir = recipName = ""
startExportFlag = finishExportFlag = False

descriptionText = """Steps:\n
1. Select an exported chat\n
2. Select an output directory\n
3. Enter the name of the recipient (case sensitive)\n
4. Click the split button\n
5. Wait until the 'Splitting...' text disappears\n
6. If the zip file is big, this may take some time\n
7. Choose a new zip to split or exit the program"""

default_x_padding = 10
default_y_padding = 5
gap_y_padding = (5, 15)

# ===== Functions used on tk buttons


def select_zip():
    global inputZip
    inputZip = filedialog.askopenfilename(initialdir=cwd, title="Select an exported chat",
                                          filetypes=[("Zip files", "*.zip")])


def select_output_dir():
    global outputDir
    outputDir = filedialog.askdirectory(initialdir="/", title="Select an output directory")


def start_export():
    global startExportFlag
    startExportFlag = True


def process():
    global inputZip, recipName, outputDir
    global finishExportFlag
    fixed_name_zip = inputZip
    fixed_name_recip = recipName
    fixed_name_dir = outputDir

    split_single_chat(fixed_name_zip, fixed_name_dir, fixed_name_recip)
    finishExportFlag = True


# ===== Tkinter initialisation

# Init window
root = tk.Tk()
root.title("WhatsApp Date Splitter")
root.resizable(False, False)
root.iconbitmap('icon.ico')

selected_zip_var = StringVar()
selected_output_var = StringVar()
splitting_string_var = StringVar()


# ===== Create widgets

# Create input widgets
select_zip_button = tk.Button(root, text="Select an exported chat", command=select_zip, bd=3)
selected_zip_label = tk.Label(root, textvariable=selected_zip_var)

select_output_button = tk.Button(root, text="Select an output directory", command=select_output_dir, bd=3)
selected_output_label = tk.Label(root, textvariable=selected_output_var)

name_box_label = tk.Label(root, text="Enter the name of the recipient:")
enter_name_box = tk.Entry(root)

# Instructions for use
description_label = tk.Label(root, text=descriptionText)

# Create special button widgets
split_button = tk.Button(root, text="Split", command=start_export, state="disabled", bd=3)
splitting_string_label = tk.Label(root, textvariable=splitting_string_var)
exit_button = tk.Button(root, text="Exit", command=root.destroy, bd=3)


# ===== Place widgets

# Instructions for use
description_label.grid(row=1, rowspan=7, column=0, padx=(default_x_padding, 50), pady=15)

# Select zip and display name
select_zip_button.grid(row=0, column=2, padx=default_x_padding, pady=(15, default_y_padding))
selected_zip_label.grid(row=1, column=2, padx=default_x_padding, pady=gap_y_padding)

# Select output directory and display it
select_output_button.grid(row=2, column=2, padx=default_x_padding, pady=default_y_padding)
selected_output_label.grid(row=3, column=2, padx=default_x_padding, pady=gap_y_padding)

# Enter recipient name
name_box_label.grid(row=4, column=2, padx=default_x_padding, pady=default_y_padding)
enter_name_box.grid(row=5, column=2, padx=default_x_padding, pady=(default_y_padding, 25))

# Place special button widgets
split_button.grid(row=6, column=2, padx=default_x_padding, pady=default_y_padding)
splitting_string_label.grid(row=7, column=2, padx=default_x_padding, pady=default_y_padding)
exit_button.grid(row=8, column=2, padx=default_x_padding, pady=(default_y_padding, 15))


# ===== Loop to sustain window


def update_loop():
    """Infinite loop to continually update the root tkinter window and check for conditions
to activate/deactivate buttons."""
    global recipName, inputZip
    global startExportFlag, finishExportFlag

    while True:
        try:
            if enter_name_box.get():
                recipName = enter_name_box.get()

            truncated_input_zip = inputZip.split("/")[-1]
            selected_zip_var.set(f"Selected: \n{truncated_input_zip}")

            selected_output_var.set(f"Selected: \n{outputDir}")

            if inputZip and outputDir and recipName:
                split_button.config(state="normal")
            else:
                split_button.config(state="disabled")

            if startExportFlag:
                process_thread = threading.Thread(target=process)
                process_thread.start()
                splitting_string_var.set("Splitting...")

                # Allow split button to be greyed out
                inputZip = ""
                enter_name_box.delete(0, tk.END)  # Clear entry box

                select_zip_button.config(state="disabled")
                select_output_button.config(state="disabled")
                enter_name_box.config(state="disabled")
                exit_button.config(state="disabled")
                startExportFlag = False

            if finishExportFlag:
                splitting_string_var.set("")
                select_zip_button.config(state="normal")
                select_output_button.config(state="normal")
                enter_name_box.config(state="normal")
                exit_button.config(state="normal")
                finishExportFlag = False

            root.update()

        except _tkinter.TclError:
            return


update_loop()
