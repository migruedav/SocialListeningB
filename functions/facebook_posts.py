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


def facebook_posts():
    last_date = supabase.table('posts').select(
        '*').eq(column="red", value="facebook").order(column="fecha", desc=True).limit(1).execute()
    last_date = last_date.data[0]['fecha']
    token = os.environ.get('token')
    page_id = os.environ.get('fbid')

    url = f"https://graph.facebook.com/v16.0/{page_id}/posts"

    params = {
        'access_token': token,
        'fields': 'id,created_time,message,permalink_url,full_picture,shares,likes.summary(true),comments.summary(true),attachments',
        'since': last_date
    }

    def image_to_bucket(url, name):
        response = requests.get(url)
        type = response.headers['Content-Type']
        ext = type.split('/')[1]
        type = type.split('/')[0]
        size = response.headers['Content-Length']
        supabase.storage().from_('posts').upload(
            f"{name}.{ext}", response.content)

        return (f"https://axjugomavcpjuegkhkya.supabase.co/storage/v1/object/public/posts/{name}.{ext}", type)

    while True:
        response = requests.get(url, params=params)
        posts = response.json()['data']

        for i in posts:
            if 'message' in i:
                fecha = i['created_time']
                texto = i['message'] if 'message' in i else ''
                url = i['permalink_url']
                post_id = i['id']

                try:
                    name = secrets.token_hex(8)
                    if 'source' in i['attachments']['data'][0]['media']:
                        url_imagen = (i['attachments']['data'][0]['media']['source'])
                    else:
                        url_imagen = (i['attachments']['data'][0]['media']['image']['src'])
                    imagen, media_type = image_to_bucket(
                        url_imagen, name) if url_imagen != '' else ''
                except Exception as e:
                    print(e)
                    print(post_id)
                    imagen = ''
                shares = i['shares']['count'] if 'shares' in i else 0
                likes = i['likes']['summary']['total_count'] if 'likes' in i else 0
                color = "#4267B2"
                red = 'facebook'
                fecha_str = datetime.strptime(
                    fecha, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %d, %Y')
                doc = {'fecha': fecha, 'texto': texto, 'url': url, 'imagen': imagen, 'shares': shares,
                       'likes': likes, 'post_id': post_id, 'color': color, 'red': red, 'fecha_str': fecha_str, 'media_type': media_type}
                supabase.table('posts').insert(doc).execute()

        if 'paging' in response.json() and 'next' in response.json()['paging']:
            url = response.json()['paging']['next']
        else:
            return "Facebook posts updated"