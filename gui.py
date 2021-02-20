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

"""This is the module that holds the GUI for the WhatsApp Date Splitter.

Classes:
    DateSplitterGUI:
        The class for th GUI for the WhatsApp Date Splitter.

        You have to create an instance (no arguments taken) and then call show() on it to show the window.

Functions:
    show_window():
        Create an instance of the GUI window and show it. Takes no arguments.

"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QShortcut
import sys
import threading
import functions


# This is a function I copied from [StackOverflow](https://stackoverflow.com/questions/64336575/select-a-file-or-a-folder-in-qfiledialog-pyqt5)
# It is a custom file selection dialog which also allows for the selection of directories
def get_open_files_and_dirs(parent=None, caption='', directory='', filter='', initial_filter='', options=None):
    """Open a Qt dialog that can select files or directories.

    I copied this function from [StackOverflow](https://stackoverflow.com/questions/64336575/select-a-file-or-a-folder-in-qfiledialog-pyqt5).
    """
    def update_text():
        # update the contents of the line edit widget with the selected files
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append('"{}"'.format(index.data()))
        line_edit.setText(' '.join(selected))

    dialog = QtWidgets.QFileDialog(parent, windowTitle=caption)
    dialog.setFileMode(dialog.ExistingFiles)
    if options:
        dialog.setOptions(options)
    dialog.setOption(dialog.DontUseNativeDialog, True)
    if directory:
        dialog.setDirectory(directory)
    if filter:
        dialog.setNameFilter(filter)
        if initial_filter:
            dialog.selectNameFilter(initial_filter)

    # by default, if a directory is opened in file listing mode,
    # QFileDialog.accept() shows the contents of that directory, but we
    # need to be able to "open" directories as we can do with files, so we
    # just override accept() with the default QDialog implementation which
    # will just return exec_()
    dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

    # there are many item views in a non-native dialog, but the ones displaying
    # the actual contents are created inside a QStackedWidget; they are a
    # QTreeView and a QListView, and the tree is only used when the
    # viewMode is set to QFileDialog.Details, which is not this case
    stacked_widget = dialog.findChild(QtWidgets.QStackedWidget)
    view = stacked_widget.findChild(QtWidgets.QListView)
    view.selectionModel().selectionChanged.connect(update_text)

    line_edit = dialog.findChild(QtWidgets.QLineEdit)
    # clear the line edit contents whenever the current directory changes
    dialog.directoryEntered.connect(lambda: line_edit.setText(''))

    dialog.exec_()
    return dialog.selectedFiles()


class DateSplitterGUI(QMainWindow):
    """The class for the GUI for the WhatsApp Date Splitter.

    Subclasses PyQt5.QtWidgets.QMainWindow. It has no public methods or attributes and only has __init__().
    You have to create an instance (no arguments taken) and then call show() on it to show the window.
    """

    def __init__(self):
        """Create an instance of the WhatsApp Date Splitter GUI.

        This method takes no arguments and you must call show() after initialising an instance of it.
        """
        super(DateSplitterGUI, self).__init__()

        # A boolean to see if the window exists. Used to close properly
        self._exists = True

        self.setWindowTitle('WhatsApp Date Splitter')
        with open('style_gui.css', 'r') as f:
            self.setStyleSheet(f.read())

        self._instructions_text = '''Steps:\n
1. Select an exported chat\n
2. Select an output directory\n
3. Enter the name of the recipient (case sensitive)\n
4. Click the split button\n
5. Wait until the 'Splitting...' text disappears\n
6. If the zip file is big, this may take some time\n
7. Choose a new zip to split or exit the program'''

        self._selected_chat = ''
        self._selected_output = ''

        self._chat_title = ''

        # ===== Create widgets

        self._instructions_label = QtWidgets.QLabel(self)
        self._instructions_label.setText(self._instructions_text)
        self._instructions_label.setAlignment(QtCore.Qt.AlignCenter)
        self._instructions_label.setProperty('class', 'instructions')

        self._select_chat_button = QtWidgets.QPushButton(self)
        self._select_chat_button.setText('Select an exported chat')
        self._select_chat_button.clicked.connect(self._select_chat_dialog)

        self._selected_chat_label = QtWidgets.QLabel(self)
        self._selected_chat_label.setText('Selected:\n')
        self._selected_chat_label.setAlignment(QtCore.Qt.AlignCenter)

        self._select_output_button = QtWidgets.QPushButton(self)
        self._select_output_button.setText('Select an output directory')
        self._select_output_button.clicked.connect(self._select_output_dialog)

        self._selected_output_label = QtWidgets.QLabel(self)
        self._selected_output_label.setText('Selected:\n')
        self._selected_output_label.setAlignment(QtCore.Qt.AlignCenter)

        self._chat_title_label = QtWidgets.QLabel(self)
        self._chat_title_label.setText('Enter the desired title of the chat:')
        self._chat_title_label.setAlignment(QtCore.Qt.AlignCenter)

        self._chat_title_textbox = QtWidgets.QLineEdit(self)

        self._spacer_label = QtWidgets.QLabel(self)
        self._spacer_label.setText('')

        self._split_chat_button = QtWidgets.QPushButton(self)
        self._split_chat_button.setText('Process all')
        self._split_chat_button.setEnabled(False)
        self._split_chat_button.clicked.connect(self._start_split_chat_thread)

        self._splitting_label = QtWidgets.QLabel(self)
        self._splitting_label.setText('')
        self._splitting_label.setAlignment(QtCore.Qt.AlignCenter)

        self._exit_button = QtWidgets.QPushButton(self)
        self._exit_button.setText('Exit')
        self._exit_button.clicked.connect(self._close_properly)

        # This is a shortcut for the exit button
        self._exit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self._exit_shortcut.activated.connect(self._close_properly)

        # ===== Arrange widgets properly

        self._vbox = QVBoxLayout()
        self._hbox = QHBoxLayout()
        self._arrange_widgets()

        self._central_widget = QWidget()
        self._central_widget.setLayout(self._hbox)
        self.setCentralWidget(self._central_widget)

        # ===== Create threads

        self._check_everything_thread = threading.Thread(target=self._loop_check_everything)
        self._check_everything_thread.start()

    def _arrange_widgets(self):
        """Arrange the widgets created by __init__() nicely."""
        self._hbox.addWidget(self._instructions_label)
        # The margins are around the edges of the window and the spacing is between widgets
        self.setContentsMargins(10, 10, 10, 10)
        self._hbox.setSpacing(20)

        self._vbox.addWidget(self._select_chat_button)
        self._vbox.addWidget(self._selected_chat_label)
        self._vbox.addWidget(self._select_output_button)
        self._vbox.addWidget(self._selected_output_label)
        self._vbox.addWidget(self._chat_title_label)
        self._vbox.addWidget(self._chat_title_textbox)
        self._vbox.addWidget(self._spacer_label)
        self._vbox.addWidget(self._split_chat_button)
        self._vbox.addWidget(self._splitting_label)
        self._vbox.addWidget(self._exit_button)

        self._hbox.addLayout(self._vbox)

    def _select_chat_dialog(self):
        """Open a dialog and allow the user to select a zip file, which then becomes self._selected_chat."""
        # This is a file select dialog to select a zip file
        self._selected_chat_raw = get_open_files_and_dirs(self, caption='Select an exported chat', filter='Zip files (*.zip)')

        try:
            # We then need to trim the raw data down into just the name of the zip file
            self._selected_chat = self._selected_chat_raw[0]
            self._selected_chat_display = self._selected_chat.split('/')[-1]
        except IndexError:
            self._selected_chat = ''
            self._selected_chat_display = ''

        self._selected_chat_label.setText(f'Selected:\n{self._selected_chat_display}')

    def _select_output_dialog(self):
        """Open a dialog and allow the user to select a directory, which then becomes self._selected_output."""
        self._selected_output_raw = get_open_files_and_dirs(self, caption='Select an output directory')

        try:
            # We then need to trim the raw data down into just the name of the folder
            self._selected_output = self._selected_output_raw[0]
        except IndexError:
            self._selected_output = ''

        self._selected_output_label.setText(f'Selected:\n{self._selected_output}')

    def _split_chat(self):
        """Pass the necessary arguments to functions.split_single_chat().

        This method actually creates a copy of all the data, then clears the attributes and passes the original values to the function.
        """
        # Disable the exit button until the split_single_chat function returns
        self._exit_button.setEnabled(False)
        self._splitting_label.setText('Splitting...')

        # Pack necessary arguments into list, copy it, and pass it to the function
        # This allows those instance attributes to be cleared or changed while the function is running
        data = [self._selected_chat, self._selected_output, self._chat_title].copy()

        # Clear everything
        # This doesn't actually clear the selected chat but it clears the label, prompting the user to choose a new one
        self._selected_chat_label.setText('')
        self._chat_title_textbox.setText('')

        functions.split_single_chat(*data)

        self._splitting_label.setText('')
        self._exit_button.setEnabled(True)

    def _start_split_chat_thread(self):
        """Start a thread running self._split_chat() so it can be run in the background."""
        self._split_chat_thread = threading.Thread(target=self._split_chat)
        self._split_chat_thread.start()

    def _get_textbox_value(self):
        """Get the text in self._chat_title_textbox and assign it to self._chat_title."""
        self._chat_title = self._chat_title_textbox.text()

    def _enable_split_button(self):
        """Set self._split_chat_button to enabled if there is data in all the conditions have been met.

        There must be a non-empty string in self._chat_title_textbox and a chat and an output must be selected.
        """
        if self._chat_title != '' and self._selected_chat != '' and self._selected_output != '':
            self._split_chat_button.setEnabled(True)
        else:
            self._split_chat_button.setEnabled(False)

    def _loop_check_everything(self):
        """Run the methods to check the textbox and enable the split button while self._exists is True."""
        while self._exists:
            self._get_textbox_value()
            self._enable_split_button()

    def _close_properly(self):
        """Set the self._exists boolean to false to end the threads and then close the window."""
        self._exists = False
        self.close()


def show_window():
    """Create an instance of DateSplitterGUI and show it. Terminate the program when the user exits the window."""
    app = QApplication(sys.argv)
    window = DateSplitterGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    show_window()
