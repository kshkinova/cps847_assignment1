import slack
import os
from pathlib import Path
from dotenv import load_dotenv
# Import Flask
from flask import Flask,request,Response
import requests

# Handles events from Slack
from slackeventsapi import SlackEventAdapter

# Load the Token from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configure your flask application
app = Flask(__name__)
# Configure SlackEventAdapter to handle events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

# Using WebClient in slack, there are other clients built-in as well !!
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# connect the bot to the channel in Slack Channel
#client.chat_postMessage(channel='#cps-847-course', text='Send Message Demo')

# Get Bot ID
BOT_ID = client.api_call("auth.test")['user_id']

# Modify to perform weather API request
# url='https://geek-jokes.sameerkumar.website/api'
# @app.route('/joke', methods=['GET','POST'])
# def joke():
#     data = request.form
#     channel_id = data.get('channel_id')
#     response = requests.request("GET", url)
#     print(response.text)
#     client.chat_postMessage(channel=channel_id, text=response.text)
#     return Response(), 200

# handling Message Events
# @slack_event_adapter.on('message')
# def message(payload):
#     print(payload)
#     event = payload.get('event',{})
#     user_id = event.get('user')
#     channel_id = event.get('channel')
#     if BOT_ID != user_id:
#         text = event.get('text')
#         if text.endswith("?"):
#             resp = "Good question. " + text.capitalize()
#             client.chat_postMessage(channel=channel_id, text=resp)

# handling mention Events and echoing questions
@slack_event_adapter.on('app_mention')
def message(payload):
    print(payload)
    event = payload.get('event',{})
    user_id = event.get('user')
    channel_id = event.get('channel')
    if BOT_ID != user_id:
        text = event.get('text')
        if text.endswith("?"):
            resp = "You talking to me? " + text.capitalize().replace("<@u01nxkv0f2s>", "")
            print(resp)
            client.chat_postMessage(channel=channel_id, text=resp)



# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True)