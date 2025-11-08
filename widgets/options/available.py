from PySide6.QtCore import Slot, QThread, Signal
from PySide6 import QtCore
from PySide6.QtWidgets import QSizePolicy, QLineEdit, QTabWidget, QComboBox, QListWidget, QButtonGroup, QRadioButton, QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar
from subprocess import Popen, PIPE
import re, regex
import asyncio, threading
import yt_dlp
from ..utils.TableParser import ParseTable

#The main widget for the whole app.
class Available(QWidget):
    def __init__(self, textWidget:QTextEdit):
        super().__init__()
        self.t1 = None
        self.text = textWidget
        self.formats = []
        self.MainList = []
        
        self.seperator = " , "
        
        self.SavedChoice = [{"audio_id":"Regular", "video_id":"Regular", "vcodec":"", "audio_idx":0, "video_idx":0} for l in range(len(self.text.toPlainText().split(",")))]

        newMainLayout = QHBoxLayout(self)

        mainLayout = QVBoxLayout(self)

        zero_row_layout = QHBoxLayout(self)
        
        first_row_layout = QHBoxLayout(self)

        self.videoIndexLabel = QLabel("Video Index: ")
        self.videoIndex = QComboBox(self)
        self.videoIndex.addItem("1")
        self.videoIndex.activated.connect(self.editComboBoxChoices)
        
        label = QLabel("Click Search to find all available formats (if empty, default will be chosen): ", self)
        
        self.formats = QComboBox(self)
        self.formats.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.formats.addItem("Regular")
        self.formats.activated.connect(self.saveState)
        #lists.setFixedHeight(80)

        second_row_layout = QVBoxLayout(self)
        self.audio_label = QLabel("Choose an audio format below (Default will be chosen if nothing else is picked): ", self)
        self.audio_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.audiobox = QComboBox(self)
        self.audiobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.audiobox.addItem("Regular")
        self.audiobox.addItem("No Audio")
        self.audiobox.activated.connect(self.saveState)

        self.status_message = QLabel("", self)
        self.status_message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.status_message.setAlignment(QtCore.Qt.AlignCenter)

        third_row_layout = QHBoxLayout(self)
        self.groupings = QButtonGroup(self)
        r1 = QRadioButton("First Only", self) #First Only
        r1.setChecked(True)
        r2 = QRadioButton("Seperate", self) #All that apply
        r2.setChecked(False)
        self.groupings.addButton(r1)
        self.groupings.addButton(r2)
        third_row_layout.setAlignment(QtCore.Qt.AlignCenter)
        third_row_layout.addWidget(r1)
        third_row_layout.addWidget(r2)
        
        self.button = QPushButton("Search", self)
        self.button.clicked.connect(self.task)

        zero_row_layout.addWidget(self.videoIndexLabel)
        zero_row_layout.addWidget(self.videoIndex)
        
        first_row_layout.addWidget(self.formats)
        #first_row_layout.addWidget(self.button)

        second_row_layout.addWidget(self.audio_label)
        second_row_layout.addWidget(self.audiobox)

        mainLayout.addLayout(zero_row_layout)
        mainLayout.addWidget(label)
        mainLayout.addLayout(first_row_layout)
        mainLayout.addLayout(second_row_layout)
        mainLayout.addLayout(third_row_layout)
        mainLayout.addWidget(self.status_message)

        newMainLayout.addLayout(mainLayout)
        newMainLayout.addWidget(self.button)

    def saveState(self, e=None):
        video_index = self.videoIndex.currentIndex()
        audioChoice = self.audiobox.currentText().split(self.seperator)[-1]
        videoChoice = self.formats.currentText().split(self.seperator)[-1]
        audio_idx = self.audiobox.currentIndex()
        video_idx = self.formats.currentIndex()
        vcodec = ""
        splitVideoInfo = self.formats.currentText().split(",")
        if(len(splitVideoInfo) > 1):
            split_v = splitVideoInfo[-2].split(":")
            if(len(split_v) == 2):
                vcodec = split_v[1].strip()
        else:
            vcodec = ""
        
        #print({"audio_id":audioChoice, "video_id":videoChoice, "audio_idx":audio_idx, "video_idx":video_idx})
        self.SavedChoice[video_index] = {"audio_id":audioChoice.strip(), "video_id":videoChoice.strip(), "vcodec":vcodec.strip(), "audio_idx":audio_idx, "video_idx":video_idx}
        
    def setMainList(self, mainList):
        self.MainList = mainList
        self.editComboBoxChoices("0")
    
    def SetIndexToNumOfLinks(self, num):
        self.videoIndex.clear()
        
        for i in range(1, num+1):
            self.videoIndex.addItem(str(i))
              
    def setFormats(self, formations):
        self.formats = formations
    
    def formatString(self, object, isAudio=False):
        if(not isAudio):
            return str(object["res"].split("x")[1]) + "p" + self.seperator + str(object["fps"]) + " Frames Per Second" + self.seperator + "vcodec: " + object["vcodec"] + self.seperator + str(object["id"])
        
        else:
            return str(object["info"]) + self.seperator + str(object["id"])
        
    def editComboBoxChoices(self, e):
        self.reclear()
        idx = e
        try:
            formats = self.MainList[int(idx)]
            for format in formats:
                if(format["vcodec"].strip() == "audio only"):
                    self.audiobox.addItem(self.formatString(format, True))
                elif(format["vcodec"] != ("images" or "audio only")):
                    self.formats.addItem(self.formatString(format, False))

            self.audiobox.setCurrentIndex(self.SavedChoice[int(idx)]["audio_idx"])
            self.formats.setCurrentIndex(self.SavedChoice[int(idx)]["video_idx"])
        except:
            pass
    
    def enable_format_boxes(self, formations):
        audios = ["aac", "alac", "flac", "m4a", "mp3", "opus", "vorbis", "wav", "ogg"]
        videos = ["avi", "flv", "mkv", "mov", "mp4", "webm", "3gp"]
        
        if(formations in audios):
            self.formats.setEnabled(False)
            self.audiobox.setEnabled(True)
            self.audiobox.removeItem(1)
        elif(formations in videos):
            self.formats.setEnabled(True)
            self.audiobox.setEnabled(True)
            if(self.audiobox.itemText(1) != "No Audio"):
                self.audiobox.insertItem(1, "No Audio")
    
    def add_item(self, vid_str):
        contains = re.search("(vp9|vp09)", vid_str)
        if(contains == None):
            self.formats.addItem(vid_str)
    
    def add_audio(self, aud_str):
        self.audiobox.addItem(aud_str)

    def set_label(self, string):
        self.status_message.setText(string)

    def enable_search(self, enable):
        self.button.setEnabled(enable)
    
    def reclear(self):
        self.formats.clear()
        self.audiobox.clear()
        self.formats.addItem("Regular")
        self.audiobox.addItems(["Regular", "No Audio"])
    
    def task(self, e):
        if(self.text.toPlainText() == ""):
            self.set_label("No link was entered in the textbox above.")
            return
        self.set_label("Searching for formats...")
        self.videoIndex.clear()
        self.add_item("1")
        self.reclear()
        first_vid = self.text.toPlainText().split(",")[0].strip()
        self.t1 = WorkerThread(self.text.toPlainText(), self.groupings)
        self.t1.start()

        self.t1.formatbox.connect(self.add_item)
        self.t1.audio.connect(self.add_audio)
        self.t1.status.connect(self.set_label)
        self.t1.search.connect(self.enable_search)
        self.t1.indexing.connect(self.SetIndexToNumOfLinks)
        self.t1.mainList.connect(self.setMainList)
        
class WorkerThread(QThread):
    formatbox = Signal(str)
    audio = Signal(str)
    status = Signal(str)
    search = Signal(bool)
    indexing = Signal(int)
    mainList = Signal(list)

    def __init__(self, url, setting):
        super().__init__()
        
        self.parser = ParseTable()
        self.text = url
        self.setting = setting

        self.editable_text = ""
        self.info = ""

    def run(self):
        print("Starting")
        self.search.emit(False)

        choice = self.setting.checkedButton().text()
   
        if(self.text != ""):
            maximum = 0
            if(choice == "First Only"):
                self.text = self.text.strip().split(",")
                maximum = 1
            else:
                self.text = self.text.split(",")
                maximum = len(self.text)
                
            self.parser.clearList() #empty list as we are restarting
            
            count = 0
            
            for i in range(maximum):
                process = ""
                options = {"noplaylist":True}
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(self.text[i].strip(), download=False)
                    process = ydl.render_formats_table(info)
                
                self.parser.getInformation(process)
            
            self.indexing.emit(maximum)
            self.mainList.emit(self.parser.mainList)
            
            self.status.emit("Finished searching!")
            self.search.emit(True)
            return
        else:
            print("is empty")
        
        self.search.emit(True)