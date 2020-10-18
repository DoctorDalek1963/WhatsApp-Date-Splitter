# WhatsApp-Date-Splitter

![License](https://img.shields.io/github/license/DoctorDalek1963/WhatsApp-Date-Splitter)
![Release](https://img.shields.io/github/v/release/DoctorDalek1963/WhatsApp-Date-Splitter)
![Last Commit](https://img.shields.io/github/last-commit/DoctorDalek1963/WhatsApp-Date-Splitter)

![Repo Size](https://img.shields.io/github/repo-size/DoctorDalek1963/WhatsApp-Date-Splitter)
![Code Size](https://img.shields.io/github/languages/code-size/DoctorDalek1963/WhatsApp-Date-Splitter)

A program to split exported WhatsApp chats into months to allow for more convenient zip file sizes to be formatted.

I have previously made a [program](https://github.com/DoctorDalek1963/WhatsApp-Formatter) to reformat exported WhatsApp chats into HTML files.
This program is intended to split exported chats into zip files containing truncated text files and the associated attachments.
This will make it easier for the formatter to produce smaller HTML files.

## Steps:

1. Export the desired chat (must be a private chat. Group chats don't work)
2. Copy the zip file to the directory specified by the program
3. Decide on an export directory and copy it
4. Run the Python script and enter the name of the zip file, the name of the recipient, and the output directory
5. The program will create a collection of zip files organised by month.
6. You may need to manually move some attachment files that don't have their dates in their filenames.
7. Remove the complete zip file
