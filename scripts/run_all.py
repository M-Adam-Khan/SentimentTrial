#!/usr/bin/env python3

import os
import subprocess

REDDIT_POST_URL = "https://www.reddit.com/r/politics/comments/1nr5x4r/oversight_democrats_release_third_batch_of/"

def run_script(script_filename, input_text=None):
    path = os.path.join("scripts", script_filename)
    print(f"\nRunning {script_filename}...")
    subprocess.run(["python", path], input=input_text, text=True)

def main():
    run_script("scrape_reddit.py", input_text=REDDIT_POST_URL + "\n")
    run_script("preprocess.py")
    run_script("train_model.py")
    run_script("save_db.py")
    run_script("query_db.py")
    run_script("post_discord.py")

if __name__ == "__main__":
    main()
