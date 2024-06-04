import random
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import BooleanVar, IntVar, StringVar, Tk, ttk, Radiobutton, filedialog
import time
import threading
import asyncio
import sys

class YT_dl_toMP3(tk.Tk):
  def __init__(self, master) -> None:
    self.master = master
    self.master.title("YT to MP3 Convertor")
    self.master.geometry("600x350")
    self.master.maxsize(700, 540)
    self.master.minsize(550, 330)
    self.master.grid_columnconfigure([0], weight=1)
    self.master.grid_rowconfigure([0,1,2], weight=1)
    self.url = ""
    self.endDownload = False
    
    self.MainPage()

  def MainPage(self):
    #if(self.active.json()["active"]):
    for i in self.master.winfo_children():
      i.destroy()

    def cancel():
      cancelled.set(True)
      
    
    def progress(Delay):
      constantUpdate = 10
      updateAmount = random.randint(0,10)
      divideDelay = 100
      for i in range(int(400/constantUpdate)):
        if Pb["value"] < 100:      
          Pb["value"] += random.randint(0,10)
          ProgressLabel["text"] = str(Pb["value"]) + "%"
          time.sleep(Delay/divideDelay)
        else:
          ProgressLabel["text"] = "Completed"
          SubmitButton.config(state=tk.NORMAL)
          return
    
    def resetProgress():
      Pb["value"] = 0
      ProgressLabel["text"] = ""
    
    def Start():
      ErrorLabel.config(text="", foreground="red",  font=("Times New Roman", 0))
      if(Directory.get() == ""):
        ErrorLabel.config(text="Please enter a directory.", foreground="red",  font=("Times New Roman", 15))
        return
      
      video_url = InputURL.get("1.0", tk.END)
      #Link to use: https://www.youtube.com/watch?v=E8owWw1OaNM&ab_channel=NightTempo
      resetProgress()
      retainVid = bool()
      FormatType = ""
      QualityFormat = ""
      video_info = ""

      if(video_url != "" and (video_url.find("youtube")!= -1 or video_url.find("youtu.be") != -1) and Option1.get() != 0):
        SubmitButton.config(state=tk.DISABLED)
        CancelButton.config(state=tk.NORMAL)
        ProgressLabel["text"] = "Beginning Download"
        #video_url = input("YouTube Video URL: ")
        with YoutubeDL({}) as ydl:
          try:
            video_info = ydl.extract_info(video_url, download=False)
          except:
            SubmitButton.config(state=tk.NORMAL)
            ErrorLabel.config(text="Error Occurred Downloading Video", foreground="red",  font=("Times New Roman", 15))
            ProgressLabel["text"] = ""
            return
        #video_info = youtube_dl.YoutubeDL().extract_info(url=str(video_url).strip(), download=False)

        if(Option1.get() == 1):
          FormatType = "mp3"
          retainVid = False
          QualityFormat = "bestaudio/best"
        elif(Option1.get() == 2):
          FormatType = "mp4"
          retainVid = True
          QualityFormat = "best"
        elif(Option1.get() == 3):
          FormatType = "ogg"
          retainVid = False
          QualityFormat = "bestaudio"
        elif(Option1.get() == 4):
          FormatType = "wav"
          retainVid = False
          QualityFormat = "bestaudio"
        else:
          SubmitButton.config(state=tk.NORMAL)
          CancelButton.config(state=tk.DISABLED)
          ProgressLabel["text"] = "Download Cancelled problem with Formatting"

        #filename = f"{video_info['title']}.{FormatType}" #format type has to be mp3 or mp4
        filename = f"something{random.randint(0,10000)}.{FormatType}"
        """
        """
        options={
          'format': FormatType, #has to be mp3 or mp4
          'keepvideo': retainVid, #has to be True or False
          'outtmpl': filename,
          'limit':5,
        }
        """
        """
        #outtmpl: 'C:/Songs/%(title)s.'+FormatType
        ydl_opts = {
          'format': QualityFormat,
          'outtmpl': Directory.get()+'/%(title)s.'+FormatType,
          'postprocessors': [{
              'key': 'FFmpegExtractAudio',
              'preferredcodec': FormatType,
              'preferredquality': '192',
          }]
        }

        #asyncio.create_task(Process(video_info, ydl_opts, filename))
        """
        x = threading.Thread(target=Process(video_info, ydl_opts, filename))
        x.start()
        x.join()
        """
        Process(video_info, ydl_opts, filename, video_url)
      else:   
        ProgressLabel["text"] = "Nothing or an invalid URL was entered."
    
    def checkCancel():
      while True:
        if(endOfProgram.get()):
          endOfProgram.set(False)
          break
        if(cancelled.get()):
          cancelled.set(False)
          sys.exit()
    
    async def download(video_info, options, filename, url):
      with YoutubeDL(options) as ydl:
        try:
          ydl.download([url])
        except KeyError as error:
          endOfProgram.set(True)
          #print("Key Error: " + str(error))
          SubmitButton.config(state="normal")
          CancelButton.config(state="disabled")
          ProgressLabel["text"] = "Download Complete"
      """
      with youtube_dl.YoutubeDL(options) as ydl:
        try:
          ydl.download([video_info['webpage_url']])
        except youtube_dl.utils.DownloadError:
          SubmitButton.config(state="normal")
          CancelButton.config(state="disabled")
          ProgressLabel["text"] = "A problem occured while downloading"
      """

    async def main(video_info, options, filename, video_url):
      x = threading.Thread(target=checkCancel)
      x.start()
      await asyncio.gather(download(video_info, options, filename, video_url))
      
    def startDownload(video_info, options, filename, video_url):
      asyncio.run(main(video_info, options, filename, video_url))
      #with youtube_dl.YoutubeDL(options) as ydl:
      # ydl.download([video_info['webpage_url']])             
        
    def Process(video_info, options, filename, video_url):
      beg = time.perf_counter()
      """
      y = threading.Thread(target = startDownload, args=(video_info, options, filename))
      y.start()
      y.join()
      """
      startDownload(video_info, options, filename, video_url)
      end = time.perf_counter()
      ProgressLabel["text"] = "Download Completed"
      progress(end-beg)
      
      print(f"Download Complete... {filename}")
      endOfProgram.set(True)
      CancelButton.config(state=tk.DISABLED)
    

    def getDir():
      InputFileLocation.config(state="normal")
      directory = filedialog.askdirectory()
      Directory.set(directory)
      InputFileLocation.delete("1.0", tk.END)
      InputFileLocation.insert("1.0", str(directory))
      ErrorLabel.config(text="", foreground="black",  font=("Times New Roman", 0))
      InputFileLocation.config(state="disable")
      
    #Var Variables
    cancelled = BooleanVar(self.master, value=False)
    endOfProgram = BooleanVar(self.master, value=False)
    Directory = StringVar(self.master, value="")
    
    MainPanel = tk.Frame(self.master)
    MainPanel.grid_columnconfigure([0,1], weight=1)
    MainPanel.grid_rowconfigure([0,1,2,3,4], weight=1)

    TitlePanel = tk.Frame(MainPanel)
    TitlePanel.grid_columnconfigure([0], weight=1)
    Title = tk.Label(TitlePanel, text="Convert to MP3/MP4", font=("Times New Roman", 20, "bold"))

    RadioPanel = tk.Frame(MainPanel)

    global Option1
    Option1 = IntVar(RadioPanel, value=1)
    RadioPanel.grid_columnconfigure([0,1], weight=1)
    Mp3Radio = Radiobutton(RadioPanel,text="MP3", variable=Option1, value=1)
    Mp4Radio = Radiobutton(RadioPanel, text="MP4", variable=Option1, value=2)
    OggRadio = Radiobutton(RadioPanel, text="Ogg", variable=Option1, value=3)
    WavRadio = Radiobutton(RadioPanel, text="Wav", variable=Option1, value=4)
    
    InputPanel = tk.Frame(MainPanel)
    InputPanel.grid_columnconfigure([0,1,2], weight=1)
    InputPanel.grid_rowconfigure([0,1,2], weight=1)
    InputLabel = tk.Label(InputPanel, text="URL: ")
    InputURL = tk.Text(InputPanel, width=50, height=2, font=("Times New Roman", 15))

    InputFileLabel = tk.Label(InputPanel, text="Location: ")
    InputFileLocation = tk.Text(InputPanel, width=50, height=1)
    InputFileLocation.config(state="disable")
    InputFileButton = tk.Button(InputPanel, text="...", width=10, command=lambda:getDir())

    ErrorLabel = tk.Label(InputPanel, text="", height=0,font=("Times New Roman", 0))

    ProgressPanel = tk.Frame(MainPanel)
    ProgressPanel.grid_columnconfigure([0,1], weight=1)
    Pb = ttk.Progressbar(ProgressPanel,
                        orient="horizontal",
                        mode="determinate",
                        length=400)
    ProgressLabel = tk.Label(ProgressPanel, text="")
    
    SubmitPanel = tk.Frame(MainPanel)
    SubmitPanel.grid_columnconfigure([0], weight=1)
    SubmitButton = tk.Button(SubmitPanel, text="Download", command=lambda:threading.Thread(target=Start).start())
    CancelButton = tk.Button(SubmitPanel, text="Cancel", state=tk.DISABLED, command=lambda:cancel())

    Title.grid(row=0, column=0, sticky="n")
    TitlePanel.grid(row=0, column=0, pady=10)

    Mp3Radio.grid(row=0, column=0)
    Mp4Radio.grid(row=0, column=1)
    OggRadio.grid(row=0, column=2)
    WavRadio.grid(row=0, column=3)
    RadioPanel.grid(row=1, column=0, pady=10)

    InputLabel.grid(row=0, column=0, sticky="w")
    InputURL.grid(row=0, column=1, columnspan=2, sticky="e")
    InputFileLabel.grid(row=1, column=0, pady=(10,0))
    InputFileLocation.grid(row=1,column=1, pady=(10,0))
    InputFileButton.grid(row=1, column=2, pady=(10,0))
    ErrorLabel.grid(row=2, column=0, columnspan=3, pady=0)
    InputPanel.grid(row=2, column=0, pady=(10, 1))

    Pb.grid(row=0, column=0)
    ProgressLabel.grid(row=1, column=0)
    ProgressPanel.grid(row=3, column=0, pady=10)
  
    SubmitButton.grid(row=0, column=0)
    CancelButton.grid(row=0, column=1, padx=20)
    SubmitPanel.grid(row=4, column=0, pady=10)

    MainPanel.grid(row=0, column=0)

if __name__ == "__main__":
  root = Tk()
  YT_dl_toMP3(root)
  root.mainloop()