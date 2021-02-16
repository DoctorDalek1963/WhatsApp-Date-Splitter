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

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys


class DateSplitterGUI(QMainWindow):
    def __init__(self):
        super(DateSplitterGUI, self).__init__()

        self.setWindowTitle('WhatsApp Date Splitter')


def show_window():
    app = QApplication(sys.argv)
    window = DateSplitterGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    show_window()
