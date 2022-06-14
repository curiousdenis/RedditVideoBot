import random
from console import print_substep, print_step,print_markdown
from pathlib import Path
import yt_dlp
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# here start - is a random number between (3 minutes to (3660 - voice_time))-> main point is that it is a random num
# end - equals to start + voice_time -> main point is it is a random + voice_time

def get_video_param(main_video, voice_time):
    start = random.randrange(60, (int(main_video) - int(voice_time)))
    end = start + voice_time
    return start, end

def download_background():
    print_step("Creating background...")
    path = 'mp4_files'
    Path(path).mkdir(exist_ok = True, parents = True)
    print_substep("We need to download background only once, do not worry we make sure that it is done only once")
    if not Path('mp4_files/background.mp4').exists():
        ydl_opts = {
            "outtmpl": 'mp4_files/background.mp4',
            "merge_output_format": "mp4",
        }
        print_substep("You can either provide a link or to use a build in, please write yes, "
                      "if you want to provide, no if you don't: ")
        answer = input()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if answer == 'no':
                ydl.download("https://www.youtube.com/watch?v=V7XVOHsuzYw")
            elif answer == 'yes':
                url = str(input("Well, provide a link then: "))
                ydl.download(url)
        print_substep("Backgorund video has been downloaded!", style = "bold green")
    else:
        print_substep("Background has already been saved!", style = "bold green")

def get_chopped_video(voice_time):
    print_step("Creating chopped video...")
    background_time = VideoFileClip('mp4_files/background.mp4').duration # in seconds
    start, end = get_video_param(background_time, voice_time)
    ffmpeg_extract_subclip(
        'mp4_files/background.mp4',
        start,
        end,
        targetname="mp4_files/background_chopped.mp4",
    )
    print_substep("Background has been chopped and successfully saved!", style = "bold green")

