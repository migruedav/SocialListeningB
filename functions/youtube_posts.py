import requests
from datetime import datetime, timedelta
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def youtube_posts():
    last_post = supabase.table('posts').select('*').eq(column="red",value="youtube").order(column="fecha", desc=True).limit(1).execute()
    last_post = last_post.data[0]['fecha']
    last_post = datetime.strptime(last_post, '%Y-%m-%dT%H:%M:%S%z')+timedelta(minutes=1)
    published_after = last_post.strftime('%Y-%m-%dT%H:%M:%SZ')


    api_key = os.environ.get('api_key')
    channel_id = os.environ.get('channel_id')
    meses = ["X","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]


    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=id&order=date&maxResults=50&publishedAfter={published_after}"
    response = requests.get(url)
    response = response.json()['items']

    ids = []

    for i in response:
        if 'videoId' in i['id']:
            ids.append(i['id']['videoId'])

    data = []
    for id in ids:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={id}&key={api_key}"
        response = requests.get(url)
        data.append(response.json())

    for i in data:
        print(i)
        id = i['items'][0]['id']
        fecha = i['items'][0]['snippet']['publishedAt']
        day = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S%z')
        fecha_str = f"{meses[day.month]} {day.day}, {day.year}"
        url = f"https://www.youtube.com/watch?v={id}"
        texto = i['items'][0]['snippet']['title']
        imagen = i['items'][0]['snippet']['thumbnails']['high']['url']
        likes = int(i['items'][0]['statistics']['likeCount'])
        doc = {'fecha': fecha, 'texto': texto, 'url': url,'imagen': imagen, 'likes': likes, 'post_id': id, 'color': 'red','red':'youtube', "fecha_str":fecha_str}

        supabase.table('posts').insert(doc).execute()

    return "Youtube Posts Actualizados"