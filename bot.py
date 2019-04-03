import time
import threading
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop

## Current Problem faced:
## 1. I have declared the global variables (mark) but when I update them in the later on functions, it does not change...
## 2. line 38 will the the chat_id but I have to pass it as a parameter to other functions instead of letting it become a global variable.
## 3. Because it is very hard to differentiate what the user inputs so we didn't do much vaildation and assuming user can follow the correct format all the way.
## 4. If the user input part of the Prof name/ course name, our API will search for them and return the possible output for them to choose. But because of problem 3, 
##    it is very hard to achieve this function
## p.s. We have link this bot to our api so from line 113-129 will be hard code for now.

#################################################
## response1: which method user want to use
## response2: pname/ cname/ cid                       
## response3: pname/ cname/ cid            ## This will be from buttons
## response4: scores
## response5: optional things
###################################################
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
mark = 0
response1 = ""
response2 = ""
# chat_id = "386055474" ## this need to extract from database

def on_chat_message(msg):
    # chat_id = msg['chat']["id"]
    content_type, chat_type, chat_id = telepot.glance(msg)                
    print('Chat:', content_type, chat_type, chat_id)                                                                 
    if content_type != 'text':                                            
        return                                                           
    global response1                                                     
    global response2
    global mark                                                       ## 问题： 后面要是改 var 貌似没有用啊！！！！！！！！
    response = msg['text']                             
    if response[:6] == "Search":                                        
        response1 = response
        step_2(response1, chat_id) 
    elif mark == 1:
        response3 = response 
        step_4(chat_id)       
    elif mark == 2:
        response4 = response
        step_5(chat_id)
    elif mark == 3:
        response5 = response
        msg = "Thank you for your review."
        validation_reply(msg, chat_id)
    elif response1 != "" and mark == 0:    
        response2 = response
        step_2_vaildation(response2, response1, chat_id)

    ########################
    elif response == 'c' or mark == 10:
        markup = ReplyKeyboardMarkup(keyboard=[
                     ['Search by Course ID', KeyboardButton(text='Search by Course Name')],
                     [KeyboardButton(text = "Search by Professor Name")],
                 ])
        bot.sendMessage(chat_id, 'Pls indicate which methods would you like to use', reply_markup=markup)
    elif response == 'h':
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)

#######################################################################################################################################


def validation_reply(msg, chat_id):
    return bot.sendMessage(chat_id, msg)

def step_2(response1, chat_id):  
    if response1 == "Search by Course ID":
        msg = "Pls enter course code"
    elif response1 == "Search by Course Name":
        msg = "Pls enter course name"
    elif response1 == "Search by Professor Name":
        msg = "Pls enter professor name"
    
    return validation_reply(msg, chat_id)                              ## this step is just to check user click on which button and give corresponding respond


# response2 = "SMT203" ## this need to get from user 

def step_2_vaildation(response2, response1, chat_id):
    if response1 == "Search by Course ID":
        if response2.isalpha() or response2.isdigit():
            msg = "Pls enter the correct format of Course code"
            return validation_reply(msg, chat_id)
        else:
            return step_3(response2, response1, chat_id)
    if response1 == "Search by Course Name":
        cname_without_space =response2.replace(" ", "")
        if cname_without_space.isalpha():
            return step_3(response2, response1, chat_id)              ## cname may not be complete and contain space
        else:
            msg = "Pls enter the correct format of course name"
            return validation_reply(msg, chat_id)
    if response1 == "Search by Professor Name":
        pname_without_space = response2.replace(" ", "")
        if pname_without_space.isalpha():
            return step_3(response2, response1, chat_id)     ## pname contains space e.g "Tan Hwee Xian"
        else:
            msg = "Pls enter the correct format of Prof name"
            return validation_reply(msg, chat_id)

##############################################################################################
def step_3(response2, response1, chat_id):  ## vaildate the input and start calling API          
    global mark

    l = []
    if response1 == "Search by Course ID": 
        l = ["XYZ", "ABC", "DEF"]
    if response1 == "Search by Course Name":
        l = ["XYZ", "ABC", "DEF"]
    if response1 == "Search by Professor Name":
        l = ["IS111", "SMT222", "IS123"]
    ## call our Course API and retrieve corresponding prof and append into list l
    if l == []:
        msg = "Pls check your input"
        mark = 10
        response1 = ""
        return validation_reply(msg, chat_id), mark, response1                                        ## 这里会让他们从头再来、成功与否取决于 response1 有没有被清零
    mark = 1
    return send_list(l, chat_id), mark
#############################################################################################################
def send_list(l, chat_id):
    keyboard = []
    for i in l:
        z = []
        x = i
        z.append(x)
        keyboard.append(z)

    markup = ReplyKeyboardMarkup(keyboard=keyboard)
    bot.sendMessage(chat_id, 'Pls indicate which professor/course you want to review', reply_markup=markup)

# response3 = "xxx"      ## base on which button user select

def step_4(chat_id):
    global mark
    review_scores = """ Please provide scores based on 'Clarity of Teaching', 'Workload', 'Grading Fairnes'.(i.e. 3.5,4,5) """
    mark = 2
    return bot.sendMessage(chat_id, review_scores), mark

def step_5(chat_id): 
    global mark        
    review_qns = """Following questions are optional.
                    1. Any further comment?
                    2. Any advice for prof to improve?
                    3. Your School
                    4. Your current year 
                    (i.e. 1.Don't bid for this mod, it is tiring, 3.SIS, 3. 2)"""
    mark = 3
    # print(response1)                                                                   ## 到最后 response1 还在、也许可以用来做点事
    return bot.sendMessage(chat_id, review_qns), mark

#######################################################################################################################################



bot = telepot.Bot("830250985:AAFeA-dy4mB1kXZbK_kBc6pBeT5xD7sqPu0")
MessageLoop(bot, on_chat_message).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)