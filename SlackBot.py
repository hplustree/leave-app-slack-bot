import logging
import slack_sdk
from slack_sdk.errors import SlackApiError
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

announcement_id=[]

# Leave time
leaveTime = time(hour=12, minute=30)
leaveScheduleTime = int(datetime.combine(presentday, leaveTime).timestamp())
# BirthDay time
birthdayTime = time(hour=5,minute=30)
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
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking leave on {start_date} [{findDay(start_date)}] to {end_date} [{findDay(end_date)}].\n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"

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

def alternateShift(name,start_date,end_date,reason,alternate_shift):
    if(start_date==end_date):
       return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be doing alternate shift on {start_date}[{findDay(start_date)}].\n Alternate Shift Time :- {alternate_shift} \n Reason:-{reason}\n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"
    else:
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be doing alternate shift on {start_date}[{findDay(start_date)}] to {end_date} [{findDay(end_date)}].\n Alternate Shift Time :-{alternate_shift} \n Reason:-{reason}\n  <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"

def halfdayLeave(name,start_date,end_date,reason,half_leave_time):
    if(start_date==end_date):
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking half-day leave on {start_date} [{findDay(start_date)}].\n Half-day Time:- {half_leave_time} \n Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"
    else:
        return f"This is to inform you that, {f'<@{user_id[name]}>' if name in user_id else name} will be taking half-day leave on {start_date} [{findDay(start_date)}] to {end_date} [{findDay(end_date)}].\n Half-day Time:- {half_leave_time} \n  Reason:- {reason} \n <!here> <@{BARKHA_ID}> <@{DHARMESH_ID}>"

def birthdayWish(name):
    return f"<!channel> \n Today is {f'<@{user_id[name]}>' if name in user_id else name}'s birthday! \n From all of us here at the F(x), we wish you a very happy birthday & an  amazing year that ends with accomplishing all the great goals that you've set! \n May the days ahead be full of prosperity! \n \n Your contributions and commitment have made a significant impact on our success and we are grateful to have you as part of F(x) Team! \n Light the candles & uniquely enjoy this vital day using the fire of desires! Have a well deserved, thoroughly enjoyable birthday! \n Have a wonderful day! \n \n Once again, Happy Birthday! We look forward to continuing our work together and achieving more success in the future."


def workAnniversaryWish(name,totalYear):
    return f"<!channel> \nHappy work anniversary {f'<@{user_id[name]}>' if name in user_id else name}! \nWe want to take a moment to acknowledge and celebrate your {totalYear} work anniversary with F(x) Data Labs Pvt. Ltd. It's been an amazing journey working with you and we're fortunate to have someone with your talent and dedication on our team.\n\nYour hard work and commitment to excellence have not gone unnoticed. You have contributed significantly to the growth and success of our company, and we couldn't have come this far without your valuable contributions.\n\nWe appreciate your dedication, loyalty, and the positive impact you have made during your time with us. We are looking forward to working with you for many more years to come.\n\nCongratulations on this important milestone, and once again, thank you for everything you do."

def announcementId(id):
    for _id in announcement_id:
        if(_id == id):
            break;
    else:
        announcement_id.append(id)
        return False
    return True

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
        return alternateShift(name,start_date,end_date,reason,half_leave_time)


def leave_schedule_messages():
    try:
        response = requests.get(f'{LEAVE_API}/slack-bot/leave-request?token={API_KEY}')
        myresult =response.json()
    except requests.exceptions.HTTPError as errh:
            return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred" + repr(err)
    for result in myresult:
        try:
            client.chat_scheduleMessage(channel=LEAVE_CHANNEL,post_at=leaveScheduleTime,text=switchType(type=result['req_type_id'],result=result))
        except SlackApiError as e:
            logger.error("Error creating conversation {}",format(e))

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
        try:
            client.chat_scheduleMessage(channel=GENERAL_CHANNEL,post_at=birthdayScheduleTime,text=birthdayWish(result['name']))
        except SlackApiError as e:
            logger.error("Error creating conversation {}",format(e))

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
        try:
            client.chat_scheduleMessage(channel=GENERAL_CHANNEL,post_at=workAnniversaryScheduleTime,text=workAnniversaryWish(result['name'],totalYear))
        except SlackApiError as e:
            logger.error("Error creating conversation {}",format(e))

def announcement_schedule_message():
    try:
        response = requests.get(f'{LEAVE_API}/slack-bot/announcement-request?token={API_KEY}')
        myresult = response.json();
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred" + repr(err)
    announcementScheduleTime = int((datetime.now() + timedelta(minutes=1)).timestamp())
    for result in myresult:
        if(announcementId(result['id'])):
            continue;
        else:
            try:
                client.chat_scheduleMessage(channel=GENERAL_CHANNEL,post_at=announcementScheduleTime,text=f"<!channel> \n{result['description']}")
            except SlackApiError as e:
                logger.error("Error creating conversation {}",format(e))

# Schedule Function to run everyday
schedule.every().day.at("05:25").do(birthday_schedule_message)
schedule.every().day.at("12:25").do(leave_schedule_messages)
schedule.every().day.at("05:25").do(work_anniversary_schedule_message)


# Run every minute
schedule.every().minute.do(announcement_schedule_message)


# To run script infinite time
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    tm.sleep(1)
