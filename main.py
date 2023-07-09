from fastapi import FastAPI
from pydantic import BaseModel

from functions.facebook_posts import facebook_posts
from functions.instagram_posts import instagram_posts
from functions.youtube_posts import youtube_posts
from functions.facebook_mentions import facebook_mentions
from functions.instagram_mentions import instagram_mentions
from functions.facebook_messages import facebook_messages
from functions.trends import trends

app = FastAPI()

class Msg(BaseModel):
    msg: str

@app.get("/")
async def root():
    return "Social Listening API"

@app.get("/facebook_posts")
async def get_facebook_posts():
    data = facebook_posts()
    return data

@app.get("/facebook_mentions")
async def get_facebook_mentions():
    data = facebook_mentions()
    return data

@app.get("/facebook_messages")
async def get_facebook_messages():
    data = facebook_messages()
    return data


@app.get("/instagram_posts")
async def get_instagram_posts():
    data = instagram_posts()
    return data

@app.get("/instagram_mentions")
async def get_instagram_mentions():
    data = instagram_mentions()
    return data

@app.get("/youtube_posts")
async def get_youtube_posts():
    data = youtube_posts()
    return data

@app.get("/trends")
async def get_trends(keywords: str="Formica", timeframe: str="2023-01-01 2023-07-09"):
    data = trends(keywords,timeframe)
    return data