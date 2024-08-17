from PySide2.QtCore import Slot
from PySide2 import QtCore
from PySide2.QtWidgets import QGridLayout, QSizePolicy, QFileDialog, QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout
import random
import json
from os import path

#The main widget for the whole app.
class FileLocation(QWidget):
    def __init__(self, user_dir):
        super().__init__()
        self.supported_types = ["3gp", "aac", "flv", "m4a", "mp3", "mp4", "ogg", "wav", "webm"]
        self.current_path = "."
        self.user_dir = user_dir
        
        mainLayout = QVBoxLayout(self)
        first_row_layout = QGridLayout(self)
        
        self.label = QLabel("Choose the save location:")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        
        self.direct = QTextEdit(self)
        self.direct.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.direct.setEnabled(False)
        self.direct.setFixedHeight(30)

        search = QPushButton("...", self)
        search.clicked.connect(self.open_dialog)
        
        first_row_layout.addWidget(self.label, 0, 0, 1, 3)
        first_row_layout.addWidget(self.direct, 1, 0, 1, 3)
        first_row_layout.addWidget(search, 1, 3, 1, 1)

        mainLayout.addLayout(first_row_layout)
        #mainLayout.addWidget(self.direct, 1, 0)
        #mainLayout.addWidget(search, 1, 1)
        #mainLayout.addLayout(first_row_layout)
        self.build()
    
    def build(self):
        cur_dir = path.abspath(self.user_dir)
        file_dir = self.get_setting_file()
        if(path.exists(file_dir)):
            try:
                obj = json.load(open(file_dir, "r", encoding="UTF-8"))
                self.current_path = obj["default_path"]
                if(self.current_path == "." or self.current_path == ""):
                    self.current_path = cur_dir
                    self.direct.setText(cur_dir)
                else:
                    self.direct.setText(self.current_path)
            except:
                file = open(file_dir, "a+")
                file.write("{\"default_path\":\".\"}")
                file.close()
                self.current_path = cur_dir
                self.direct.setText(cur_dir)
        else:    
            file = open(file_dir, "a+")
            file.write("{\"default_path\":\".\"}")
            file.close()
            self.current_path = cur_dir
            self.direct.setText(cur_dir)

    def get_setting_file(self):
        path_to_file = path.abspath(path.dirname(__file__)+"/../..") + "\\settings.json"
        return path_to_file
    
    def set_setting_file(self, new_path):
        path_to_file = self.get_setting_file()
        
        built = False
        
        for i in range(2):
            try:
                obj = json.load(open(path_to_file, "r", encoding="UTF-8"))
                obj["default_path"] = new_path
                json.dump(obj, open(path_to_file, "w+", encoding="UTF-8"))
                break
            except Exception as e:
                self.build() #build the file up again from scratch
                
    def open_dialog(self, event):
        start_dir = self.current_path #set a variable that won't change
        cur_dir = path.abspath(self.user_dir)
            
        dire=""
        dialog = QFileDialog(self)
        try:
            dire = dialog.getExistingDirectory(self, "Choose a Directory", start_dir)  
            if(dire == ""):
                dire = self.current_path
            
            self.set_setting_file(dire)   
            self.current_path = dire

        except Exception as e:
            dire = cur_dir
            self.current_path = cur_dir
            self.set_setting_file(".")
        
        self.direct.setEnabled(True)
        self.direct.setText(dire)
        self.direct.setEnabled(False)
