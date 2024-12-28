import time
from datetime import datetime

import requests
import schedule
import pytz

from decouple import config


list_of_zikr = [
    '“Ләә иләәһә илләә әнтә субхәәнәкә иннии кунту минәз-зоолимиин” деп айт\n\n~ Аллаһым, барлық кемшіліктен пәк және аса даңқты Сенен өзге (құлшылыққа ие) ешбір құдай жоқ. Шынында, мен өзіме зұлымдық еткендерден болдым~',
    '«Аллаһуммә бисмикә әмуту уә әхя» деп айт \n\n~ Аллаһым! Тек Сенің атыңмен өлеміз және тірілеміз',
    '"Аллаһумма ‘кфинихим бимә шитә" деп айт\n\n~ Я, Аллаһ! Мені олардан өзің қалаған жолмен құтқара көр~',
    '"Ләббайк Аллаһумма ләббайк, ләббайкә ләә шәрика ләкә ләббайк, инналхәмда уанни’мәтә ләкә уалмулк, ләә шәрика ләк" деп айт \n\n~ Аллаһым, мен сенің әміріңді орындауға келдім, сенің әміріңе бой ұсындым. Сенің серігің жоқ, сенің әміріңді орындау – менің борышым. Күмәнсіз барлық мадақ саған тән және жалпы иелік пен нығмет сенікі. Сенің еш серігің жоқ ~',
    '"Лә иләһә иллә Аллаһ, уәхдәһу лә шәрикә ләһ" деп айт\n\n~ Алладан басқа Құдай жоқ, Ол - жалғыз, оның серігі жоқ~',
    '"Робби яссир уа ләә ту`ассир, уә тәммим бил-хайр" деп айт \n\n~ Раббым! Ісімді жеңілдет және қиындата көрме. Бастаған ісімнің қайырлы аяқталуын нәсіп ет!~',
    '"Лә хәулә уә лә қууәтә иллә билләһ" деп айт \n\n~ барлық күш-қуат тек Аллаға тән ~',
    '"Аллаһу Акбар" деп айт\n\n ~ Алла ұлы ~',
    '"СубханАллаһ" деп айт \n\n~ Алла - мінсіз ~',
    '"Әстағфируллаһ уә әтубу иләйһ" деп айт \n\n~ Алладан кешірім тілеп, Оған тәубе етемін ~',
    '“Аллаһумма ахсин хулуқи” \n\n ~ Аллаһым, мінезімді жақсарта көр! ~',
    '«Джәзаллаһу `аннә Мухаммадан бимә һуә әһлуһ» \n\n {Алла Тағала Мұхаммедті біздің атымыздан сый құрметке бөлесін, өйткені Ол онсыз да бұған әбден лайық}',
    '"Бисмилләһир-рохманиир-рохиим" деп айт \n\n ~ Аса Рақымды, Аса Мейірімді Алланың атымен ~',
    '"Әлхамдулилләһ" деп айт \n\n ~ Аллаға мадақ (шүкір) ~'
]

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {config('BEARER_TOKEN')}"
}

channel_id = config('CHANNEL_ID')
url = config('API_URL')

current_index = 0

timezone = pytz.timezone('Asia/Almaty')

def send_message():
    global current_index
    now = datetime.now(timezone)
    current_hour = now.hour

    if 9 <= current_hour < 22:

        message_to_send = list_of_zikr[current_index]

        payload = {
            "typing_time": 0,
            "to": channel_id,
            "body": message_to_send
        }
        requests.post(url, json=payload, headers=headers)
        print(f"Отправлено сообщение: {message_to_send}")

        current_index = (current_index + 1) % len(list_of_zikr)
    else:
        print(f"Сейчас {current_hour} часов, бот не отправляет сообщения в это время.")

def send_juma_dua():
    message_to_send = """**Жұма күнгі салауат**\n\nПайғамбарымыз Мұхаммед ﷺ былай деп айтты:\n"Кімде-кім жұма күні маған 80 рет салауат айтса, оның 80 жылдық күнәлары кешіріледі."\n\nЖұма күні **"Аллаһумма солли ‘алә Мухаммадин уә 'алә әли Мухаммад"** деп 80 рет айтыңыз."""

    payload = {
        "typing_time": 0,
        "to": channel_id,
        "body": message_to_send
    }
    requests.post(url, json=payload, headers=headers)
    print(f"Отправлено Жұма дұғасы: {message_to_send}")


def send_juma_dua_2():
    message_to_send = """Жұма күні айтатын дұға\n\n"Әстағфируллаһәлләзи лә иләһә иллә һуәл хайюл қайиуму уә әтубу иләйһи" деп 3 рет айтыңыз.\n\nМағынасы:\n«Өзінен басқа ешбір тәңір болмаған, әрдайым тірі, әр нәрсені толық басқарып тұрушы Алладан күнәларыма кешірім сұраймын және Оған тәубе етемін»."""

    payload = {
        "typing_time": 0,
        "to": channel_id,
        "body": message_to_send
    }
    requests.post(url, json=payload, headers=headers)
    print(f"Отправлено Жұма дұғасы: {message_to_send}")

def check_and_send_juma_dua():
    now = datetime.now(timezone)
    current_hour = now.hour
    current_minute = now.minute
    current_weekday = now.weekday()  # Понедельник = 0, Пятница = 4

    # Если пятница и текущее время 10:00, отправить первую дуа
    if current_weekday == 4 and current_hour == 10 and current_minute == 0:
        send_juma_dua_2()

    # Если пятница и текущее время 11:00, отправить вторую дуа
    elif current_weekday == 4 and current_hour == 11 and current_minute == 0:
        send_juma_dua()


# Запланировать проверку каждую минуту
schedule.every().minute.do(check_and_send_juma_dua)
schedule.every(15).minutes.do(send_message)


while True:
    schedule.run_pending()
    time.sleep(1)
