from PySide6.QtCore import Slot
from PySide6 import QtCore
from PySide6.QtWidgets import QSizePolicy, QLineEdit, QWidget, QPushButton, QLabel, QVBoxLayout

#The main widget for the whole app.
class FileName(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self)

        first_row_layout = QVBoxLayout(self)

        label = QLabel("Enter a name for your file (if empty, default will be chosen. Applies to first successful file only): ", self)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.name = QLineEdit(self)
        self.name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        #lists.setFixedHeight(80)

        first_row_layout.addWidget(label)
        first_row_layout.addWidget(self.name)

        #mainLayout.addWidget(label)
        mainLayout.addLayout(first_row_layout)
