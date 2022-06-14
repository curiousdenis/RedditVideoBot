from pathlib import Path
from gtts import gTTS
from subreddit import get_subreddit_threads
from mutagen.mp3 import MP3
from console import print_substep, print_step, print_markdown
import time

lang = 'en'

def create_audio(subreddit, voice_number):
    """ Here, we will create a voice cover for title, comment form the specific subreddit from subredit.py"""
    print_step("Creating audio...")
    length = 0
    path = 'audio_mp3'
    Path(path).mkdir(parents=True, exist_ok=True)
    subreddit_info = subreddit
    #add voice thread title
    gtts_title = gTTS(text = subreddit_info['thread_title'], lang = lang, slow = False)
    gtts_title.save('audio_mp3/title.mp3')
    length += MP3('audio_mp3/title.mp3').info.length

    #add thread body
    if subreddit_info['thread_post'] != "":
        gtts_body = gTTS(text = subreddit_info['thread_post'], lang = lang, slow = False)
        gtts_body.save('audio_mp3/body.mp3')
        length += MP3('audio_mp3/body.mp3').info.length
    else:
        pass

    #add voice comments
    for index, comment in enumerate(subreddit_info['comments']):
        # I want to voice cover 50 comments, it can be greater
        if index >= voice_number:
            break
        gtts_comment = gTTS(text = comment["comment_body"], lang = lang, slow = False)
        gtts_comment.save(f"audio_mp3/{index}_comment.mp3")
        length += MP3(f"audio_mp3/{index}_comment.mp3").info.length


    print_substep("Saved text to MP3 file, keep in mind: title - thread title, body - thread body.")
    time.sleep(3)
    return length