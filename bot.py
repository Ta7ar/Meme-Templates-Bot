from utils import best_match, url_to_image
import praw
from bot_info import Info
import requests
import cv2
from skimage import io
import sqlite3 as db
from pprint import pprint

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
            
            if comment.submission.is_reddit_media_domain and comment.submission.domain == "i.redd.it":
                imageUrl = comment.submission.url
                imageData = url_to_image(imageUrl)
                bestMatchLink,percentageMatch = best_match(imageData)
                print(bestMatchLink)
                commentStr = (  f"[Best Match]({bestMatchLink}) with a {percentageMatch} % match\n\n"
                                "^(I am a bot created by) ^u/ZeCookieMunsta." 
                                "^(I don\'t have all the images. Help better my search by)"
                                "^[Contributing!](https://github.com/Ta7ar/Meme-Templates-Bot)" )
                comment.reply(commentStr) 
                cur.execute("INSERT INTO comments(comment_id) VALUES(?)",(comment.id,))
                conn.commit()
            else:
                #post does not contain an image
                pass
conn.close()