import time
from datetime import datetime

import requests
import schedule
import pytz

from decouple import config

from zikrs import list_of_zikr

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {config('BEARER_TOKEN')}"
}

channel_id = config('CHANNEL_ID')
url = config('API_URL')

timezone = pytz.timezone('Asia/Aqtau')

current_index = {
    "morning": 0,
    "evening": 0,
    "sleep": 0,
    "anytime": 0
}


def send_message():
    now = datetime.now(timezone)
    hour = now.hour

    if 8 <= hour < 10:
        zikr_category = "morning"
    elif 17 <= hour < 20:
        zikr_category = "evening"
    elif 20 <= hour < 22:
        zikr_category = "sleep"
    else:
        zikr_category = "anytime"

    zikr_list = list_of_zikr[zikr_category]

    index = current_index[zikr_category]
    zikr_info = zikr_list[index]

    message_to_send = f"«{zikr_info['zikr']}»\n\n{zikr_info['translation']}"
    if zikr_info['explanation']:
        message_to_send += f"\n\nℹ️ {zikr_info['explanation']}"

    payload = {
        "typing_time": 0,
        "to": channel_id,
        "body": message_to_send
    }
    requests.post(url, json=payload, headers=headers)

    current_index[zikr_category] = (index + 1) % len(zikr_list)


def send_juma_dua():
    juma_zikr = list_of_zikr["friday"][0]

    message_to_send = f"Жұма зікірі🕌\n«{juma_zikr['zikr']}»\n\n{juma_zikr['translation']}\n\nℹ️ {juma_zikr['explanation']}"

    payload = {
        "typing_time": 0,
        "to": channel_id,
        "body": message_to_send
    }
    requests.post(url, json=payload, headers=headers)


def check_and_send_juma_dua():
    now = datetime.now(timezone)
    if now.weekday() == 4 and now.hour == 9 and now.minute == 0:
        send_juma_dua()


schedule.every().minute.do(check_and_send_juma_dua)
schedule.every(30).minutes.do(send_message)


while True:
    schedule.run_pending()
    time.sleep(1)
