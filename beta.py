import django
import requests
import pdb
import json
import time

# getting the API token ( static file )
with open("GetThere_bot_token.txt",'r') as myfile:
    TOKEN = myfile.read().replace('\n', '')

# calling the bot
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_Me():
    """
    This is a default getMe function from the telegram
    obtain a text response of bot details
    :return: {"ok":true,"result":{"id":xxxxxxxxx,"is_bot":true,"first_name":"GetThere_bot","username":"GetThere_bot"}}
    """
    getMe_url = URL + "getMe"
    print(getMe_url)
    r = requests.get(getMe_url)
    return r.text


def get_updates_json():
    """
    This is a default getUpdates function from telegram
    obtain json response of the updates which contains info such as update_id,first_name,
    last_name, username,chat_id, text for when this code runs.
    anything send to the bot after this code is run will not be captured.
    :return: the json response
    """
    getUpdates_method = URL + "getUpdates"
    r_updates = requests.get(getUpdates_method)
    r_updates_json = json.loads(r_updates.text)
    return r_updates_json

#
# def get_text_chatID_name_from_json():
#     """
#     This function gets the json updates from get_updates_json() function
#     obtain the last updates and its id, text, and first name
#     :return: text, chat_id, first name of that update message
#     """
#     response_json = get_updates_json()
#     chat_id = response_json['result'][-1]['message']['chat']['id']
#     text = response_json['result'][-1]['message']['text']
#     name = response_json['result'][-1]['message']['from']['first_name']
#     return text, chat_id, name

def get_text_from_json(_response_json):
    """
    This function takes in the json response
    extracts the text out of latest message
    :param _response_json:
    :return: text
    """
    text = _response_json['result'][-1]['message']['text']
    return text

def get_chatID_from_json(_response_json):
    """
    This function takes in the json response
    extracts the chatid out of the latest message
    :param _response_json:
    :return: chatid
    """
    chatid = _response_json['result'][-1]['message']['chat']['id']
    return chatid

def get_name_from_json(_response_json):
    """
    This function takes in the json response
    extracts out the name from the latest message
    :param _response_json:
    :return: first name , last name
    """
    first_name = _response_json['result'][-1]['message']['from']['first_name']
    last_name =  _response_json['result'][-1]['message']['from']['last_name']
    return first_name, last_name



def send_message(_textMessage,_response_json):
    """
    takes in a dynamic message as the parameter
    :param _textMessage:
    this functions first get the text, chatid and name from the json response
    combines them in an updated text which adds in the user's name into the textmessage
    post it back to the chatbot as a response to the user
    :return: none
    """
    first_name, last_name = get_name_from_json(_response_json)
    chat_id = get_chatID_from_json(_response_json)

    _updated_text = "Hello {}, ".format(str(first_name)) + _textMessage
    url = URL + "sendMessage?text={}&chat_id={}".format(_updated_text, str(chat_id))
    requests.post(url)

response_json = get_updates_json()
def main():
    last_textchat = (None, None)
    while True:
        text = get_text_from_json(response_json)
        chat = get_chatID_from_json(response_json)
        if (text, chat) != last_textchat:
            send_message("How are you?",response_json)
            last_textchat = (text, chat)
        time.sleep(0.5)


if __name__ == '__main__':
    main()