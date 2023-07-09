
import supabase
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = supabase.create_client(supabase_url, supabase_key)
token = os.environ.get('token')
page_id = os.environ.get('igid')

def instagram_mentions():
    last_date = supabase.table('mentions').select('*').eq(column="red",value="instagram").order(column="fecha", desc=True).limit(1).execute()
    last_date = last_date.data[0]['fecha']

    since = datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')
    print(last_date)

    url = f'https://graph.facebook.com/v16.0/{page_id}/tags'
    params = {
        "fields": 'caption,permalink,id,media_url,username,timestamp,like_count',
        "access_token": token,
        "since": since,
        "until": datetime.today().strftime('%Y-%m-%d'),
    }

    response = requests.get(url, params=params)
    posts = response.json()
    for i in posts['data']:
        if i['timestamp'] < last_date:
            break
        else:
            if 'caption' in i:
                print(i['timestamp'])
                creador = i['username'] if 'username' in i else None
                fecha = i['timestamp']
                texto = i['caption'] if 'caption' in i else ''
                url = i['permalink']
                imagen = i['media_url'] if 'media_url' in i else ''
                likes = i['like_count'] if 'like_count' in i else 0
                post_id = i['id']
                color = "#4267B2"
                red = 'instagram'
                fecha_str = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %d, %Y')
                doc = {'fecha': fecha, 'texto': texto, 'url': url, 'imagen': imagen, 'likes': likes, 'color': color, 'red': red, 'fecha_str': fecha_str, 'creador': creador}
                supabase.table('mentions').insert(doc).execute()

    return 'Instagram_mentions updated'