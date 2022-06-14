from subreddit import get_subreddit_threads
from video_screenshot import get_subreddit_screenshots
from video_background import download_background, get_chopped_video
from video_voice import create_audio
from video_final import make_final_video

number_of_comments = int(input("Please, provide us a number of comments to work with: "))
content = get_subreddit_threads()
video_length = create_audio(content, number_of_comments)
download_background()
get_chopped_video(video_length)
get_subreddit_screenshots(content, number_of_comments)
final_video = make_final_video(number_of_comments, content)
