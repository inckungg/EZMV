import youtube_dl   # Youtube downloader
import numpy as np
from PIL import Image
from colorthief import ColorThief
import subprocess   # Working on batch
import ffmpeg       # Video concat / Trim
import scenedetect  # Detecting scene changes
import time         # Changing duration format
import os           # Deleting files
import shutil
from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
from os import path # Changing directory
from pychorus import find_and_output_chorus # Finding song's chorus
from subprocess import  check_output, CalledProcessError, STDOUT

def getDuration(filename):

    command = [
        'ffprobe', 
        '-v', 
        'error', 
        '-show_entries', 
        'format=duration', 
        '-of', 
        'default=noprint_wrappers=1:nokey=1', 
        filename
      ]

    try:
        output = check_output( command, stderr=STDOUT ).decode()
    except CalledProcessError as e:
        output = e.output.decode()

    return int(float(output))


def find_scenes(video_path, threshold=25.0):
    # Create our video & scene managers, then add the detector.
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold))

    # Base timestamp at frame 0 (required to obtain the scene list).
    base_timecode = video_manager.get_base_timecode()

    # Improve processing speed by downscaling before processing.
    video_manager.set_downscale_factor()

    # Start the video manager and perform the scene detection.
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    # Each returned scene is a tuple of the (start, end) timecode.
    return scene_manager.get_scene_list(base_timecode)


def main_cut(URL):
    ydl_opts = {
    'format': '137',
    'nocheckcertificate': True,
    'restrictfilenames': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(URL, download=False)
        video = result['entries'][0] if 'entries' in result else result

    print(video)
    # url = video['url']
    title = video['title']
    duration_sec = video['duration']
    if duration_sec >= 480:
        print("Video longer than 6 minutes is not recommended.")
        exit()
    elif duration_sec <= 120:
        print("Video shorter than 2 minutes is not recommended.")
        exit()

    trim_1 = time.strftime('%H:%M:%S', time.gmtime(((duration_sec // 3) * 1) - 30))
    trim_2 = time.strftime('%H:%M:%S', time.gmtime(((duration_sec // 3) * 2) - 30))
    trim_3 = time.strftime('%H:%M:%S', time.gmtime(((duration_sec // 3) * 3) - 30))
    trim_section = [trim_1,trim_2,trim_3]
    duration = time.strftime('%H:%M:%S', time.gmtime(duration_sec))

    print(title)
    print("Video duration: ",duration)
    print(trim_section)
    TARGET = r"mv.mp4"
    # FIX ISSUE
    subprocess.call('youtube-dl -f 137 --no-check-certificate -o "%s" "%s"' %(TARGET, URL), shell=True)
    # subprocess.call('ffmpeg -i "%s" -c:v copy -c:a copy "%s"' % (surl, TARGET))

    for trim_portion in trim_section:
        FROM = trim_portion
        TIME = "00:00:10"
        TARGET_TRIM = r"trim{}.mp4".format(trim_section.index(trim_portion) + 1)

        # TRIM 1
        subprocess.call('ffmpeg -i "%s" -ss %s -t %s -c:v copy -c:a copy "%s"' % (TARGET, FROM, TIME, TARGET_TRIM), shell=True)
        # TRIM 2
        scenes = find_scenes(TARGET_TRIM)
        print("======== VIDEO {}'s cutting analysis ========".format(trim_section.index(trim_portion) + 1))
        print(scenes)

        try:
            print("2nd scene starts from: ", scenes[1][0])
            scene_float = float(scenes[1][0])

            if scene_float >= 0.5:
                CUT_FROM_CON = False
                CUT_FROM = scenes[0][0]
                CUT_FROM += 3
            else:
                CUT_FROM_CON = True
                CUT_FROM = scenes[1][0]
                CUT_FROM += 3

            print("Last scene ends at: ", scenes[-1][0])
            scene_float_2 = float(scenes[-1][0])

            if scene_float_2 >= 9:
                CUT_END_CON = True
                CUT_END = scenes[-2][1]
                CUT_END -= 3
            else:
                CUT_END_CON = False
                CUT_END = scenes[-1][0]
                CUT_END -= 3

        except IndexError:
            CUT_FROM_CON = False
            CUT_FROM = scenes[0][0]
            CUT_END_CON = False
            CUT_END = scenes[-1][0]

        print("Cutting starts from: ", CUT_FROM)
        print("Cutting ends at: ", CUT_END)

        TARGET_TRIM_2 = r"file{}.mp4".format(trim_section.index(trim_portion) + 1)
        if CUT_FROM == CUT_END:
            print("CUT CONDITION 0")
            subprocess.call('ffmpeg -i "%s" -c:v copy -c:a copy "%s"' % (TARGET_TRIM, TARGET_TRIM_2), shell=True)
        else:
            if CUT_FROM_CON == False and CUT_END_CON == False:
                print("CUT CONDITION 1")
            elif CUT_FROM_CON == False and CUT_END_CON != False:
                print("CUT CONDITION 2")
            elif CUT_FROM_CON != False and CUT_END_CON == False:
                print("CUT CONDITION 3")
            elif CUT_FROM_CON != False and CUT_END_CON != False:
                print("CUT CONDITION 4")
            subprocess.call('ffmpeg -i "%s" -ss %s -to %s -c:v copy -c:a copy "%s"' % (TARGET_TRIM, CUT_FROM, CUT_END, TARGET_TRIM_2), shell=True)


def audio_cut(URL):
    AUDIO_TARGET = r"audio.mp4"
    AUDIO_CONVERT = r"audio_convert.mp3"
    AUDIO_CHORUS = r"audio_chorus.wav"
    CLIP_LENGTH = getDuration(r"merged.mp4")
    print("Merged Clip's length: ", CLIP_LENGTH)
    ydl_opts = {
    'format': 'best',
    'nocheckcertificate': True,
    'restrictfilenames': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(URL, download=False)
            video = result['entries'][0] if 'entries' in result else result

    # url = video['url']
    # FIX ISSUE
    subprocess.call('youtube-dl -f best --no-check-certificate -o "%s" "%s"' %(AUDIO_TARGET, URL), shell=True)
    # subprocess.call('ffmpeg -i "%s" -c:v copy -c:a copy "%s"' % (url, AUDIO_TARGET))
    subprocess.call('ffmpeg -i "%s" -f mp3 "%s"' % (AUDIO_TARGET, AUDIO_CONVERT), shell=True)
    chorus_start_sec = find_and_output_chorus(AUDIO_CONVERT, AUDIO_CHORUS, CLIP_LENGTH)
    print(chorus_start_sec)


def remove_unused_magic_cut():
    os.remove("trim1.mp4")
    os.remove("trim2.mp4")
    os.remove("trim3.mp4")
    os.remove("file1.mp4")
    os.remove("file2.mp4")
    os.remove("file3.mp4")
    os.remove("audio_convert.mp3")
    os.remove("audio_chorus.wav")
    os.remove("audio_final.wav")
    os.remove("audio.mp4")
    os.remove("merged.mp4")
    os.remove("faded.mp4")
    os.remove("mv.mp4")
    os.remove("mylist.txt")
    os.remove("concat.bat")
    os.remove("concat.sh")
    try:
        os.remove("mylist.txt")
    except FileNotFoundError:
        pass


def remove_unused_color_palette():
    try:
        os.remove("thumbnail.jpg")
    except FileNotFoundError:
        os.remove("thumbnail.webp")
    os.remove("palette_h.jpg")
    os.remove("palette_v.jpg")
    os.remove("concat.bat")
    os.remove("concat.sh")
    
def magic_cut(URL):
    new_folder(URL)
    main_cut(URL)

    time.sleep(3)
    # Merging videos
    subprocess.call([r"concat.bat"], shell=True)
    try:
        MERGED_LENGTH = getDuration(r"merged.mp4")
    except ValueError:
        time.sleep(1)
        subprocess.call('bash concat.sh', shell=True)
        MERGED_LENGTH = getDuration(r"merged.mp4")
    MERGED_FRAME = (MERGED_LENGTH - 1) * 24
    time.sleep(2)
    subprocess.call('ffmpeg -y -i merged.mp4 -vf fade=out:%i:24 -acodec copy faded.mp4' % (MERGED_FRAME), shell=True)

    time.sleep(2)
    # finding chorus
    audio_cut(URL)

    time.sleep(2)
    # fading audio
    AUDIO_PREFADE = r"audio_chorus.wav"
    AUDIO_FINAL = r"audio_final.wav"
    subprocess.call('ffmpeg -i "%s" -filter_complex "afade=d=1.0, areverse, afade=d=1.0, areverse" "%s"' % (AUDIO_PREFADE, AUDIO_FINAL), shell=True)

    time.sleep(2)
    # merge video + audio
    VIDEO_PREMIX = r"faded.mp4"
    AUDIO_PREMIX = r"audio_final.wav"
    FINAL_OUTPUT = r"Final_Output.mp4"
    subprocess.call('ffmpeg -i "%s" -i "%s" -c:v copy -c:a aac "%s"' % (VIDEO_PREMIX, AUDIO_PREMIX, FINAL_OUTPUT), shell=True)

    time.sleep(2)
    #Delete files
    remove_unused_magic_cut()
    exit()

def palette_h(img1, img2, img3, img4, img5):
    totalwidth = img1.width + img2.width + img3.width + img4.width + img5.width
    concatimg = Image.new('RGB', (totalwidth, img1.height))
    concatimg.paste(img1, (0, 0))
    imglist = [img1, img2, img3, img4, img5]
    pasted = 0
    for img in imglist:
        concatimg.paste(img, (img1.width * pasted, 0))
        pasted += 1
    return concatimg

def palette_v(img1, img2, img3, img4, img5):
    totalheight = img1.height + img2.height + img3.height + img4.height + img5.height
    concatimg = Image.new('RGB', (img1.width, totalheight))
    concatimg.paste(img1, (0, 0))
    imglist = [img1, img2, img3, img4, img5]
    pasted = 0
    for img in imglist:
        concatimg.paste(img, (0, img1.height * pasted))
        pasted += 1
    return concatimg

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def color_palette(URL):
    new_folder(URL)
    thumbnail_name = r"thumbnail.jpg"
    thumbnail_name_webp = r"thumbnail.webp"
    subprocess.call('youtube-dl --write-thumbnail --skip-download --no-check-certificate -q -o "%s" "%s"'% (thumbnail_name, URL), shell=True)
    try:
        target_thumbnail = ColorThief(thumbnail_name)
    except FileNotFoundError:
        target_thumbnail = ColorThief(thumbnail_name_webp)
        
    palette = target_thumbnail.get_palette(color_count=5)
    print(palette)
    hexcode1 = '#%02x%02x%02x' % (palette[0])
    hexcode2 = '#%02x%02x%02x' % (palette[1])
    hexcode3 = '#%02x%02x%02x' % (palette[2])
    hexcode4 = '#%02x%02x%02x' % (palette[3])
    hexcode5 = '#%02x%02x%02x' % (palette[4])
    hexarr = [hexcode1, hexcode2, hexcode3, hexcode4, hexcode5]

    colorimg1 = Image.new('RGB', (256, 144), palette[0])
    colorimg2 = Image.new('RGB', (256, 144), palette[1])
    colorimg3 = Image.new('RGB', (256, 144), palette[2])
    colorimg4 = Image.new('RGB', (256, 144), palette[3])
    colorimg5 = Image.new('RGB', (256, 144), palette[4])

    palette_h(colorimg1, colorimg2, colorimg3, colorimg4, colorimg5,).save('palette_h.jpg')
    palette_v(colorimg1, colorimg2, colorimg3, colorimg4, colorimg5,).save('palette_v.jpg')

    try:
        imgthumbnail = Image.open(thumbnail_name)
    except FileNotFoundError:
        imgthumbnail = Image.open(thumbnail_name_webp)

    imgpalette_h = Image.open('palette_h.jpg')
    imgpalette_v = Image.open('palette_v.jpg')

    get_concat_v(imgthumbnail, imgpalette_h).save('thumbnail_palette_h.jpg')
    get_concat_h(imgthumbnail, imgpalette_v).save('thumbnail_palette_v.jpg')

    time.sleep(2)
    with open('Color Code.txt', 'w+') as f:
        f.write("RGB Code: \n")
        for color in palette:
            f.write("%s\n" % str(color))
        f.write("\nHex Code: \n")
        for hexcode in hexarr:
            f.write("%s\n" % hexcode)
    remove_unused_color_palette()
    exit()

def new_folder(URL):
    substring = "watch?"
    if substring in URL:
        URLname = URL.split("=")
        URLname2 = URLname[1]
        URLname3 = URLname2.split("&")
        URLname4 = URLname3[0]
        pathname = URLname4
    else:
        URLname = URL.split("/")
        pathname = URLname[-1]
    print("PATH = ", pathname)
    try:
        os.makedirs(pathname)
    except FileExistsError:
        pass
    shutil.copy2('concat.bat', pathname)
    shutil.copy2('concat.sh', pathname)
    os.chdir(pathname)
    workdir = os.getcwd()
    print ("Saving to: ",workdir)

if __name__ == "__main__":
    print("======== EZMV HIGHLIGHT ========")
    URL = input("Enter valid Youtube's URL: ")  # Take URL from user
    # Select trimming style
    print(":: 1 : Magic cut")
    print(":: 2 : Color Palatte")
    while True:
        style = input("Please enter style (1-2): ") or "0"
        if style == "1":
            magic_cut(URL)
        elif style == "2":
            color_palette(URL)
        else:
            pass
