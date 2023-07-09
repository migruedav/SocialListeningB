import os
from supabase import create_client, Client
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get('token')
fbid = os.environ.get('fbid')

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def facebook_messages():
    last_message = supabase.table('messages').select('*').order('fecha', desc=True).limit(1).execute()
    last_message = last_message.data[0]['fecha']
    print(last_message)
    ids = supabase.table('posts').select('post_id').filter(column='fecha', operator='gt', criteria=last_message).filter(column='red', operator='eq', criteria='facebook').execute()
    ids = [i['post_id'] for i in ids.data]


    for post_id in ids:
        url = f"https://graph.facebook.com/{post_id}/comments"
        params = {
            "fields": "from,created_time,message,like_count",
            "access_token": token,
        }
        response = requests.get(url, params=params)
        response = response.json()
        data = response['data']
        for i in data:
            print(i)
            if 'from' in i and  i['from'] != 'Formica de México':
                pass
            else:
                if 'message' in i:
                    url = "https://api.mymemory.translated.net/get"
                    params = {
                        "q": i['message'],
                        "langpair": "es|en",
                    }

                    response = requests.get(url, params=params)
                    response = response.json()
                    message_en = response['responseData']['translatedText']
                    doc = {"fecha": i['created_time'], 'post_id': post_id, 'message': i['message'],'red': 'facebook', 'message_en': message_en}
                    supabase.table('messages').insert(doc).execute()
    else:
        pass

    return "Facebook messages updated"
