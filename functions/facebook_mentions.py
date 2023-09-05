
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
token = os.environ.get('token')
page_id = os.environ.get('fbid')

def facebook_mentions():

    last_date = supabase.table('mentions').select('*').eq(column="red",value="facebook").order(column="fecha", desc=True).limit(1).execute()
    last_date = last_date.data[0]['fecha']
    

    url = f"https://graph.facebook.com/v16.0/{page_id}/tagged"
    params = {
        'access_token': token,
        "fields": "from,created_time,permalink_url,message,full_picture,shares",
        "since": last_date
    }
    response = requests.get(url, params=params)
    posts = response.json()['data']

    def image_to_bucket(url, name):
        response = requests.get(url)
        type = response.headers['Content-Type']
        ext = type.split('/')[1]
        type = type.split('/')[0]
        size = response.headers['Content-Length']
        supabase.storage().from_('mentions').upload(
            f"{name}.{ext}", response.content)

        return (f"https://axjugomavcpjuegkhkya.supabase.co/storage/v1/object/public/mentions/{name}.{ext}", type)
        
    for post in posts:
        for i in response.json()['data']:
            if 'message' in i and 'from' in i:
                creador = i['from']['name'] if 'from' in i else ''
                fecha = i['created_time']
                texto = i['message'] if 'message' in i else ''
                url = i['permalink_url']
                try:
                    name = secrets.token_hex(8)
                    url_imagen = i['full_picture'] if 'full_picture' in i else ''
                    imagen, media_type = image_to_bucket(
                        url_imagen, name) if url_imagen != '' else ''
                except Exception as e:
                    print(e)
                    print(post_id)
                    imagen = ''
                post_id = i['id']
                color = "#4267B2"
                red = 'facebook'
                fecha_str = datetime.strptime(
                    fecha, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %d, %Y')
                doc = {'fecha': fecha, 'texto': texto, 'url': url, 'imagen': imagen,
                       'creador': creador, 'color': color, 'red': red, 'fecha_str': fecha_str, 'media_type': media_type}
                supabase.table('mentions').insert(doc).execute()
                print(doc)

        else:
            pass
        if 'paging' in response.json() and 'next' in response.json()['paging']:
            url = response.json()['paging']['next']
        else:
            return "Facebook mentions updated"
