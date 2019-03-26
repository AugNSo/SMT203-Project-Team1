import sys
import time
import threading
import random
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import telegram

"""
$ python3.5 skeleton_route.py <token>
It demonstrates:
- passing a routing table to `message_loop()` to filter flavors.
- the use of custom keyboard and inline keyboard, and their various buttons.
Remember to `/setinline` and `/setinlinefeedback` to enable inline mode for your bot.
It works like this:
- First, you send it one of these 4 characters - `c`, `h` - and it replies accordingly:
    - `c` - a custom keyboard with various buttons
    - `h` - hide custom keyboard
- Press various buttons to see their effects
"""
def validation_reply(msg):
    return bot.sendMessage(chat_id, msg)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)
    ########################
    updates = bot.getUpdates()                       ## 这一段只适用于step_2
    response1 = updates[0]["message"]["text"]
    step_2(response1)
    ########################
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
    elif command == 'h':
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)

#######################################################################################################################################
chat_id = "386055474" ## this need to extract from database
# text = """Pls enter 1.Professor's name OR 2.Course code OR 3.Course name.
#         Choose ONE of them with the index infront. 
#         (i.e 1.Tan Hwee Xian OR 2.SMT203 OR 3.SCSM)"""
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
    return (text, chat_id)


def step_2(response1):  ## this need to check what kinds of response from button (need edition)
    if response1 == "Search by Course ID":
        msg = "Pls enter course code"
    elif response1 == "Search by Course Name":
        msg = "Pls enter course name"
    elif response1 == "Search by Professor Name":
        msg = "Pls enter professor name"
    return validation_reply(msg)                              ## this step is just to check user click on which button and giev corresponding respond


# response2 = "SMT203" ## this need to get from user 

def step_2_vaildation(response2):
    if response1 == "Search by Course ID":
        if response2.isalpha() or response2.isdigit():
            msg = "Pls enter the correct format of Course code"
            return validation_reply(msg)
        else:
            return step_3(response2)
    if response1 == "Search by Course Name":
        cname_without_space =response2.replace(" ", "")
        if cname_without_space.isalpha():
            return step_3(response2)               ## cname may not be complete and contain space
        else:
            msg = "Pls enter the correct format of course name"
            return validation_reply(msg)
    if response1 == "Search by Professor Name":
        pname_without_space = response2.replace(" ", "")
        if pname_without_space.isalpha():
            return step_3(response2)     ## pname contains space e.g "Tan Hwee Xian"
        else:
            msg = "Pls enter the correct format of Prof name"
            return validation_reply(msg)


def step_3(response2):  ## vaildate the input and start calling API
    l = []
    ## call our Course API and retrieve corresponding prof and append into list l
    if l == []:
        msg = "Pls check your input"
        return validation_reply(msg)
    return send_list(l)

def send_list(l):
    keyboard = []
    # Mirar el "KeyboardButton(text='Location', request_location=True)", lo que hace que se comparta las cordenadas.
    for i in l:
        z = []
        x = i
        z.append(x)
        keyboard.append(z)

    markup = ReplyKeyboardMarkup(keyboard=keyboard)
    bot.sendMessage(chat_id, 'Pls indicate which professor you want to review', reply_markup=markup)

# response3 = "xxx"      ## base on which button user select
## 怎么用response3 trigger step_4?

def step_4():
    review_scores = """ Please provide scores based on 'Clarity of Teaching', 'Workload', 'Grading Fairnes'.(i.e. 3.5,4,5) """
    return bot.sendMessage(chat_id, review_scores)

def step_5():         ## may change to better way...
    review_qns = """Following questions are optional.
                    1. Any further comment?
                    2. Any advice for prof to improve?
                    3. Your School
                    4. Your current year 
                    (i.e. 1.Don't bid for this mod, it is tiring, 3.SIS, 3. 2)"""
    return bot.sendMessage(chat_id, review_qns)    
#######################################################################################################################################

# Cambiar el Token
#TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot("782592193:AAGUgd3khDTWnymBdLx8co21UE9ihaIGFPg")
answerer = telepot.helper.Answerer(bot)

bot.message_loop({'chat': on_chat_message})
print('Listening ...')

# step_2(response1)
# Keep the program running.
while 1:
    time.sleep(10)