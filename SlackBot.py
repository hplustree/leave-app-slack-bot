import logging
import slack_sdk
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime,date,time,timedelta
import schedule
import requests
import calendar
import constant
import time as tm
from UserID import user_id
from flask import Flask,request


app = Flask(__name__)
# Setup the env file and Log
logger = logging.getLogger(__name__)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Setup the Slackbot with client
client = slack_sdk.WebClient(token=os.environ['SLACK_TOKEN'])
LEAVE_API = os.environ['LEAVE_API']
API_KEY = os.environ['API_KEY']


LEAVE_CHANNEL= constant.LEAVE_CHANNEL
GENERAL_CHANNEL= constant.GENERAL_CHANNEL
BARKHA_ID= constant.BARKHA_ID
DHARMESH_ID= constant.DHARMESH_ID

# Set the time for every bot
presentday = date.today() 
currentYear = presentday.year


# BirthDay time
birthdayTime = time(hour=18,minute=10)
birthdayScheduleTime = int(datetime.combine(presentday, birthdayTime).timestamp())

# Work Anniversary time
workAnniversaryTime = time(hour=5,minute=30)
workAnniversaryScheduleTime = int(datetime.combine(presentday, workAnniversaryTime).timestamp())


# <!here> for @here
# <!channel> for @channel
# <!everyone> for @everyone
# <@UserId> for @User


# Return the day of the week
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


def birthdayWish(name):
    return f"<!channel> \n Today is {f'<@{user_id[name]}>' if name in user_id else name}'s birthday! \n From all of us here at the F(x), we wish you a very happy birthday & an  amazing year that ends with accomplishing all the great goals that you've set! \n May the days ahead be full of prosperity! \n \n Your contributions and commitment have made a significant impact on our success and we are grateful to have you as part of F(x) Team! \n Light the candles & uniquely enjoy this vital day using the fire of desires! Have a well deserved, thoroughly enjoyable birthday! \n Have a wonderful day! \n \n Once again, Happy Birthday! We look forward to continuing our work together and achieving more success in the future."


def workAnniversaryWish(name,totalYear):
    return f"<!channel> \nHappy work anniversary {f'<@{user_id[name]}>' if name in user_id else name}! \nWe want to take a moment to acknowledge and celebrate your {totalYear} work anniversary with F(x) Data Labs Pvt. Ltd. It's been an amazing journey working with you and we're fortunate to have someone with your talent and dedication on our team.\n\nYour hard work and commitment to excellence have not gone unnoticed. You have contributed significantly to the growth and success of our company, and we couldn't have come this far without your valuable contributions.\n\nWe appreciate your dedication, loyalty, and the positive impact you have made during your time with us. We are looking forward to working with you for many more years to come.\n\nCongratulations on this important milestone, and once again, thank you for everything you do."


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


def birthday_schedule_message():
    try:
        response = requests.get(f'{LEAVE_API}/slack-bot/birthday-request?token={API_KEY}')
        myresult = response.json();
    except requests.exceptions.HTTPError as errh:
            return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred" + repr(err)
    for result in myresult:
        client.chat_scheduleMessage(channel=GENERAL_CHANNEL,post_at=birthdayScheduleTime,text=birthdayWish(result['name']))

def work_anniversary_schedule_message():
    try:
        response = requests.get(f'{LEAVE_API}/slack-bot/work-anniversary-request?token={API_KEY}')
        myresult = response.json();
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred" + repr(err)
    for result in myresult:
        totalYear = currentYear - result['year']
        client.chat_scheduleMessage(channel=GENERAL_CHANNEL,post_at=workAnniversaryScheduleTime,text=workAnniversaryWish(result['name'],totalYear))

@app.route('/slack-bot/announcement',methods = ['POST'])
def announcement_schedule_message():
    content = request.get_json();
    result = content[0]
    client.chat_postMessage(channel=GENERAL_CHANNEL,text=f"<!channel> \n{result['description']}")
    return content

@app.route('/slack-bot/leave-request',methods = ['POST'])
def leave_schedule_messages():
    content = request.get_json();
    myresult = content[0]
    for result in myresult:
        client.chat_postMessage(channel=LEAVE_CHANNEL,text=switchType(type=result['req_type_id'],result=result))
    return content  



# Schedule Function to run everyday
schedule.every().day.at("05:25").do(birthday_schedule_message)
schedule.every().day.at("05:25").do(work_anniversary_schedule_message)


if(__name__== "__main__"):
    app.run()

# # To run script infinite time
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    tm.sleep(60)
