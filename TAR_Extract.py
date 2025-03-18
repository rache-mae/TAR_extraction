from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os
import sys
import shutil
import tarfile
from datetime import *
from tkinter import filedialog

# Creating initial GUI where user chooses TAR file that will be extracted
class Window(QMainWindow):
    def __init__(extract_gui):
        super().__init__()
        # Setting GUI title 
        extract_gui.setWindowTitle('TAR Extraction')

        # Initializing layouts used to design GUI
        gen_layout = QVBoxLayout()
        tar_layout = QHBoxLayout()
        ext_layout = QHBoxLayout()

        # Setting margins and spacing of different widgets that will be used
        gen_layout.setContentsMargins(10, 10, 10, 10)
        gen_layout.setSpacing(10)

        # Creating Push Button to select TAR file
        extract_gui.tar_button = QPushButton('Select TAR File')
        extract_gui.tar_button.setFixedSize(150, 25)
        extract_gui.tar_button.setFont(QFont('Arial', 10))

        # Creating Line Edit that displays selected file
        extract_gui.tar_field = QLineEdit(extract_gui)
        extract_gui.tar_field.setReadOnly(True)
        extract_gui.tar_field.setFixedSize(300, 25)
        extract_gui.tar_field.setFont(QFont('Arial', 10))

        # Adding the last two widgets to 'tar_layout' so they will be in the same row
        tar_layout.addWidget(extract_gui.tar_button)
        tar_layout.addWidget(extract_gui.tar_field)

        # Creating Push Button to begin extraction
        extract_gui.ext_button = QPushButton('Extract')
        extract_gui.ext_button.setFixedSize(120, 25)
        extract_gui.ext_button.setFont(QFont('Arial', 10))

        # Adding the last widget to 'ext_layout'
        ext_layout.addWidget(extract_gui.ext_button)

        # Aliging the 'ext_layout' to be centered on the GUI
        ext_layout.setAlignment(Qt.AlignCenter)

        # Adding 'tar_layout' and 'ext_layout' to 'gen_layout' 
        gen_layout.addLayout(tar_layout)
        gen_layout.addLayout(ext_layout)

        # Connecting TAR and Extract Push button to functions for when they're pressed
        extract_gui.tar_button.clicked.connect(extract_gui.tar_click)
        extract_gui.ext_button.clicked.connect(extract_gui.ext_click)

        # Creating parent widget to hold child widgets created above and setting layout widget
        # for the parent widget
        widget = QWidget()
        widget.setLayout(gen_layout)
        extract_gui.setCentralWidget(widget)

    # Function for when TAR Push Button is clicked; select file window pops up and Line Edit is 
    # populated with selected file
    def tar_click(tar_file):
        global tar_dir
        tar_dir = filedialog.askopenfilename()
        tar_file.tar_field.setText(tar_dir)

    # Function for when Extract Push Button is clicked
    def ext_click(ext_start):
        # If no file is selected, an error window will pop up
        if ext_start.tar_field.text() == '':
            err_msg = QMessageBox()
            err_msg.setWindowTitle('Error!')
            err_msg.setText('Select a file!')
            err_msg.exec_()

        else:
            tar_file = tar_dir
            study_folder = os.path.basename(tar_file)
            study_path = os.path.dirname(tar_file)

            extract_file = tarfile.open(tar_file)
            extract_file.extractall(study_path)
            extract_file.close()

            destination_location = os.path.dirname(study_path)

            log_copy = destination_location + '/' + str(date.today()).replace('-', '') + '.log'

            copy = shutil.copyfile(log_file, log_copy)

            with open(log_copy, 'r') as log:
                log = log.readlines()

            delete_line = 'insert line here'

            with open(log_copy, 'w') as log_update:
                for line in log:
                    if delete_line not in line:
                        log_update.write(line)

# Initializing application GUI 
extract_gui = QApplication(sys.argv)

# Displaying GUI
window = Window()
window.show()

# Terminating script
sys.exit(extract_gui.exec())
