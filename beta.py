import django
import requests
import pdb
import json
import time

# getting the API token
with open("GetThere_bot_token.txt",'r') as myfile:
    TOKEN = myfile.read().replace('\n', '')

print(TOKEN)
#HEADER_URL = "https://api.telegram.org/bot"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_Me():
    getMe_url = URL + "getMe"
    print(getMe_url)
    r = requests.get(getMe_url)
    # for testing purposes
    print(r.text)
    return r.text

def get_updates_json():
    getUpdates_method = URL + "getUpdates"
    r_updates = requests.get(getUpdates_method)
    r_updates_json = json.loads(r_updates.text)
    return r_updates_json


#pdb.set_trace()
#getMe_method = URL +"/getMe"
#r = requests.get(getMe_method)
#print(r.text)

#r1 = requests.get(getUpdates_method)

def get_text_chatID_name_from_json():
    _response_json = get_updates_json()
    chat_id = _response_json['result'][-1]['message']['chat']['id']
    text =  _response_json['result'][-1]['message']['text']
    name =  _response_json['result'][-1]['message']['from']['first_name']
    return text, chat_id, name

## read json  string
#r1_json = json.loads(r1.text)
def send_message(_textMessage):
    text, chat_id, name = get_text_chatID_name_from_json()
    _updated_text = "Hello {}, ".format(str(name)) + _textMessage
    url = URL + "sendMessage?text={}&chat_id={}".format(_updated_text, str(chat_id))
    requests.post(url)

#pdb.set_trace()

def main():
    last_textchat = (None, None)
    while True:
        text, chat, name = get_text_chatID_name_from_json()
        if (text, chat) != last_textchat:
            send_message("How are you?")
            last_textchat = (text, chat)
        time.sleep(0.5)


if __name__ == '__main__':
    main()