
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
    #last_date = "2022-08-08T00:00:00+00:00"    
    since = datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')

    url = f'https://graph.facebook.com/v16.0/{page_id}/tags'
    params = {
        "fields": 'caption,permalink,id,media_url,username,timestamp,like_count',
        "access_token": token,
        "since": since,
        "until": datetime.today().strftime('%Y-%m-%d'),
    }

    response = requests.get(url, params=params)
    posts = response.json()

    def image_to_bucket(url, name):
        response = requests.get(url)
        type = response.headers['Content-Type']
        ext = type.split('/')[1]
        type = type.split('/')[0]
        size = response.headers['Content-Length']
        supabase.storage().from_('mentions').upload(
            f"{name}.{ext}", response.content)

        url = f"https://axjugomavcpjuegkhkya.supabase.co/storage/v1/object/public/mentions/{name}.{ext}"
        return url, type


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
                try:
                    name = secrets.token_hex(8)
                    url_imagen = i['media_url'] if 'media_url' in i else ''
                    imagen, media_type = image_to_bucket(
                        url_imagen, name) if url_imagen != '' else ''
                except Exception as e:
                    print(e)
                    imagen = ''
                likes = i['like_count'] if 'like_count' in i else 0
                post_id = i['id']
                color = "#C13584"
                red = 'instagram'
                fecha_str = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %d, %Y')
                doc = {'fecha': fecha, 'texto': texto, 'url': url, 'imagen': imagen, 'likes': likes, 'color': color, 'red': red, 'fecha_str': fecha_str, 'creador': creador, 'media_type': media_type}
                supabase.table('mentions').insert(doc).execute()

    return 'Instagram_mentions updated'