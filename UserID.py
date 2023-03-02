import logging
import slack_sdk
from slack_sdk.errors import SlackApiError
import os
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack_sdk.WebClient(token=os.environ['SLACK_TOKEN'])

# Put users into the dict
def save_users(users_array):
    for user in users_array:
        # Key user info on their unique user ID
        user_name = user['profile']['real_name']
        # print(user['profile']['real_name'])
        # Store the entire user object (you may not need all of the info)
        users_store[user_name] = user["id"]
try:
    # Call the users.list method using the WebClient
    # users.list requires the users:read scope
    users_store = {}
    result = client.users_list()
    save_users(result["members"])

except SlackApiError as e:
    logger.error("Error creating conversation {}",format(e))
