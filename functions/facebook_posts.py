import supabase
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = supabase.create_client(supabase_url, supabase_key)

def facebook_posts():
    last_date = supabase.table('posts').select('*').eq(column="red",value="facebook").order(column="fecha", desc=True).limit(1).execute()
    last_date = last_date.data[0]['fecha']

    token = os.environ.get('token')
    page_id = os.environ.get('fbid')

    url =  f"https://graph.facebook.com/v16.0/{page_id}/posts"

    params = {
        'access_token': token,
        'fields': 'id,created_time,message,permalink_url,full_picture,shares,likes.summary(true),comments.summary(true)',
    'since': last_date
    }

    response = requests.get(url, params=params)
    posts = response.json()['data']

    for post in posts:
        while 'paging' in response.json():
            for i in response.json()['data']:
                if 'message' in i:
                    fecha = i['created_time']
                    texto = i['message'] if 'message' in i else ''
                    url = i['permalink_url']
                    imagen = i['full_picture'] if 'full_picture' in i else ''
                    shares = i['shares']['count'] if 'shares' in i else 0
                    likes = i['likes']['summary']['total_count'] if 'likes' in i else 0
                    post_id = i['id']
                    color = "#4267B2"
                    red = 'facebook'
                    fecha_str = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %d, %Y')
                    doc = {'fecha': fecha, 'texto': texto, 'url': url, 'imagen': imagen, 'shares': shares, 'likes': likes, 'post_id': post_id, 'color': color, 'red': red, 'fecha_str': fecha_str}
                    supabase.table('posts').insert(doc).execute()
                    
            else:
                pass
            if 'next' in response.json()['paging']:
                response = requests.get(response.json()['paging']['next'])
            else:
                break

    return "Facebook posts updated"

