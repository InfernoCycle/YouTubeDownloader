import subprocess
from subprocess import PIPE

from widgets.main_widget import MainWidget
from PySide2 import QtWidgets
import sys


#available audio formats:
#(3gp, aac, flv, m4a, mp3, mp4, ogg, wav, webm)

#available video formats:
#(avi, flv, gif, mkv, mov, mp4, webm, aac, aiff, alac,
# flac, m4a, mka, mp3, ogg, opus, vorbis,
# wav)

if (__name__ == "__main__"):
    app = QtWidgets.QApplication([])
    
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())
    """
    app = CTk()
    
    main = App(app)
    
    app.mainloop()
    """

#process = subprocess.Popen(["cmd.exe", "/c", "yt-dlp", "-w", "-F", "https://www.youtube.com/watch?v=zIz85dwehIg&ab_channel=%E7%B7%8B%E6%9C%88"], stdout=PIPE, encoding="UTF-8")


#print(process.stdout.read())
"""

is_audio_only = input("Enter audio_only? (y/n): ")
file_format = input("Enter format (mp3, mp4, ogg, wav): ")

process = None

if(is_audio_only == "y"):
    process = subprocess.Popen(["cmd.exe", "/c", "yt-dlp", "-w", "-x", "--audio-format", file_format, "-o", "'%(title)s.%(ext)s'", "https://www.youtube.com/watch?v=tFOoq2oOTJU&ab_channel=%E8%94%A1%E5%AE%9C%E7%9C%9F"], stdout=PIPE, encoding="UTF-8")
else:
    process = subprocess.Popen(["cmd.exe", "/c", "yt-dlp", "-w", "-f", file_format, "-o", "'%(title)s.%(ext)s'", "https://www.youtube.com/watch?v=tFOoq2oOTJU&ab_channel=%E8%94%A1%E5%AE%9C%E7%9C%9F"], stdout=PIPE, encoding="UTF-8")

print(process.stdout.read())
"""
