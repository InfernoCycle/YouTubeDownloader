<div align="center">
  
[![yttomp3](https://raw.githubusercontent.com/InfernoCycle/TrueYTtoMP3/main/assets/.github/generated-1785fb59b35d01e34f76f4e174244d14ddeccadb4ad7bf5dd5ee7e4f42fcb211-7.jpg)](#readme)

</div>

TrueYTtoMP3/Crossfield is a simple downloader for YouTube videos into the format you want. Unlike online downloaders, this one doesn't include ads and is completely free to use.

* [Installations](#installations)
  * [Releases](#releases)
* [Usage](#usage)
  * [URLs](#urls)
  * [Available Formats](#available-formats)
  * [Download Location](#download-location)
  * [Naming Files](#naming-files)
  * [Media Options](#media-options)
* [Version](#version)
* [Things To Know](#things-to-know)

# Installations
There are only window releases for this program. There will be future updates for linux users someday.

## Releases
Available downloads for the application.

#### Zips

File|Description
:---|:---
[CrossfieldPlus](https://github.com/InfernoCycle/TrueYTtoMP3/releases/tag/v2.0.0)|Download zip for Windows 10 and 11. (ffmpeg and ffprobe included Uses Pyside6)
[Crossfield](https://github.com/InfernoCycle/TrueYTtoMP3/releases/tag/v1.1.0)|Download zip for Windows 8 and up. (ffmpeg and ffprobe included. Uses PySide2)

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

## Available Formats
Available formats include:

- Audio: `aac, alac, flac, m4a, mp3, opus, wav, ogg`
- Video: `avi, flv, mkv, mov, mp4, webm, 3gp`

> [!NOTE]
> All formats can be found on yt-dlp postprocessor ffmpeg [page](https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/postprocessor/ffmpeg.py).

## Download Location

By default the download location will be the current directory of the executable file.
![image](https://github.com/user-attachments/assets/cbc9f9c5-da4c-49d7-9001-1f7c8e8f89df)

- You can change the default download location by clicking the button next to the location textbox.

## Naming Files

You can name each file that is downloaded in the 'Name' tab by seperating each name by a comma.

    name1, name2, name3, etc

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
- Version 2.0.0 (For Windows 10 and 11)
- Version 1.1.0 (For Windows 7 and Up)

# Things To Know
Some important things to know when using the application.

## First Time Running The Application
The first few times you run this application, please be ready to wait at least 2 to 3 minutes for it to open. This should not happen too many times after using the program.

## Differences between Version 1.1.0 and 2.0.0
- 1.1.0 uses PySide2 as the GUI framework while 2.0.0 uses PySide6
- 1.1.0 supports Windows 7 and up while 2.0.0 supports Windows 10 and 11
- I will focus more on the 2.0.0 version as more and more user's switch to newer operating systems.

## Future Operating System Support
- I have no idea when I will add support for systems other than Windows. There is a chance however.

## Failure of Downloads
- Sometimes downloads will fail due to an invalid URL or the page itself is down or it can also mean you were banned from downloading from that page due to excessive downloads.
- Please be careful when downloading too much and limit downloads to at most 10 a day.

## Delayed Downloads
- There is a default delay between downloads set to 5 seconds to avoid getting IP banned.

## Bugs and Future Updates
- There has been reports where the progress bar will freeze even after a download has finished. A fix is in the works.

## Disclaimer
I am not responsible for any IP bans or copyright crimes that a user may incur with the use of this product.
