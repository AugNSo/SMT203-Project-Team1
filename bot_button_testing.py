import sys
import time
import threading
import random
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

"""
$ python3.5 skeleton_route.py <token>
It demonstrates:
- passing a routing table to `message_loop()` to filter flavors.
- the use of custom keyboard and inline keyboard, and their various buttons.
Remember to `/setinline` and `/setinlinefeedback` to enable inline mode for your bot.
It works like this:
- First, you send it one of these 4 characters - `c`, `i`, `h`, `f` - and it replies accordingly:
    - `c` - a custom keyboard with various buttons
    - `i` - an inline keyboard with various buttons
    - `h` - hide custom keyboard
    - `f` - force reply
- Press various buttons to see their effects
"""

message_with_inline_keyboard = None
chat_id = "386055474"

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        return

    command = msg['text'][-1:].lower()

    if command == 'c':
        # Mirar el "KeyboardButton(text='Location', request_location=True)", lo que hace que se comparta las cordenadas.
        markup = ReplyKeyboardMarkup(keyboard=[
                     ['Search by Course ID', KeyboardButton(text='Search by Course Name')],
                     [KeyboardButton(text = "Search by Professor Name")],
                 ])
        bot.sendMessage(chat_id, 'Pls indicate which methods would you like to use', reply_markup=markup)
    elif command == 'i':
        markup = InlineKeyboardMarkup(inline_keyboard=[
                     [dict(text='Search By Course ID', callback_data="courseID")],
                     [InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
                     [dict(text='Search By Course Name', callback_data='alert')],
                     [InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
                     [dict(text='Search By Professor Name', switch_inline_query='initial query')],
                 ])

        global message_with_inline_keyboard
        message_with_inline_keyboard = bot.sendMessage(chat_id, 'Inline keyboard with various buttons', reply_markup=markup)
    elif command == 'h':
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)
    elif command == 'f':
        markup = ForceReply()
        bot.sendMessage(chat_id, 'Force reply', reply_markup=markup)


#######################################################################################################################################

#######################################################################################################################################

# Cambiar el Token
#TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot("782592193:AAGUgd3khDTWnymBdLx8co21UE9ihaIGFPg")
answerer = telepot.helper.Answerer(bot)

bot.message_loop({'chat': on_chat_message})
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)