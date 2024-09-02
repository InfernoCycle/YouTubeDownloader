<div align="center">
  
[![yttomp3](https://raw.githubusercontent.com/InfernoCycle/TrueYTtoMP3/main/assets/.github/generated-1785fb59b35d01e34f76f4e174244d14ddeccadb4ad7bf5dd5ee7e4f42fcb211-7.jpg)](#readme)

</div>

TrueYTtoMP3/Crossfield is a simple downloader for YouTube videos into the format you want. Unlike online downloaders, this one doesn't include ads and is completely free to use.

* [Installations](#installations)
  * [Releases](#releases)
* [Getting Started](#getting-started)
* [Usage](#usage)
  * [URLs](#urls)
  * [Available Formats](#available-formats)
  * [Download Location](#download-location)
  * [Naming Files](#naming-files)
  * [Media Options](#media-options)
* [Version](#version)
* [Things To Know](#things-to-know)
  * [First Time Running The Application](#first-time-running-the-application)
  * [Differences between Version 1.1.0 and 2.0.0](#differences-between-version-110-and-200)
  * [Choosing Correct Video and Audio Options in Formats Tab](#choosing-correct-video-and-audio-options-in-formats-tab)
  * [Defaults](#defaults)
  * [Config and Log Files](#config-and-log-files)
  * [Future Operating System Support](#future-operating-system-support)
  * [Delayed Downloads and Failure of Downloads](#delayed-downloads-and-failure-of-downloads)
  * [Bugs and Future Updates](#bugs-and-future-updates)
  * [Disclaimer](#disclaimer)
* [Sources Used](#sources-used)

# Installations
There are only window releases for this program. There will be future updates for linux users someday.

## Releases
Available downloads for the application.

#### Zips

File|Description
:---|:---
[CrossfieldPlus](https://github.com/InfernoCycle/TrueYTtoMP3/releases/download/v2.0.1/CrossfieldPlus.zip)|Download zip for Windows 10 and 11. (ffmpeg and ffprobe included Uses Pyside6)
[Crossfield](https://github.com/InfernoCycle/TrueYTtoMP3/releases/download/v1.1.1/Crossfield.zip)|Download zip for Windows 8 and up. (ffmpeg and ffprobe included. Uses PySide2)

# Getting Started
Unzip either the 'CrossfieldPlus' or 'Crossfield' zip file and leave the contents inside where they are in the unzipped folder. You can either run the `CrossfieldPlus.exe` or `Crossfield.exe` file directly or create a shortcut to put anywhere on your computer.


# Usage
How to use the program.

* [URLs](#urls)
* [Available Formats](#available-formats)
* [Download Location](#download-location)
* [Naming Files](#naming-files)
* [Media Options](#media-options)

## URLs

Multiple URL's can be entered as long as they are seperated by a comma.

    url1, ur2, url3, etc

![image](https://github.com/user-attachments/assets/68e6b71d-34d8-41d0-bbec-52365ad8ee68)


## Available Formats
Available formats include:

- Audio: `aac, alac, flac, m4a, mp3, opus, wav, ogg`
- Video: `avi, flv, mkv, mov, mp4, webm, 3gp`

![image](https://github.com/user-attachments/assets/c8e3c7e5-b858-4e19-95c6-7688939c33da)


> [!NOTE]
> All formats can be found on yt-dlp postprocessor ffmpeg [page](https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/postprocessor/ffmpeg.py).

## Download Location

By default the download location will be the current directory of the executable file.
![image](https://github.com/user-attachments/assets/cbc9f9c5-da4c-49d7-9001-1f7c8e8f89df)

- You can change the default download location by clicking the button next to the location textbox.

## Naming Files

You can name each file that is downloaded in the 'Name' tab by seperating each name by a comma.

    name1, name2, name3, etc

![image](https://github.com/user-attachments/assets/95029d8e-062a-4abf-aeda-d9269ba14a9f)


> [!NOTE]
> If there are more url's/downloads than names entered, then the filename will default to the video title.

## Media Options
You can choose what type of quality video and audio you want before downloading the file in the 'Formats' tab.

Video Options Example:
![image](https://github.com/user-attachments/assets/32cc6200-6725-41df-b619-6e5a9cabaa30)

Audio Options Example:
![image](https://github.com/user-attachments/assets/02281399-b0ad-4524-9743-f5a409632db4)


#### Important Notes for choosing options 
- You will have to generate the available formats by clicking the 'Search' button on the side of the 'Formats' tab.

- The options that appear are the ones from the first successful URL and will only apply to the first downloaded file by default while the rest of the downloads will use default options.

- When a user chooses 'All that apply', the same options will be applied to all subsequent downloads. If the option is unavailable for that particular download then the default options will be applied to those downloads.

- Options cannot be changed while files are being downloaded. You will have to either cancel the next downloads or wait for all downloads to finish. 


# Version
- Version 2.0.1 (For Windows 10 and 11)
- Version 1.1.1 (For Windows 8 and Up)

# Things To Know
Some important things to know when using the application.

## First Time Running The Application
The first few times you run this application, please be ready to wait at least 2 to 3 minutes for it to open. This should not happen too many times after using the program.

## Differences between Version 1.1.0 and 2.0.0
- 1.1.0 uses PySide2 as the GUI framework while 2.0.0 uses PySide6
- 1.1.0 supports Windows 8 and up while 2.0.0 supports Windows 10 and 11
- I will focus more on the 2.0.0 version as more and more user's switch to newer operating systems.

## Choosing Correct Video and Audio Options in Formats Tab
- There are different options that can appear after searching for available formats. Please pay special attention that you choose a format that is supported on your system. There are different video codecs (vcodec value) that may appear which may begin with "vp", "avc", "av01", and any other codec available as shown below (av01 not shown).

![image](https://github.com/user-attachments/assets/68e47ad3-82c7-47b9-a267-eb921af055b0)

- From some testing, I found that formats with a codec starting with "avc" were more likely to be supported than formats with codecs starting with "vp", and "av01". I am by no means an expert on codecs and their differences so please try out what is best.

- As for Audio formats, there has been no known issues (yet) in choosing any option.

> [!NOTE]
> For more information on codecs, visit [this page](https://getstream.io/glossary/video-codecs/).

## Defaults
Here are a list of the actual values being used that are not seen

### Audio and Video Format
- Video default yt-dlp format value when using "Regular" is "**bv[vcodec\*=avc]**"
- Audio default yt-dlp format value when using "Regular" is "**140**" or "**139**"

### Extension Option
- The default extension value upon starting the application is always "mp4".

### Save Location
- The default save location when first starting the application or not changing the location is the directory the application's exe file is located.

### File Name
- Default filename is the title of the video unless otherwise stated.

## Config and Log Files
- The config and log files are located in the "**_internal**" directory in the same folder as the application's exe and are named "**settings.json**" and "**log.txt**" respectively.

## Future Operating System Support
- I have no idea when I will add support for systems other than Windows. There is a chance however.

## Delayed Downloads and Failure of Downloads
- There is a default delay between downloads set to 5 seconds to avoid getting IP banned.
- Sometimes downloads will fail due to an invalid URL or the page itself is down or it can also mean you were banned from downloading from that page due to excessive downloads.
- Please be careful when downloading too much and limit downloads to at most 10 a day.

## Bugs and Future Updates
- There has been reports where the progress bar will freeze even after a download has finished. A fix is in the works.
- Progress bar may also reach 100% despite a download actually failing.
- Future Update: I've been looking into creating a tab to convert files into user's desired format. (October)
- Future Update: Tab to send downloads to your desired computer location or email as long as another mini receiver I will make is installed and running. (December)

## Disclaimer
I am not responsible for any IP bans or copyright crimes that a user may incur with the use of this product.

# Sources Used
1. [ffmpeg and ffprobe](https://www.ffmpeg.org/)
2. [yt-dlp](https://github.com/yt-dlp/yt-dlp)
3. [python](https://www.python.org/downloads/)
