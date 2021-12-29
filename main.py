import datetime
import requests
import time
import os
from os import environ
from bs4 import BeautifulSoup

# Config
interval = 3600  # Sleep for 1 Hour
baseURI = 'https://www.parcelforce.com/track-trace?trackNumber='
usragnt = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'

# Temp Array
status = []

def telegram_bot_sendtext(bot_message, telegram_bot_token, telegram_chat_id):
    send_text = 'https://api.telegram.org/bot' + telegram_bot_token + '/sendMessage?chat_id=' + telegram_chat_id + '&parse_mode=html&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def getTracking(trackingCode, telegram_bot_token, telegram_chat_id):
    trackingURI = baseURI + trackingCode
    track = requests.get(trackingURI, headers={'User-Agent': usragnt})

    soup = BeautifulSoup(track.text, features="lxml")
    table = soup.find('table', attrs={'class': 'tableheader-processed sticky-enabled'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:

        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        if cols not in status:
            status.append([ele for ele in cols if ele])

            msg = '<b>Tracking:</b> ' + trackingCode + '\n' \
                + '<b>Date:</b> ' + cols[0] + '\n' \
                + '<b>Time:</b> ' + cols[1] + '\n' \
                + '<b>Location:</b> ' + cols[2] + '\n' \
                + '<b>Tracking Event:</b> ' + cols[3] + '\n'
            telegram_bot_sendtext(msg, telegram_bot_token, telegram_chat_id)

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def main():
    print(("{0} Starting...").format(now()))

    if environ.get('TRACKING_ID') is None:
        print(("{0} Error! TRACKING_ID not defined").format(now()))
        exit()
    tracking_id = os.environ['TRACKING_ID']

    if environ.get('TG_BOT_TOKEN') is None:
        print(("{0} Error! TG_BOT_TOKEN not defined").format(now()))
        exit()
    telegram_bot_token = os.environ['TG_BOT_TOKEN']

    if environ.get('TG_CHAT_ID') is None:
        print(("{0} Error! TG_CHAT_ID not defined").format(now()))
        exit()
    telegram_chat_id = os.environ['TG_CHAT_ID']

    while True:
        print(("{0} Checking...").format(now()))
        getTracking(tracking_id, telegram_bot_token, telegram_chat_id)
        time.sleep(interval)

if __name__ == '__main__':
    main()