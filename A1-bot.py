import slack
import os
from pathlib import Path
from dotenv import load_dotenv
# Import Flask
from flask import Flask,request,Response
import requests

# Handles events from Slack
from slackeventsapi import SlackEventAdapter

# Handle NLP for city recognition
import spacy

# Load the Token from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configure your flask application
app = Flask(__name__)
# Configure SlackEventAdapter to handle events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

# Using WebClient in slack, there are other clients built-in as well !!
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# Get Bot ID
BOT_ID = client.api_call("auth.test")['user_id']

# handling mention Events and echoing questions
@slack_event_adapter.on('app_mention')
def message(payload):
    print(payload)
    event = payload.get('event',{})
    user_id = event.get('user')
    channel_id = event.get('channel')
    if BOT_ID != user_id:
        text = event.get('text').replace("<@U01NXKV0F2S>", "").strip().capitalize() # strip the mention tag
        if text.endswith("?"):
            client.chat_postMessage(channel=channel_id, text=text)
        elif is_city_only(text):
            weather = get_weather(text)
            resp = "Current weather in {} {}".format(text, weather)
            client.chat_postMessage(channel=channel_id, text=resp)



nlp = spacy.load('en_core_web_lg')
def is_city_only(text):
    if len(text.split()) != 1:
        return False
    
    doc = nlp(text)
    return False if not doc.ents else True

weather_api = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
def get_weather(city):
    url = weather_api.format(city, os.environ['WAPI_KEY'])
    response = requests.request("GET", url)
    if response.ok:
        json = response.json()
        # print(json)
        resp_str = "feels like " + str(round(json['main']['feels_like'] - 273.15,2)) + " degrees celcius with " + json['weather'][0]['description'] + "."
        # print(resp_str)
        return resp_str
    
    return "is unknown."



# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True)