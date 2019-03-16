import requests
import json
import datetime, time

my_token = '' # put your secret Telegram token here 
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
text = """Pls enter 1.Professor's name OR 2.Course code OR 3.Course name.
        Choose ONE of them with the index infront. 
        e.g. 1.Tan Hwee Xian OR 2.SMT203 OR 3.SCSM"""

def first_step():
    params = {"chat_id": chat_id, "text" : text}
    r = requests.post(url_sendMsg,params) 
    return r.json()

def vaildation_reply(msg):
    params = {"chat_id": chat_id, "text" : msg}
    r = requests.post(url_sendMsg,params) 
    return r.json()

def validate_first_response(response1):   ## way to get the response haven't written yet
    if response[0] == "2":
        if len(response1) != 7:
            msg = "Pls enter the correct format of Course code"
            return vaildation_reply(msg)
        else:
            cid = response[2:]
            return method_cid(cid)    ## incomplete vaildation...

def method_cid(cid):
    result = []
    ############# extra prof data from database
    return second_step(result) ## result will be a list of prof name

def second_step(result):     ## reply user with a list of prof name
    msg = "Pls indicate the INDEX of that prof \n"
    index = 1
    for i in result:
        msg = msg + index + i + "\n"
        index += 1
    params = {"chat_id": chat_id, "text" : msg}
    r = requests.post(url_sendMsg,params) 
    return r.json()    

def validate_second_response(response2):    ## way to get the response haven't written yet and need to think of a way to differentiate from first respond
    ## 看看怎么和上一个的 index 做下比较
    Try:
        response2 = int(response2)
        return third_step()
    Except:
        msg = "Pls indicate the correct index! Check your format."
        return vaildation_reply(msg)         ## still need changes


def third_step():
    review_qns = """ 

