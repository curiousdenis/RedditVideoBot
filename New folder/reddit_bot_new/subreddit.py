import praw
from console import print_markdown, print_step, print_substep
import random

with open(".env.txt") as f:
    content = f.readlines()
content_list = []
for lines in content:
    lines = lines.split('=')
    for line in lines:
        line.rstrip()
        content_list.append(line)
def convert(lst):
    res_dct = {lst[i]: lst[i + 1].rstrip() for i in range(0, len(lst), 2)}
    return res_dct
user_info = convert(content_list)


def get_subreddit_threads():
    """Returns a list of threads from AskReddit subreddit"""

    print_step("Sarch for a subreddit...", justify='right')

    content = {}

    # my information
    reddit = praw.Reddit(
        client_id=user_info['REDDIT_CLIENT_ID'],
        client_secret=user_info['REDDIT_CLIENT_SECRET'],
        user_agent="Accessing AskReddit threads",
        username=user_info['REDDIT_USERNAME'],
        password=user_info['REDDIT_PASSWORD'],
        check_for_async = False,
    )

    # subreddit info - prompt user to type a subreddit name, which is the name of a club (movie, askanything etc.)
    if user_info['SUBREDDIT']:
        subreddit = reddit.subreddit(user_info['SUBREDDIT'])
    elif not user_info['SUBREDDIT'] and (user_info['REDDIT_SUBREDDIT_URL'] == "yes"):
        # here submission is essentially a thread
        print_substep("Please, provde url")
        thread_url = input()
        submission = reddit.submission(url = thread_url)
    else:
        try:
            subreddit = reddit.subreddit(input("What subreddit would you like to pull from? "))
            threads = subreddit.hot(limit=25)
            submission = list(threads)[random.randrange(0, 25)]
            print_substep(f"Video will be: {submission.title} :thumbsup:")
        except Exception as e:
            subreddit = reddit.subreddit("askreddit")
            print_substep("Subreddit not defined. Using AskReddit instead.", style="red")
            threads = subreddit.hot(limit=25)
            submission = list(threads)[random.randrange(0, 25)]
            print_substep(f"Video will be: {submission.title} :thumbsup:")
    try:
        content['thread_title'] = submission.title
        content['thread_url'] = submission.url
        content['thread_post'] = submission.selftext
        content['comments'] = []
        for top_level_comment in submission.comments:
            content['comments'].append(
                {
                    "comment_body": top_level_comment.body,
                    "comment_url": top_level_comment.permalink,
                    "comment_id": top_level_comment.id, }
            )
    except Exception as e:
        pass

    print_substep(f"Received {submission.title} threads successfully.\n", style="bold green")
    print("-----------------------------------------------------------------------------------------")
    return content

