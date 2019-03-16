import requests
import json
import datetime, time
import re

my_token = '782592193:AAGUgd3khDTWnymBdLx8co21UE9ihaIGFPg' # put your secret Telegram token here 
url_base = 'https://api.telegram.org/bot{}/'.format(my_token)

url_getMe = '{}getme'.format(url_base)
url_getUpdates = '{}getupdates'.format(url_base)
url_sendMsg = '{}sendMessage'.format(url_base)
url_editMsgText = '{}editMessageText'.format(url_base)
url_delMsg = '{}deleteMessage'.format(url_base)

url_sendPhoto = '{}sendPhoto'.format(url_base)
url_sendDoc = '{}sendDocument'.format(url_base)
url_sendSticker = '{}sendSticker'.format(url_base)

########################################################
chat_id = "386055474" ## this need to extract from database
# text = """Pls enter 1.Professor's name OR 2.Course code OR 3.Course name.
#         Choose ONE of them with the index infront. 
#         (i.e 1.Tan Hwee Xian OR 2.SMT203 OR 3.SCSM)"""
def vaildation_reply(msg):
    params = {"chat_id": chat_id, "text" : msg}
    r = requests.post(url_sendMsg,params) 
    return r.json()

# response1 = "cid"
# step_2(response1)
# def step_2(response1):  ## this need to check what kinds of response from button (need edition)
#     if response1 == "cid":
#         msg = "Pls enter course code"
#     elif response1 == "cname":
#         msg = "Pls enter course name"
#     elif response1 == "pname":
#         msg = "Pls enter course name"
#     vaildation_reply(msg)
#     return response1                              ## this step is just to check user click on which button


response2 = "SMT203" ## this need to get from user 
def step_2_vaildation(response2):
    if response1 == "cid":
        if response2.isalpha() or response2.isdigit():
            msg = "Pls enter the correct format of Course code"
            return vaildation_reply(msg)
        else:
            return step_3(response2)
    if response1 == "cname":
        cname_without_space =response2.replace(" ", "")
        if cname_without_space.isalpha():
            return step_3(response2)               ## cname may not be complete and contain space
        else:
            msg = "Pls enter the correct format of course name"
            return vaildation_reply(msg)
    if response1 == "pname":
        pname_without_space = response2.replace(" ", "")
        if pname_without_space.isalpha():
            return step_3(response2)     ## pname contains space e.g "Tan Hwee Xian"
        else:
            msg = "Pls enter the correct format of Prof name"
            return vaildation_reply(msg)


def step_3(response2):  ## vaildate the input and start calling API
    prof_list = []
    ## call our Course API and retrieve corresponding prof and append into prof_list
    if prof_list == []:
        msg = "Pls check your input"
        return vaildation_reply(msg)
    return prof_list


response3 = "1"      ## 如果是给一个list的名字    # assume we don't have button for this
def step_3_validation(response3):               #
    if len(response3) != 1:                     #
        msg = "Pls indicate the correct index"  #
        return vaildation_reply(msg)            #
    try:                                        #
        response3 = int(response3)              #
        return step_4()                         #
    except:                                     #
        msg = "Pls indicate the correct index"  #
        return vaildation_reply(msg)            ## This will change base on whether we can do button or not

def step_4():
    review_scores = """ Please provide scores based on 'Clarity of Teaching', 'Workload', 'Grading Fairnes'.(i.e. 3.5,4,5) """
    params = {"chat_id": chat_id, "text" : review_scores}
    r = requests.post(url_sendMsg,params) 
    return r.json() 

def step_5():         ## may change to better way...
    review_qns = """Following questions are optional.
                    1. Any further comment?
                    2. Any advice for prof to improve?
                    3. Your School
                    4. Your current year 
                    (i.e. 1.Don't bid for this mod, it is tiring, 3.SIS, 3. 2)"""
    params = {"chat_id": chat_id, "text" : review_qns}
    r = requests.post(url_sendMsg,params) 
    return r.json()    