import time
from datetime import datetime, timedelta

import requests
import schedule
import pytz

from decouple import config

from zikrs import list_of_zikr, juma_zikr_info, suhur_dua, iftar_dua, tarauyh_dua
from prayer_times import prayer_times

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {config('BEARER_TOKEN')}"
}

channel_id = config('CHANNEL_ID')
url = config('API_URL')

current_index = 0

timezone = pytz.timezone('Asia/Aqtau')


def base_send_message(message):
    payload = {
        "typing_time": 0,
        "to": channel_id,
        "body": message
    }
    requests.post(url, json=payload, headers=headers)


def send_message():
    global current_index
    now = datetime.now(timezone)
    current_hour = now.hour

    if 8 <= current_hour < 24:
        zikr_info = list_of_zikr[current_index]

        message_to_send = f"«{zikr_info['zikr']}»\n\n{zikr_info['translation']}\n\n📖 {zikr_info['source']}\n\nℹ️ {zikr_info['explanation']}"

        payload = {
            "typing_time": 0,
            "to": channel_id,
            "body": message_to_send
        }
        requests.post(url, json=payload, headers=headers)

        current_index = (current_index + 1) % len(list_of_zikr)


def send_juma_dua():
    message_to_send = f"Жұма зікірі🕌\n«{juma_zikr_info['zikr']}»\n\n{juma_zikr_info['translation']}\n\nℹ️ {juma_zikr_info['explanation']}"

    payload = {
        "typing_time": 0,
        "to": channel_id,
        "body": message_to_send
    }
    requests.post(url, json=payload, headers=headers)


def send_tarauyh_dua():
    message_to_send = f"🤲 Тарауих намазының тәсбихы:\n{tarauyh_dua['dua']}\n\nℹ️ {tarauyh_dua['translation']}"

    payload = {
        "typing_time": 0,
        "to": channel_id,
        "body": message_to_send
    }
    requests.post(url, json=payload, headers=headers)


def check_and_send_juma_dua():
    now = datetime.now(timezone)
    current_hour = now.hour
    current_minute = now.minute
    current_weekday = now.weekday()  # Понедельник = 0, Пятница = 4

    # Если пятница и текущее время 9:00, отправить вторую дуа
    if current_weekday == 4 and current_hour == 9 and current_minute == 0:
        send_juma_dua()


def send_ramadan_dua():
    today = datetime.now(timezone).day
    month = datetime.now(timezone).month

    if month == 3 and str(today) in prayer_times:
        now = datetime.now(timezone)
        suhur_time = timezone.localize(datetime.combine(now.date(), datetime.strptime(prayer_times[str(today)]["suhur"],
                                                                                      "%H:%M").time())) - timedelta(minutes=5)
        iftar_time = timezone.localize(datetime.combine(now.date(), datetime.strptime(prayer_times[str(today)]["iftar"],
                                                                                      "%H:%M").time())) - timedelta(minutes=5)

        zuhur_msg = f"🤲 Ауыз бекітерде оқылатын дұға:\n{suhur_dua['dua']}\n\nℹ️ {suhur_dua['translation']}"
        iftar_msg = f"🤲 Ауызашарда оқылатын дұға:\n{iftar_dua['dua']}\n\nℹ️ {iftar_dua['translation']}"

        schedule.every().day.at(suhur_time.strftime("%H:%M")).do(lambda: base_send_message(zuhur_msg))
        schedule.every().day.at(iftar_time.strftime("%H:%M")).do(lambda: base_send_message(iftar_msg))


def check_time_and_send_tarauyh_dua():
    now = datetime.now(timezone)
    current_hour = now.hour
    current_minute = now.minute

    if current_hour == 9 and current_minute == 0:
        send_tarauyh_dua()


def schedule_ramadan_tasks():
    if datetime.now(timezone).month == 3:
        schedule.every().minute.do(send_tarauyh_dua)
        schedule.every().minute.do(check_time_and_send_tarauyh_dua)


def schedule_ramadan_duas():
    now = datetime.now(timezone)
    if now.month == 3:  # Проверяем, идет ли Рамадан
        send_ramadan_dua()  # Запускаем сразу при проверке


# Запланировать проверку каждую минуту
schedule.every().minute.do(check_and_send_juma_dua)

schedule.every().hour.do(schedule_ramadan_tasks)

schedule.every(30).minutes.do(send_message)

schedule.every().day.at("00:01").do(schedule_ramadan_duas)

schedule_ramadan_duas()

while True:
    schedule.run_pending()
    time.sleep(1)
