import subreddit
from console import print_substep, print_step, print_markdown
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    concatenate_audioclips,
    CompositeAudioClip,
    CompositeVideoClip,
)
from pathlib import Path
import re

W, H = 1080, 1920
def make_final_video(clips_number, content):
    opacity = subreddit.user_info['OPACITY']
    print_step("Creating a final video...")

    VideoFileClip.reW = lambda clip: clip.resize(width = W)
    VideoFileClip.reH = lambda clip: clip.resize(width = H)

    background_clip = (
        VideoFileClip("mp4_files/background_chopped.mp4")
        .without_audio()
        .resize(height = H)
        .crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
    )
    #insert, add audio info
    audio_clips = []
    for index in range(0, clips_number):
        audio_clips.append(AudioFileClip(f"audio_mp3/{index}_comment.mp3"))
    audio_clips.insert(0, AudioFileClip('audio_mp3/title.mp3'))
    try:
        audio_clips.insert(1, AudioFileClip('audio_mp3/body.mp3'))
    except OSError as e:
        pass
    audio_concat = concatenate_audioclips(audio_clips)
    audio_composite = CompositeAudioClip([audio_concat])

    #Gather Images
    image_clips = []
    for index in range(0, clips_number):
            image_clips.append(
                ImageClip(f"png_files/{index}_comment.png")
                .set_duration(audio_clips[index +1].duration)
                .set_position('center')
                .resize(width = W - 100)
                .set_opacity(float(opacity))
            )
    if Path('audio_mp3/body.mp3').exists():
        image_clips.insert(
            0,
            ImageClip(f'png_files/title.png')
                .set_duration(audio_clips[0].duration + audio_clips[1].duration)
                .set_position('center')
                .resize(width=W - 100)
                .set_opacity(float(opacity)),
        )
    else:
        image_clips.insert(
            0,
            ImageClip(f'png_files/title.png')
            .set_duration(audio_clips[0].duration)
            .set_position('center')
            .resize(width = W  - 100)
            .set_opacity(float(opacity)),
        )
    image_concat = concatenate_videoclips(image_clips).set_position(("center", "center"))
    image_concat.audio = audio_composite

    final = CompositeVideoClip([background_clip, image_concat])
    filename = (re.sub('[?\"%*:|<>]', '', ("final_video/" + content['thread_title'] + ".mp4")))
    final.write_videofile(filename, fps = 30, audio_codec = "aac", audio_bitrate="192k")




