import logging
import slack_sdk
from slack_sdk.errors import SlackApiError
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import calendar
import constant
from UserID import user_id
from flask import Flask,request

app = Flask(__name__)
# Setup the env file and Log
logger = logging.getLogger(__name__)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Setup the Slackbot with client
client = slack_sdk.WebClient(token=os.environ['SLACK_TOKEN'])

LEAVE_CHANNEL= constant.LEAVE_CHANNEL
GENERAL_CHANNEL= constant.GENERAL_CHANNEL
BARKHA_ID= constant.BARKHA_ID
DHARMESH_ID= constant.DHARMESH_ID

def findDay(date):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    return (calendar.day_name[date.weekday()])

def casualLeave(name,start_date,end_date,reason):
    if(start_date==end_date):
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking leave on {start_date} [{findDay(start_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"
    else:
        return f"This is to inform you that,{f'<@{user_id[name]}>' if name in user_id else name} will be taking leave on {start_date} [{findDay(start_date)}] to {end_date} [{findDay(end_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"

def earnedLeave(name,start_date,end_date,reason):
    if(start_date==end_date):
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking leave on {start_date}[{findDay(start_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"
    else:
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking leave on {start_date}[{findDay(start_date)}] to {end_date} [{findDay(end_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"


def unpaidLeave(name,start_date,end_date,reason):
    if(start_date==end_date):
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking leave on {start_date}[{findDay(start_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"
    else:
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking leave on {start_date}[{findDay(start_date)}] to {end_date} [{findDay(end_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"


def adjustmentLeave(name,start_date,end_date,reason,adjustment_date):
    if(start_date==end_date):
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking adjustment leave on{start_date}[{findDay(start_date)}],\n will adjustment date:-{adjustment_date} \n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"
    else:
       return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking adjustment leave on{start_date}[{findDay(start_date)}] to {end_date} [{findDay(end_date)}],\n will adjustment date:-{adjustment_date} \n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"

def altermateShift(name,start_date,end_date,reason,alternate_shift):
    if(start_date==end_date):
       return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be doing alternate shift on {start_date}[{findDay(start_date)}].\n Alternate Shfit Time :- {alternate_shift} \n Reason:-{reason}\n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"
    else:
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be doing alternate shift on {start_date}[{findDay(start_date)}] to {end_date} [{findDay(end_date)}].\n Alternate Shfit Time :-{alternate_shift} \n Reason:-{reason}\n  <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"

def halfdayLeave(name,start_date,end_date,reason):
    if(start_date==end_date):
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking half-day leave on {start_date} [{findDay(start_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"
    else:
        return f"This is to inform you that,{f'<@{user_id[name]}>' if name in user_id else name} will be taking half-day leave on {start_date} [{findDay(start_date)}] to {end_date} [{findDay(end_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"

def switchType(type,result):
    name =result['name']
    start_date = result['start_date']
    end_date=result['end_date']
    reason = result['reason']
    adjustment_date =result['adjustment_date']
    half_leave_time=result['half_leave_time']
    is_half_leave=result['is_half_leave']
    if ((type==1 or type==2 or type==5 or type==3) and is_half_leave==1):
        return halfdayLeave(name,start_date,end_date,reason)
    elif type==1:
       return casualLeave(name,start_date,end_date,reason)
    elif type==3:
       return earnedLeave(name,start_date,end_date,reason)
    elif type==4:
        return adjustmentLeave(name,start_date,end_date,reason,adjustment_date)
    elif type==5:
       return unpaidLeave(name,start_date,end_date,reason)
    elif type==6:
        return altermateShift(name,start_date,end_date,reason,half_leave_time)


@app.route('/slack-bot/announcement',methods = ['POST'])
def announcement_message():
    content = request.get_json();
    result = content[0]
    try:
        client.chat_postMessage(channel=GENERAL_CHANNEL,text=f"<!channel> \n{result['description']}")
    except SlackApiError as e:
            logger.error("Error creating conversation {}",format(e))

    return content

@app.route('/slack-bot/leave-request',methods = ['POST'])
def leave_message():
    content = request.get_json();
    myresult = content[0]
    for result in myresult:
        try:
            client.chat_postMessage(channel=LEAVE_CHANNEL,text=switchType(type=result['req_type_id'],result=result))
        except SlackApiError as e:
            logger.error("Error creating conversation {}",format(e))

    return content  



if(__name__== "__main__"):
    app.run(debug=True)