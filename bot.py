from utils import best_match, url_to_image
import praw
from bot_info import Info
import requests
import cv2
from skimage import io
import sqlite3 as db

conn = db.connect("replied_comments.db")
conn.execute("CREATE TABLE IF NOT EXISTS comments (comment_id VARCHAR(50))")
cur = conn.cursor()

subredditList = ["teenagers", "madeinpython"]

reddit = praw.Reddit(client_id = Info.client_id,
                    client_secret = Info.client_secret,
                    username = Info.username,
                    password = Info.password,
                    user_agent = Info.user_agent)

subreddit = reddit.subreddit("memetemplatesbottest")

keyphrase = "!memetemplatesbot"


for comment in subreddit.stream.comments():
    if keyphrase in comment.body:
        replied = cur.execute("SELECT COUNT(1) FROM comments WHERE comment_id=?",(comment.id,)).fetchone()[0]
        if replied==0:
            
            imageUrl = comment.submission.url
            imageData = url_to_image(imageUrl)
            bestMatchName = best_match(imageData)
            comment.reply(bestMatchName) 
            cur.execute("INSERT INTO comments(comment_id) VALUES(?)",(comment.id,))
            conn.commit()
conn.close()