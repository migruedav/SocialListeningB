import supabase
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import secrets

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = supabase.create_client(supabase_url, supabase_key)


def instagram_posts():
    last_date = supabase.table('posts').select('*').eq(column="red",value="instagram").order(column="fecha", desc=True).limit(1).execute()
    last_date = last_date.data[0]['fecha']

    def image_to_bucket(url, name):
        response = requests.get(url)
        type = response.headers['Content-Type']
        ext = type.split('/')[1]
        type = type.split('/')[0]
        size = response.headers['Content-Length']
        supabase.storage().from_('posts').upload(
            f"{name}.{ext}", response.content)

        return (f"https://axjugomavcpjuegkhkya.supabase.co/storage/v1/object/public/posts/{name}.{ext}", type)

    token = os.environ.get('token')
    page_id = os.environ.get('igid')

    url = f"https://graph.facebook.com/v11.0/{page_id}/media"
    fields = ['id', 'media_url', 'like_count', 'caption',
              'timestamp', 'permalink', 'thumbnail_url', 'media_type']
    params = {
        "fields": ','.join(fields),
        "access_token": token,
        "since": last_date
    }

    posts = requests.get(url, params=params).json()

    while 'paging' in posts:
        for i in posts['data']:
            if 'caption' in i:
                fecha = i['timestamp']
                texto = i['caption'] if 'caption' in i else ''
                url = i['permalink']
                # imagen = i['media_url'] if 'media_url' in i else ''
                try:
                    name = secrets.token_hex(8)
                    url_imagen = i['media_url'] if 'media_url' in i else ''
                    imagen,media_type = image_to_bucket(
                        url_imagen, name) if url_imagen != '' else ''
                except Exception as e:
                    print(e)
                    print(post_id)
                    imagen = ''
                likes = i['like_count'] if 'like_count' in i else 0
                post_id = i['id']
                color = "#C13584"
                red = 'instagram'
                fecha_str = datetime.strptime(
                    fecha, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %d, %Y')
                doc = {'fecha': fecha, 'texto': texto, 'url': url, 'imagen': imagen, 'likes': likes,
                       'post_id': post_id, 'color': color, 'red': red, 'fecha_str': fecha_str, 'media_type': media_type}
                supabase.table('posts').insert(doc).execute()

        else:
            pass
        if 'next' in posts['paging']:
            posts = requests.get(posts['paging']['next']).json()
        else:
            break

    return "Instagram posts updated"
