from PySide2.QtCore import Slot
from PySide2 import QtCore
from PySide2.QtWidgets import QSizePolicy, QComboBox, QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout
import random

#The main widget for the whole app.
class FileType(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.supported_types = ["3gp", "aac", "avi", "flv", "m4a", "mkv", "mov", "mp3", "mp4", "ogg", "wav", "webm"]

        mainLayout = QVBoxLayout(self)

        first_row_layout = QVBoxLayout(self)

        label = QLabel("Choose the file type:", self)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.lists = QComboBox(self)
        self.lists.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        #lists.setFixedHeight(80)
        self.lists.addItems(self.supported_types)
        self.lists.setCurrentIndex(8)
        self.lists.currentTextChanged.connect(self.change_option)
        
        first_row_layout.addWidget(label)
        first_row_layout.addWidget(self.lists)

        mainLayout.addLayout(first_row_layout)
    
    def change_option(self, e):
        self.callback(e)
