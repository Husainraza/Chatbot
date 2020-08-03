import requests
import time
import urllib
import ganster


TOKEN = "1060340522:AAHwgNAwVqc2ONPtzQX0TPvQjnFOss67xHA"
URL = f"https://api.telegram.org/bot{TOKEN}/"


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url = url + f"&offset={offset}"
    response = requests.get(url)
    js = response.json()
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def reply_message(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        reply = ganster.reply_message(text)
        send_message(reply, chat)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}"
    requests.get(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            reply_message(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()