import django
import requests
import pdb
import json
import time
import telegram
#import telebot
import http.client
## adapted from https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
GENDER, PHOTO, LOCATION, BIO = range(4)

# getting the API token for telegram bot ( static file )
with open("GetThere_bot_token.txt",'r') as myfile:
    TOKEN = myfile.read().replace('\n', '')

# getting the API authentication for one map
with open("OneMap_Auth.txt",'r') as myfile1:
    OneMap_details = myfile1.read().splitlines()

# calling the bot
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def start(bot, update):
    reply_new_keyboard_1 = KeyboardButton("Send location",request_location = True)
    reply_new_keyboard_2 = KeyboardButton("Search location ")
    reply_keyboard = [[reply_new_keyboard_1,reply_new_keyboard_2]]
    logger.info("Run the start function")

    update.message.reply_text(
        'Welcome to the Get_There_bot! \n\n '
        'To start with, I would need your location. Or you could do a location search. \n\n'
        'Send /cancel to stop talking to me.\n\n',
        reply_markup= ReplyKeyboardMarkup(reply_keyboard,resize_keyboard = True, one_time_keyboard= True))

    user = update.message.from_user
    print(user)
    location = update.message.location
    print(location)
    return LOCATION

def gender(bot, update):
    user = update.message.from_user
    location = update.message.location
    print("user location?")
    print(location)
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


# def bio(bot, update):
#     user = update.message.from_user
#     logger.info("Bio of %s: %s", user.first_name, update.message.text)
#     update.message.reply_text('Thank you! I hope we can talk again some day.')
#
#     return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LOCATION: [MessageHandler(Filters.location, location)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

