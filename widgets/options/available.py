from PySide2.QtCore import Slot, QThread, Signal
from PySide2 import QtCore
from PySide2.QtWidgets import QSizePolicy, QComboBox, QButtonGroup, QRadioButton, QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
#from subprocess import Popen, PIPE #used for backup only
import re, regex #both used due to testing
#import asyncio, threading # these were no longer needed
import yt_dlp

#The main widget for the whole app.
class Available(QWidget):
    def __init__(self, textWidget:QTextEdit):
        super().__init__()
        self.t1 = None
        self.text = textWidget

        newMainLayout = QHBoxLayout(self)

        mainLayout = QVBoxLayout(self)

        first_row_layout = QHBoxLayout(self)

        label = QLabel("Click Search to find all available formats (if empty, default will be chosen): ", self)

        self.formats = QComboBox(self)
        self.formats.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.formats.addItem("Regular")
        #lists.setFixedHeight(80)

        second_row_layout = QVBoxLayout(self)
        self.audio_label = QLabel("Choose an audio format below (Default will be chosen if nothing else is picked): ", self)
        self.audio_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.audiobox = QComboBox(self)
        self.audiobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.audiobox.addItem("Regular")
        self.audiobox.addItem("No Audio")

        self.status_message = QLabel("", self)
        self.status_message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.status_message.setAlignment(QtCore.Qt.AlignCenter)

        third_row_layout = QHBoxLayout(self)
        self.groupings = QButtonGroup(self)
        r1 = QRadioButton("First Only", self)
        r1.setChecked(True)
        r2 = QRadioButton("All that apply", self)
        r2.setChecked(False)
        self.groupings.addButton(r1)
        self.groupings.addButton(r2)
        third_row_layout.setAlignment(QtCore.Qt.AlignCenter)
        third_row_layout.addWidget(r1)
        third_row_layout.addWidget(r2)
        
        self.button = QPushButton("Search", self)
        self.button.clicked.connect(self.task)

        first_row_layout.addWidget(self.formats)
        #first_row_layout.addWidget(self.button)

        second_row_layout.addWidget(self.audio_label)
        second_row_layout.addWidget(self.audiobox)

        mainLayout.addWidget(label)
        mainLayout.addLayout(first_row_layout)
        mainLayout.addLayout(second_row_layout)
        mainLayout.addLayout(third_row_layout)
        mainLayout.addWidget(self.status_message)

        newMainLayout.addLayout(mainLayout)
        newMainLayout.addWidget(self.button)

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
        self.reclear()
        first_vid = self.text.toPlainText().split(",")[0].strip()
        self.t1 = WorkerThread(self.text.toPlainText())
        self.t1.start()

        self.t1.formatbox.connect(self.add_item)
        self.t1.audio.connect(self.add_audio)
        self.t1.status.connect(self.set_label)
        self.t1.search.connect(self.enable_search)

class WorkerThread(QThread):
    formatbox = Signal(str)
    audio = Signal(str)
    status = Signal(str)
    search = Signal(bool)

    def __init__(self, url):
        super().__init__()
        self.text = url

        self.editable_text = ""
        self.info = ""

    def run(self):
        print("Starting")
        builder = ""
        self.search.emit(False)
        main_list = []
        audio_formats = []
        video_formats = []

        if(self.text != ""):
            process = ""
            options = {"noplaylist":True}
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(self.text.strip(), download=False)
                process = ydl.render_formats_table(info)
            
            #If command line needed, use this, process = Popen(["cmd.exe", "/c", "cd", "../..", "&&", "yt-dlp", "-w", "--no-playlist", "--list-formats", self.text.strip()], stdout=PIPE, encoding="UTF-8")
            
            end_header = False

            start_pattern = "(-{10,}|─{10,})"
            start_reading = False
            
            #lines = process.stdout.readlines()
            #lines = self.readlines(process)

            outter_count = 0

            counter2 = 0
            
            for i in self.readlines(process): #lines
                if(counter2 <= 1):
                    start_reading = True
                    counter2+=1
                    continue
                
                stripped = i.strip()
                matcher = re.search(start_pattern, i)
                #print()
                #if(counter2 <= 4):
                 #   print(i)
                  #  return
                string_list = []

                if(matcher != None):
                    start_reading = True
                    continue
                
                readin = False
                count = 0

                #outter_count +=1
                if(start_reading):
                    outter_count+=1
                    end = 0
                    linkage = 1
                    
                    #splits = i.split("|")
                    for k in range(len(stripped)):
                        if(stripped[k] != "|" and stripped[k] != "\n" and stripped[k] != "\u2502"):
                            builder += stripped[k]
                            readin = False
                        else:
                            if(stripped[k] != "|" and stripped[k] != "\u2502"):                 
                                #print(builder)
                                builder += stripped[k]
                            
                            self.section_cut(builder, outter_count, linkage)
                            builder = ""
                            linkage+=1
                            
                        if(end == len(stripped)-1):
                            #print("Builder: " + builder)
                            self.section_cut(builder, outter_count, linkage)
                            builder = ""
                            linkage = 0

                            #self.formatbox.emit(self.editable_text)
                            find_audio = "Video:audio-only"
                            find_video = "Audio:video-only"
                            if(self.editable_text != ""):
                                if(re.search(find_audio, self.editable_text) != None):
                                    self.audio.emit(self.text_to_readable(self.editable_text, True))
                                    #self.audio.emit(self.editable_text)
                                    #self.text_to_readable(self.editable_text)
                                if(re.search(find_video, self.editable_text) != None):
                                    #quality_pattern = re.search("\d+p", self.editable_text)
                                    #video_formats.append(self.editable_text)
                                    self.formatbox.emit(self.text_to_readable(self.editable_text))
    
                            self.editable_text = ""
                            break
                        
                        end+=1

            self.status.emit("Finished searching!")           
            #print(main_list)   
            #print(audio_formats, sep="\n")
            #print(video_formats)                  
        
        else:
            print("is empty")
        
        self.search.emit(True)
    
    def readlines(self, input_str):
        string = ""
        for h in range(len(input_str)):
            if(input_str[h] == "\n" or input_str[h] == "\0"):
                yield string
                string = ""
            string += input_str[h]
    
    def text_to_readable(self, string, is_audio=False):
        info_format = ""
        if(is_audio):
            info_format = ".*"
        else:
            info_format = "\d+p\d*|Info:.*"
        pattern = "(Info:" + info_format + "|FPS:\d+|FPS:|Size:\d+\.\d+[a-zA-Z]{2,6}|Size:|Res:\d+x\d+|Res:|ID:\d+|ID:|Video:.*\v|Video:|SampleRate:\d+[a-z]|SampleRate:|BitRate:\d+[a-z]|BitRate:)"
        
        matches = re.findall(pattern, string)

        #indexes (0-id, 1-resolution, 2-fps, 3-size, 4-vcodec, 5-sample rate 6-bit rate, 7-info)
        
        quality_or_audio = matches[7].split(":")
        ident = matches[0].split(":")
        res = matches[1].split(":")
        fps = matches[2].split(":")
        size = matches[3].split(":")
        bitrate = matches[6].split(":")
        sample_rate = matches[5].split(":")
        vcodec = matches[4].split(":")
       
        
        if(len(quality_or_audio) > 1):
            quality_or_audio = quality_or_audio[1]

        if(len(ident) > 1):
            ident = ident[1]

        if(len(fps) > 1):
            fps = fps[1]
        
        if(len(size) > 1):
            size = size[1]
        
        bitrate = bitrate[1]
        if(bitrate == ''):
            bitrate = "N/A"
        
        sample_rate = sample_rate[1]
        if(sample_rate == ''):
            sample_rate = "N/A"

        vcodec = vcodec[1].replace("\v", "")
        if(vcodec == ""):
            vcodec = "N/A"
        #if(len(quality_or_audio) > 1):
         #   quality_or_audio = quality_or_audio[1]
        
        if(not is_audio):
            return str(quality_or_audio) + " - " + str(fps) + " Frames Per Second" + " - vcodec: " + vcodec + " - " + str(ident)
        
        else:
            return str(quality_or_audio) + " - " + str(sample_rate) + " Sample Rate - " +  str(bitrate) + " Bit Rate - "+ str(ident)
        
        
        #print(str(quality_or_audio) + " - " + str(sample_rate) + " Sample Rate - " +  str(bitrate) + " Bit Rate - "+ str(ident))
        #print(matches)

    def section_cut(self, string, row_num, list_num):
        seperator = ""
        clean_seperator = ""
        format = []
        format.append(str(row_num))
        format.append(str(list_num))
        
        text_in_ansiColor_pattern = "(\\x1b\[0\;\d+m|\\x1b\[0m)"
        ansi_color_pattern = "\\x1b\[0\;\d+m.+\\x1b\[0m"
        
        second_string = ""
        keep_skipping = True
        end = 0
        length = len(string)
        for j in range(length):
            end+=1
            
            if(keep_skipping):
                if(string[j] == " "):
                    if(regex.search(text_in_ansiColor_pattern, seperator) != None):
                        stuff = clean_seperator
                        
                        if(stuff != None):
                            format.append(stuff.strip())

                        seperator = ""
                        continue
                    #print(seperator)
                    format.append(seperator)
                    seperator = ""
                    continue
                else:
                    seperator+=string[j]
                    clean_seperator = re.sub(text_in_ansiColor_pattern, "", seperator, 3, re.IGNORECASE).strip()

            else:
                second_string+=string[j]
                cleaned_secString = re.sub(text_in_ansiColor_pattern, "", second_string, 3, re.IGNORECASE).strip()
                if(cleaned_secString == "only"):
                    keep_skipping = True
                    format.append(clean_seperator+"-"+cleaned_secString)
                    seperator=""
                    second_string = ""
                    continue
                
            if(end == len(string)):
                if(clean_seperator != ''):
                    format.append(clean_seperator)
            
            if(clean_seperator == "audio" or clean_seperator == "video"):
                keep_skipping = False
                continue
        
        #if(format[1] == "1"):
            #print(format)
        self.label(format)
        #print(format)
        #print(string)  
    
    def label(self, list_object):
        id_idx = 2
        section_number_idx = 1
        
        #grouping section 1
        if(list_object[section_number_idx] == "1"):
            res_pattern = "(\d+x\d+|audio-only)"
            ext_pattern="(m4a|mp4|mhtml)"
            counter = 0
            final_list = list_object[2:]

            ext = ""
            resolution = ""
            ident = ""
            channel = ""
            fps = ""
            
            length = len(final_list)
            
            for a in range(length):
                if(final_list[a] != ""):
                    res_matcher = re.match(res_pattern, final_list[a])
                    ext_matcher = re.match(ext_pattern, final_list[a])

                    if(counter == 0): #get id
                        ident = final_list[a]
                        counter+=1
                        continue

                    if(ext_matcher != None):
                        ext = ext_matcher.group()

                    if(res_matcher != None): #get resolution
                        resolution = res_matcher.group()
                        
                    counter+=1
                
                if(a == length-1): #get channel and fps if there
                    channel = final_list[a]
                    fps = final_list[a-3]
            
            self.editable_text += "ID:"+ident + ", Res:" + resolution + ", FPS:" + fps
            #return([ident, ext, resolution, fps, channel])
            
        #grouping section 2
        if(list_object[section_number_idx] == "2"):
            file_size_pattern = "(~|=)?(\d+)?\.\d+[a-zA-Z]+"
            tbr_pattern = "\d+[a-z]{1}"
            
            counter = 0
            final_list = list_object[2:]
            file_size = ""
            proto = ""
            tbr = ""
            
            length = len(final_list)
            
            for a in range(length):
                if(final_list[a] != ""):
                    file_matcher = re.match(file_size_pattern, final_list[a])
                    
                    if(file_matcher != None): #get resolution
                        file_size = file_matcher.group()
                
                if(a == length-1): #get channel and fps if there
                    if(final_list[a] == ""):
                        if(final_list[a-1] != ""):
                            proto = final_list[a-1]
                            if(re.match(tbr_pattern, final_list[a-2]) != None):
                                tbr = final_list[a-2]
                    else:
                        proto = final_list[a]
                        tbr = final_list[a-1]
                    
            self.editable_text += ", Size:" + file_size
            #return([file_size, tbr, proto])
        
        #grouping section 3
        if(list_object[section_number_idx] == "3"):
            vid_codec_idx = 1
            
            #patterns
            more_info_pattern = "(.+,|\[\w+\])"
            more_info_matcher = None
            acodec_pattern = "(.+\..+\..+|video-only|unknown)"

            #list and variables
            final_list = list_object[2:]
            vcodec = ""
            acodec = ""
            vbr = ""
            more_info = ""
            abr = ""
            asr = ""
            
            #length of new list
            length = len(final_list)

            for a in range(length): #loop through new list by index
                if(final_list[a] != ""):
                    if(a == vid_codec_idx): #get the vcodec
                        vcodec = final_list[a]

                if(a == length-1):#run this upon last index 
                    count = 0
                    not_info = False
                    
                    while(True):
                        if(count == 0):
                            acodec_matcher = re.match(acodec_pattern, final_list[a-count])
                            if(acodec_matcher!=None):
                                acodec = final_list[a-count]
                                vbr = final_list[a-count-1]
                                not_info = True
                                break

                            more_info += final_list[a-count]

                            count+=1
                            continue
                        
                        if(not not_info):
                            more_info_matcher = re.match(more_info_pattern, final_list[a-count])
                            
                            if(more_info_matcher != None):
                                more_info = final_list[a-count] + " " + more_info
                            else:
                                asr = final_list[a-count]
                                abr = final_list[a-count-1]
                                count+=2
                                not_info = True
                        
                        acodec_matcher = re.match(acodec_pattern, final_list[a-count])
                        if(acodec_matcher != None):
                            acodec = final_list[a-count]
                            vbr =  final_list[a-count-1]
                            break

                        if(count == length-1):
                            break

                        count+=1
            
            #return final_list

            if(more_info == ""):
                self.editable_text = ""
            else:
                self.editable_text = self.editable_text + ", Video:" + vcodec + "\v, Audio:" + acodec + ", SampleRate:" + asr + ", BitRate:" + abr  + ", Info:" + more_info
            
            #return([vcodec, vbr, acodec, abr, asr, more_info])
