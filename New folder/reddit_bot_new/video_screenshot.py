from playwright.sync_api import sync_playwright, ViewportSize
from console import print_substep, print_step,print_markdown
from rich.progress import track
from pathlib import Path
from subreddit import get_subreddit_threads

def get_subreddit_screenshots(subreddit, screenshot_number):
    print_step("Creating screenshots...")
    path = 'png_files'
    # create and make sure that png_files folder exist
    Path(path).mkdir(parents = True, exist_ok = True)
    with sync_playwright() as p:
        print_substep("From 'with' statement, launching browser to ensure that it is closed at the end")
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        subreddit_info = subreddit
        page.goto(subreddit_info['thread_url'])
        page.set_viewport_size({'width' : 1920, 'height':1080})

        #here, we look for NSFW - not safe for work content
        if page.locator('[data-testid = "content_gate"]').is_visible():
            print(f"You are spicy...")
            page.locator('[data-testid = "content_gate"] button').click()

        # I really do not know what this thing is doing - EDIT* it will save title
        page.locator('[data-test-id="post-content"]').screenshot(path = 'png_files/title.png')

        # Here we will screenshot some comments based on url
        for index, comment in enumerate(subreddit['comments']):

            if index >= screenshot_number:
                break

            if page.locator('[data-testid = "content_gate"]').is_visible():
                page.locator('[data-testid = "content_gate"] button').click()

            page.goto(f'https://reddit.com{comment["comment_url"]}')
            page.locator(f"#t1_{comment['comment_id']}").screenshot(
                path = f"png_files/{index}_comment.png"
            )

        print_substep("Screenshots downloaded Successfully.", style="bold green")
