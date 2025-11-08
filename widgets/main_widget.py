from PySide2.QtCore import Slot, QThread, Signal
from PySide2 import QtCore
from PySide2.QtWidgets import QSizePolicy, QTabWidget, QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar
from .options.options_widget import FileType
from .options.location import FileLocation
from .options.filename import FileName
from .options.available import Available
import subprocess
from os import getcwd
from os import path as p1
import time
from subprocess import PIPE
import re
import yt_dlp

class WorkerThread(QThread):
    tab_label = Signal(str)
    progress = Signal(int, int, int, bool)
    start_enabled = Signal(bool)
    
    def __init__(self, url, file_ext, path, available:Available, filenames):
        super().__init__()
        self.url = url
        self.file_ext = file_ext
        self.videobox = available.formats
        self.audiobox = available.audiobox
        self.search_button = available.button
        self.FormattingSelected = available.SavedChoice
        self.apply_all_one = available.groupings.checkedButton().text()
        self.filenames = filenames
        self.process = None
        self.successful = 0
        self.total = len(self.url)
        self.path = path
        self.bail = False
        self.name = ""
        self._index = 0
        self.obtainedTitle = False
        self.seperator = ","

    def end(self):
        self.search_button.setEnabled(True)
        if(self.process != None):
            self.process.terminate()
            self.process.kill()
        self.quit()
        self.bail = True
    
    def get_id(self, audio:str, vid:str="", option="", multi=True, vcodec_t=""):
        id1 = ""
        id2 = ""
        
        if(not multi):
            split1 = audio.split(self.seperator)
            id1 = split1[-1].strip()

            if(id1 == "Regular"):
                return "140/139/ba"
            
            return id1
        
        split1 = audio.split(self.seperator) #audio_str
        split2 = vid.split(self.seperator) #video_str
        id1 = split1[-1].strip()
        id2 = split2[-1].strip()
        
        #vcodes to use: vp09 & avc
        #valid vcodec_filters: vp9, vp9.2, av1, avc
        #print(id1)
        #print(id2)
        
        vcodec = "avc"
        
        #pre-built boxes
        bv, ba, b, vcstr, lvcstr, o40, o39, co, plus = ["bv","ba", "b", "bv[vcodec*="+vcodec+"]", "bv[vcodec*="+vcodec_t+"]", "140", "139", "/", "+"]
        
        if(id1 == "No Audio"):
            if(id2 == "Regular"):
                return vcstr#"bv"+"[vcodec*="+vcodec+"]"

            return id2
        
        #due to high energy usage when using random audio format. It's best to use 139 or 140 (default to this)
        if(id1 == "Regular" and id2 == "Regular"): #video and audio are regular
            #return "bv"
            return vcstr+plus+o40+co+vcstr+plus+o39+co+bv+plus+ba
            #return "bv+ba/b*" #get best video and best aduio and combine them to one file. else combine best available formats to one file
        
        if(id1 == "Regular" and id2 != "Regular"): #audio is regular/default, video is different
            return id2+plus+o40+co+id2+plus+o39+co+lvcstr+plus+ba+co+bv+plus+ba #get best audio and whatever video option user chose else get best available combined formats

        if(id1 != "Regular" and id2 == "Regular"): #video is regular/default, audio is different
            return id1+plus+vcstr+co+vcstr+plus+o40+co+vcstr+plus+o39+co+bv+plus+ba #get best video and whatever audio option user chose else get best available combined formats

        return id1+plus+id2+co+lvcstr+plus+o39+co+vcstr+plus+ba+co+bv+plus+ba
    
    def run(self):
        self._index = 0
        mode = ""
        option = ""

        error_detected = False
        self.search_button.setEnabled(False)
        #self.apply_all_one = True

        ffmpeg_path = p1.abspath(p1.dirname(__file__)+"/..") + ""
        log_path = p1.abspath(p1.dirname(__file__)+"/.."+"/log.txt")
        
        index = 0
        
        useFirstChoice = True
        if(self.apply_all_one.strip() == "First Only"):
            useFirstChoice = True
        else:
            if(len(self.FormattingSelected) < len(self.url)):
                useFirstChoice = True
            else:
                useFirstChoice = False
        
        for i in self.url:
            self.name = ""
            filename_found = False
            extra_post_process = {}
            
            formatIndexOption = None
            
            if(useFirstChoice):
                formatIndexOption = self.FormattingSelected[0]
            else:
                formatIndexOption = self.FormattingSelected[index]
            
            index+=1
            #to find available formats:
            #PostProcessor FFMPeg: https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/postprocessor/ffmpeg.py
            #Options: https://github.com/ytdl-org/youtube-dl/blob/71b640cc5b2f15a6913a720b589bdd3ed318c154/youtube_dl/options.py#L265

            if(self.get_format() == 'aux'):
                mode="bestaudio"
                #option = self.get_id(audio=self.audiobox.currentText(), option=self.apply_all_one, multi=False)
                option = self.get_id(audio=formatIndexOption["audio_id"], option="", multi=False, vcodec_t=formatIndexOption["vcodec"])
                #print(option)
                custom = self.file_ext
                if(self.file_ext == "ogg"):
                    custom = "vorbis"
                extra_post_process = {"key":"FFmpegExtractAudio", "preferredcodec":custom}

            else:
                mode = "bv*+ba/b"

                #option = self.get_id(self.audiobox.currentText(), self.videobox.currentText(), option=self.apply_all_one)
                option = self.get_id(formatIndexOption["audio_id"], formatIndexOption["video_id"], option=self.apply_all_one, vcodec_t=formatIndexOption["vcodec"])
                extra_post_process = {"key":"FFmpegVideoConvertor", "preferedformat":self.file_ext}
                #print(option)
            
            #print(self.apply_all_one.checkedButton().text())
            time.sleep(5)
            
            if(self.bail):
                self.end()
                return
            
            self.progress.emit(0, self._index, self.total, False)
            if(i != ""):
                if(len(self.filenames) == 0):
                    #name = "%(title)s.%(ext)s"
                    self.name = "%(title)s."+self.file_ext
                    
                else:
                    #name = self.filename + ".%(ext)s"
                    if(self._index < len(self.filenames)):
                        if(self.filenames[self._index].strip() != ""):
                            self.name = self.filenames[self._index].strip() + "." + self.file_ext
                        else:
                            self.name = "%(title)s."+self.file_ext
                    else:
                        self.name = "%(title)s."+self.file_ext
                #name = "%(title)s.%(ext)s"

                options = {"noplaylist":True, "format":option, "ffmpeg_location":ffmpeg_path, "ignoreerrors":True, "overwrites":False, "progress_hooks":[self.defined], "paths":{"home":self.path}, "outtmpl":{"default":self.name}, 'postprocessors': [extra_post_process], 'progress_with_newline':False}
                
                info = None
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(i.strip(), download=True)
                    title = ""
                try:
                    title = info["title"]
                    self.obtainedTitle = False
                except:
                    pass
                self.tab_label.emit("Video: " + title)
                    #process = ydl.render_formats_table(info)
                with open(log_path, "a+") as file:
                    if(info == None):
                        self.tab_label.emit("Video: " + title + "One or more of the files requested couldn't be downloaded.")
                        file.write(time.strftime("%m-%d-%Y %H:%M:%S%p", time.localtime(time.time())) + " Download Error: One or more of the files requested couldn't be downloaded either due to failure or it was already downloaded in the selected directory " + "for file \'" + title + "\'\n")
                        file.seek(0)
                    else:
                        self.progress.emit(100, self._index, self.total, False)
                        file.write(time.strftime("%m-%d-%Y %H:%M:%S%p", time.localtime(time.time())) + " Download: Successful Download for file \'" + title + "\'\n")
                        file.seek(0)
                        
                time.sleep(1.5)
                self._index+=1
                self.progress.emit(0,0,0,True)

        
        self.start_enabled.emit(True)
        self.search_button.setEnabled(True)
    
    def defined(self, d):
        if(self.bail):
            print("Bailing")
            self.end()
            return
        
        #pattern = "\d+\.\d+[^\%]"
        pattern = "\d+\.\d+[\%]"
        accepted = False

        """
        if(not self.obtainedTitle):
            try:
                t = d["filename"].split("\\")
                title = re.sub("\.\w+", "", t[-1])
                self.tab_label.emit("Video: " + title)
                self.obtainedTitle = True
            except Exception as e:
                print("Title Error: " + str(e))
        """
        #self.progress.emit(0, index, self.total)
        
        count = 0
        #print(d)
        
        #filepath = ""
        inner_pattern = ".+[^%]"
        try:
            #progress = str(round((d["downloaded_bytes"]/d["total_bytes"])*100, 2)) + "%"
            progress = d['_percent_str']
            
            inner_reg = re.search(pattern, progress.strip())
            #print("Progress: " + str(progress))
            #print(inner_reg)
            
            if(inner_reg != None):
                #accepted = True
                try:
                    #print(inner_reg.group())
                    perc = float(inner_reg.group().replace("%",""))
                    if(perc > 100):
                        pass
                        #self.progress.emit(100, self._index, self.total, False)
                    self.progress.emit(round(perc, 0), self._index, self.total, False)
                except:
                    pass
        except Exception as e:
            print("Error Occurred with progress: " + str(e))
            pass

        #if(accepted):
         #   self.progress.emit(100, self._index, self.total, False)
        #else:
            #error_detected = True
         #   if(count == 0):
          #      self.progress.emit(0, self._index, self.total, False)
           # else:
            #    self.progress.emit(100, self._index, self.total, False)
    
    def get_format(self):
        audios = ["aac", "alac", "flac", "m4a", "mp3", "opus", "vorbis", "wav", "ogg"]
        videos = ["avi", "flv", "mkv", "mov", "mp4", "webm", "3gp"]
        
        if(self.file_ext in audios):
            return "aux"
        
        if(self.file_ext in videos):
            return "vux"
            
    def formats(self):
        formats = []
        ext = ""
        
        pattern = "\\-{10,}"
        access = False
        
        for i in self.process.stdout.readlines():
            column = 1
            reading = False
            
            if(re.search(pattern, i) != None):
                access = True
                continue
            
            if(access):
                for k in i:
                    if(k == " "):
                        if(reading == True):
                            formats.append(ext)
                            ext = ""
                            break
                            
                        if(column != 2):
                            column+=1
                        if(column == 2):
                            reading = True
                        continue
                    
                    if(reading == True):
                        ext+=k
        
        if self.file_ext in set(formats):   
            print(set(formats))
                
#The main widget for the whole app.
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.process = None
        self.thread = None
        
        self.max_downloads = 10

        self.setWindowTitle("Crossfield")
        
        self.url_label = QLabel("YouTube URL: ", self)
        self.url_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.text = QTextEdit(self)
        self.text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.text.setFixedHeight(100)

        self.progress = QProgressBar(self)
        self.progress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.progress.setAlignment(QtCore.Qt.AlignCenter)
        self.progress.setMaximum(100)

        self.progress_label = QLabel("", self)
        self.progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
          
        #tabs
        tabs = QTabWidget(self)
        tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.Location = FileLocation(getcwd())
        self.Name = FileName()
        self.Qualities = Available(self.text)
        self.Type = FileType(self.Qualities.enable_format_boxes)
        
        tabs.addTab(self.Type, "Type")
        tabs.addTab(self.Location, "Location")
        tabs.addTab(self.Name, "Name")
        tabs.addTab(self.Qualities, "Formats")

        #post/concurrent status label
        self.tab_label = QLabel("", self)
        self.tab_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        #start/stop button
        button_layouts = QHBoxLayout()
        
        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.start)
        
        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.clicked.connect(self.stop)
        self.cancel_btn.setEnabled(False)
        
        button_layouts.addWidget(self.button)
        button_layouts.addWidget(self.cancel_btn)
        
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(tabs)
        self.layout.addWidget(self.tab_label)
        self.layout.addLayout(button_layouts)

        #self.setMinimumSize(400, 300)
        self.setFixedSize(700, 490)
    
    def set_progress(self, value=0, index=0, maxi=0, finished=False):
        if(not finished):
            self.progress_label.setText("Downloading: " + str(index) + "/" + str(maxi) + " file(s)")
            self.progress.setValue(value)
        else:
            self.progress_label.setText("Download(s) Finished")
            #self.progress.setValue(value)

    def set_button_enabled(self, enable):
        self.button.setEnabled(enable)
        
        if(self.button.isEnabled()):
            self.cancel_btn.setEnabled(False)
        else:
            self.cancel_btn.setEnabled(True)
    
    def set_tab_status(self, value):
        self.tab_label.setText(value)
    
    def start(self, e):
        if(self.button.text() == "Start"):
            if(self.text.toPlainText() != ""):
                
                self.tab_label.setText("")
            
                if(self.thread != None):
                    self.thread.quit()
                    self.thread = None
                
                #process = None
                #process = subprocess.Popen(["cmd.exe", "/c", "cd", "..", "&&", "yt-dlp", "-w", "-F", "https://www.youtube.com/watch?v=zIz85dwehIg&ab_channel=%E7%B7%8B%E6%9C%88"], stdout=PIPE, encoding="UTF-8")
                #print(process.stdout.read())
                
                if(self.Location.direct.toPlainText() != ""):
                    self.set_button_enabled(False)
                    vid_str = ""
                    vids = self.text.toPlainText().split(",")
                    filenames = self.Name.name.text().split(",")
                    
                    self.set_progress(0, 0, len(vids))

                    self.thread = WorkerThread(vids, self.Type.lists.currentText(), self.Location.direct.toPlainText(), self.Qualities, filenames)
                    self.thread.start()
                
                    self.thread.tab_label.connect(self.set_tab_status)
                    self.thread.progress.connect(self.set_progress)
                    self.thread.start_enabled.connect(self.set_button_enabled)
                    
                else:
                    self.progress_label.setText("Please choose a location to download the file(s) in the 'Location' tabs below.")
            else:
                self.progress_label.setText("No Link Was Entered")

    def stop(self):
        self.Qualities.button.setEnabled(True)
        if(self.thread != None):
            self.thread.end()
        
        else:
            self.thread.quit()
            #self.thread.quit()
        self.set_button_enabled(True)
        
    def __del__(self):
        if(self.thread != None):
            self.thread.quit()
