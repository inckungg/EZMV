== EZMV Highlight Maker ==
Ronnakrit Yuankrathok (623040195-3)
Pawarut Butryojantho (623040693-7)
This project is part of EN842004, EN842005 (2020/1)
UI DEMO: https://drive.google.com/file/d/1MYfLIenpmh0Emqz5BxQmUb4AiZKqD-6B/view?usp=sharing
OUTPUT DEMO: https://drive.google.com/drive/folders/1Vn3jWAlzZqgr_69FpyDnfVEEJS2SK8TE?usp=sharing


== Required Packages/Modules ==

1. Python 3.6+

2. ffmpeg 
## MacOS
--> brew install ffmpeg
## if homebrew isn't installed yet.
--> pip install homebrew

## Windows
## Download within given link below.
--> https://ffmpeg.org/download.html
## Installation guide (Static build)
https://www.wikihow.com/Install-FFmpeg-on-Windows

3. Listed module in requirements.txt
--> pip install -r requirements.txt


== Run ==

Start.py


== Tested on ==

Window10 64bits
macOS Catalina 10.15.6
(Most recent: 6 DEC 2020)


== Known Issue ==

magic_cut() - Doesn't work with Video less than 1080p
            - Video with unique cut and frames freeze won't work well.

color_palette() - Doesn't work with Thumbnail less than 1280x720


====
