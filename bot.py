import time
import threading
import telepot
import telegram
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop
import requests
from hashids import Hashids
hashids = Hashids()
## Current Problem faced:
## 1. I have declared the global variables (mark) but when I update them in the later on functions, it does not change...
## 2. line 38 will the the chat_id but I have to pass it as a parameter to other functions instead of letting it become a global variable.
## 3. Because it is very hard to differentiate what the user inputs so we didn't do much vaildation and assuming user can follow the correct format all the way.
## 4. If the user input part of the Prof name/ course name, our API will Post for them and return the possible output for them to choose. But because of problem 3, 
##    it is very hard to achieve this function
## p.s. We have link this bot to our api so from line 113-129 will be hard code for now.

#################################################
## response1: which method user want to use
## response2: pname/ cname/ cid             #user input          
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
getprofcourse = "http://smt203-project-team1.herokuapp.com/getprofcourse"
postReview = "http://smt203-project-team1.herokuapp.com/postreview"
getreview = "http://smt203-project-team1.herokuapp.com/getreview"
pname = ''
cname = ''
scores = []
score1 = 0.0
score2 = 0.0
score3 = 0.0
comment = ''
advice = ''
school = ''
year = 1
# chat_id = "386055474" ## this need to extract from database

#continuous listen
def on_chat_message(msg):
    # chat_id = msg['chat']["id"]
    content_type, chat_type, chat_id = telepot.glance(msg)                
    print('Chat:', content_type, chat_type, chat_id)                                                                 
    if content_type != 'text':                                            
        return                                                     
    global response1                                                     
    global response2
    global response3
    global mark                                                       ## 问题： 后面要是改 var 貌似没有用啊！！！！！！！！
    response = msg['text']
    if response == '/review':#review profs
        markup = ReplyKeyboardMarkup(keyboard=[
                     ['Post by Course ID', KeyboardButton(text='Post by Course Name')],
                     [KeyboardButton(text = "Post by Professor Name")],
                 ])
        bot.sendMessage(chat_id, 'Please indicate which methods would you like to use', reply_markup=markup)
        mark = 0
    elif response == '/search':#search reviews
        markup = ReplyKeyboardMarkup(keyboard=[
                     ['Search by Course ID', KeyboardButton(text='Search by Course Name')],
                     [KeyboardButton(text = "Search by Professor Name")],
                 ])
        bot.sendMessage(chat_id, 'Please indicate which methods would you like to use', reply_markup=markup)
        mark = 0.5                    
    elif response[:4] == "Post" and mark==0:#first selection of Post by what                                        
        response1 = response
        step_2(response1, chat_id)
    elif response[:6] == "Search" and mark==0.5:#first selection of search by what                                        
        response1 = response
        search_step_2(response1, chat_id) 
    elif mark == 1:#select prof or course
        response3 = response 
        step_4(response3, chat_id)
    elif mark == 1.5:#get mod review by courses
        response3 = response
        get_modreview(response1, response3, chat_id)     
    elif mark == 2:#give score base on the selection
        response4 = response
        scores = response4
        scoreValidation(scores,chat_id)
    elif mark == 3:#give comment and finish score review
        response5 = response
        step_6_1(response5, chat_id)
    elif mark == 4:#ask and give advice else skip
        response6 = response
        step_6_2(response6, chat_id)
    elif mark == 5:
        response7 = response
        step_6_3(response7, chat_id)
    elif mark == 6:
        response8 = response
        step_6_4(response8, chat_id)
    elif response1 != "" and mark == 0:    
        response2 = response
        step_2_vaildation(response2, response1, chat_id)
    elif response1 != "" and mark == 0.5:    
        response2 = response
        get_step_2_vaildation(response2, response1, chat_id)
    elif response == 'h' or mark == 10:
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)

#######################################################################################################################################
def search_step_2(response1, chat_id):
    if response1 == "Search by Course ID":
        msg = "Please enter course code"
    elif response1 == "Search by Course Name":
        msg = "Please enter course name"
    elif response1 == "Search by Professor Name":
        msg = "Please enter professor name"
    return validation_reply(msg, chat_id)
    
def validation_reply(msg, chat_id):
    return bot.sendMessage(chat_id, msg, parse_mode=telegram.ParseMode.MARKDOWN)

def step_2(response1, chat_id):  
    if response1 == "Post by Course ID":
        msg = "Please enter course code"
    elif response1 == "Post by Course Name":
        msg = "Please enter course name"
    elif response1 == "Post by Professor Name":
        msg = "Please enter professor name"
    
    return validation_reply(msg, chat_id)                              ## this step is just to check user click on which button and give corresponding respond

def get_step_2_vaildation(response2, response1, chat_id):
    global mark
    if response1 == "Search by Course ID":
        if response2.isalpha() or response2.isdigit():
            msg = "Please enter the correct format of Course code"
            return validation_reply(msg, chat_id)
        else:
            return get_step_3(response2, response1, chat_id)
    if response1 == "Search by Course Name":
        cname_without_space =response2.replace(" ", "")
        if cname_without_space.isalpha():
            return get_step_3(response2, response1, chat_id)              ## cname may not be complete and contain space
        else:
            msg = "Please enter the correct format of course name"
            return validation_reply(msg, chat_id)
    if response1 == "Search by Professor Name":
        pname_without_space = response2.replace(" ", "")
        if pname_without_space.isalpha():
            return get_step_3(response2, response1, chat_id)     ## pname contains space e.g "Tan Hwee Xian"
        else:
            msg = "Please enter the correct format of Prof name"
            return validation_reply(msg, chat_id)

# response2 = "SMT203" ## this need to get from user 
def step_2_vaildation(response2, response1, chat_id):
    if response1 == "Post by Course ID":
        if response2.isalpha() or response2.isdigit():
            msg = "Please enter the correct format of Course code"
            return validation_reply(msg, chat_id)
        else:
            return step_3(response2, response1, chat_id)
    if response1 == "Post by Course Name":
        cname_without_space =response2.replace(" ", "")
        if cname_without_space.isalpha():
            return step_3(response2, response1, chat_id)              ## cname may not be complete and contain space
        else:
            msg = "Please enter the correct format of course name"
            return validation_reply(msg, chat_id)
    if response1 == "Post by Professor Name":
        pname_without_space = response2.replace(" ", "")
        if pname_without_space.isalpha():
            return step_3(response2, response1, chat_id)     ## pname contains space e.g "Tan Hwee Xian"
        else:
            msg = "Please enter the correct format of Prof name"
            return validation_reply(msg, chat_id)

#what are the things to show in getreview...
def get_step_3(response2, response1, chat_id):
    global mark
    url = getreview
    result = []
    try:
        if response1 == "Search by Course ID": 
            params = {"cid": response2}
            request = requests.get(url=url,params=params)
            for i in request.json():
                result.append(i)
            mark = 10
            msg = 'Here are the reviews on course {0}'.format(response2)
            return validation_reply(result, chat_id), mark
        elif response1 == "Search by Course Name":
            params = {"cname": response2}
            request = requests.get(url=url,params=params)
            for i in request.json():
                result.append(i)
            mark = 10
            msg = 'Here are the reviews on course {0}'.format(response2)
            return validation_reply(result, chat_id), mark
    except:
        msg = "Please check your input"
        mark = 0.5
        return validation_reply(msg, chat_id), mark
##############################################################################################
#call api append result to l
def step_3(response2, response1, chat_id):  ## vaildate the input and start calling API          
    global mark
    global cname
    global pname
    l = []
    url = getprofcourse
    try:
        if response1 == "Post by Course ID": 
            params = {"cid": response2}
            request = requests.get(url=url,params=params)
            for i in request.json():
                l.append(i["professor"])
                cname = i["course"]
        elif response1 == "Post by Course Name":
            params = {"cname": response2}
            cname = response2
            request = requests.get(url=url,params=params)
            for i in request.json():
                l.append(i["professor"])
        elif response1 == "Post by Professor Name":
            params = {"pname": response2}
            pname = response2
            request = requests.get(url=url,params=params)
            for i in request.json():
                l.append(i["course"])
        mark = 1
        msg = 'Please indicate which professor/course you want to review.'
        return send_list(l, msg, chat_id), mark, cname, pname
    except:
        msg = "Please check your input"
        mark = 0
        return validation_reply(msg, chat_id), mark
#############################################################################################################
#prof buttons or couse name
def send_list(l, msg, chat_id):
    keyboard = []
    for i in l:
        z = []
        x = i
        z.append(x)
        keyboard.append(z)
    markup = ReplyKeyboardMarkup(keyboard=keyboard)
    return bot.sendMessage(chat_id, msg, reply_markup=markup,parse_mode=telegram.ParseMode.MARKDOWN)

# response3 = "xxx"      ## base on which button user select
#score
def step_4(response3, chat_id):
    global mark
    global cname
    global pname
    if response1 == "Post by Course ID":
        pname = response3
    elif response1 == "Post by Course Name":
        cname = response3
    review_scores = """
    Please provide scores between 0 to 5 based on
    -*Clarity of Teaching*
    -*Workload*
    -*Grading Fairnes*
    For example:
    Clarity of Teching has 3.5. Workload has 4. And Grading has 5.
    Just enter: *3.5,4,5* """
    mark = 2
    return bot.sendMessage(chat_id, review_scores, parse_mode=telegram.ParseMode.MARKDOWN), mark, pname, cname

#convert to button
def step_5(chat_id): 
    global mark
    mark = 3
    #return bot.sendMessage(chat_id, review_qns), mark
    msg = "Following questions are optional. Please simply provide the information or press 'Skip' to skip the question."
    l = ["Skip Further comment"]
    msg = "Please enter further comment for the prof or course if any."
    return send_list(l, msg, chat_id), mark

def step_6_1(response5, chat_id):
    global mark
    global comment
    l = ["Skip for advice"]
    msg = "Please enter your advice for prof to improve if any."
    try:
        if response5 == "Skip Further comment":
            comment = ''
            mark = 4
            return send_list(l, msg, chat_id),mark, comment
        else:
            comment = response5
            mark = 4
            return send_list(l, msg, chat_id), mark, comment
    except:
        msg = response5
        mark = 3
        return validation_reply(msg, chat_id), mark

def step_6_2(response6, chat_id):
    global mark
    global advice
    l = ["Skip entering school"]
    msg = "Please enter your school. E.g. *SIS*"
    try:
        if response6 == "Skip for advice":
            advice = ''
            mark = 5
            return send_list(l, msg, chat_id),mark, advice
        else:
            advice = response6
            mark = 5
            return send_list(l, msg, chat_id),mark, advice
    except:
        msg = response6
        mark = 4
        return validation_reply(msg, chat_id), mark

def step_6_3(response7, chat_id):
    global mark
    global school
    l = ["Skip entering current year."]
    msg = "Please enter your current year in integer. E.g. *3*"
    schools = ['SIS','SOE','SOB','SOA','SOSS']
    try:
        if response7 == "Skip entering school":
            school = ''
            mark = 6
            return send_list(l, msg, chat_id),mark, school
        else:
            school = response7
            if school in schools:
                mark = 6
                return send_list(l, msg, chat_id),mark, school
            else:
                mark = 5
                msg = "Please enter your school. E.g. *SIS,SOE,SOB,SOA,SOSS*"
                return validation_reply(msg, chat_id), mark
    except:
        msg = response7
        mark = 5
        return validation_reply(msg, chat_id), mark

def step_6_4(response8, chat_id):
    global mark
    global year
    msg = "That's all for the review. Thank you."
    try:
        if response8 == "Skip entering current year.":
            year = ''
            mark = 10
            postReview(chat_id, pname, cname, score1, score2, score3, comment, advice, school, year)
            return validation_reply(msg, chat_id), mark, year
        else:
            try:
                year = int(response8)
            except:
                msg = "Please enter a integer"
                mark = 6
                return validation_reply(msg, chat_id), mark
            if(year < 1 or year>=6):
                msg = "Please enter a between 1 to 6"
                mark = 6
                return validation_reply(msg, chat_id), mark
            else:
                mark = 10
                postReview(chat_id, pname, cname, score1, score2, score3, comment, advice, school, year)
                return validation_reply(msg, chat_id), mark, year
    except:
        msg = "Something goes wrong..."
        mark = 6
        return validation_reply(msg, chat_id), mark

#check score input within 0 to 5
def scoreValidation(scores,chat_id):
    global mark
    global score1
    global score2
    global score3
    try:
        scores = scores.split(',')
        score1 = float(scores[0])
        score2 = float(scores[1])
        score3 = float(scores[2])
    except:
        msg = "Please provide three scores."
        return validation_reply(msg, chat_id), mark
    if(score1<0 or score2<0 or score3<0):
        msg = "Score could not be less than 0. Please enter your score again."
        mark = 2
        return validation_reply(msg, chat_id), mark
    elif(score1>5 or score2>5 or score3>5):
        msg = "Score could not be larger than 5. Please enter your score again."
        mark = 2
        return validation_reply(msg, chat_id), mark
    else:
        mark = 3
        msg = "Thank you for your score review"
        validation_reply(msg, chat_id)
        return step_5(chat_id), score1, score2, score3

def postReview(chat_id, pname, cname, score1, score2, score3, comment, advice, school, year):
    hashid = hashids.encode(chat_id)
    #ints = hashids.decode('xoz') #decode
    json = {"reviewer": hashid, "pname":pname, "cname":cname, "score1":score1, "score2":score2, "score3":score3, "comment":comment, "advice":advice, "school":school, "year":year}
    postReview = "http://smt203-project-team1.herokuapp.com/postreview"
    request = requests.post(url=postReview,json=json)
    mark = 10
    msg = """Prof *{0}* in *{1}* got scores *{2}* for Clarity *{3}* for Workload *{4}* for Grading with comment: *{5}* and advice: *{6}*. 
You are in year *{8}* from *{7}* .""".format(pname,cname,score1, score2, score3, comment, advice, school, year)
    return validation_reply(msg, chat_id), mark

###################################################################################################################################
#bot = telepot.Bot("830250985:AAFeA-dy4mB1kXZbK_kBc6pBeT5xD7sqPu0")
bot = telepot.Bot("864405474:AAGgINrELijqpInkrosYc-kAN-ImsQmVKbE")
MessageLoop(bot, on_chat_message).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)