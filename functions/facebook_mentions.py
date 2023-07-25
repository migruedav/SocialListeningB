
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
page_id = os.environ.get('fbid')

def facebook_mentions():

    last_date = supabase.table('mentions').select('*').eq(column="red",value="facebook").order(column="fecha", desc=True).limit(1).execute()
    last_date = last_date.data[0]['fecha']
    #last_date = 1626307200

    url =  f"https://graph.facebook.com/v16.0/{page_id}/tagged"
    params = {
        'access_token': token,
        "fields":"from,created_time,permalink_url,message,full_picture,shares",
        "since": last_date
    }
    response = requests.get(url, params=params)
    posts = response.json()['data']

    for post in posts:
        while 'paging':
            for i in response.json()['data']:
                if 'message' in i:
                    creador = i['from']['name'] if 'from' in i else ''
                    fecha = i['created_time']
                    texto = i['message'] if 'message' in i else ''
                    url = i['permalink_url']
                    imagen = i['full_picture'] if 'full_picture' in i else ''
                    post_id = i['id']
                    color = "#4267B2"
                    red = 'facebook'
                    fecha_str = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %d, %Y')
                    doc = {'fecha': fecha, 'texto': texto, 'url': url, 'imagen': imagen, 'creador': creador, 'color': color, 'red': red, 'fecha_str': fecha_str}
                    supabase.table('mentions').insert(doc).execute()
                    
            else:
                pass
            if 'next' in response.json()['paging']:
                response = requests.get(response.json()['paging']['next'])
            else:
                break

    return "Facebook mentions updated"
