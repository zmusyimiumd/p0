import requests
import time
import json
import os
import datetime

from dotenv import load_dotenv

load_dotenv()

BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
MY_S_ID = "91579416"
LAST_MESSAGE_ID = None

def get_nfl_playoff_schedule():

    return [
    {
        "NFL Playoffs Round": 1,
        "Away Team": "Cleveland Browns",
        "Home Team": "Houston Texans",
        "Date Time": "2024-01-13T16:30:00"
    },
    {
        "NFL Playoffs Round": 1,
        "Away Team": "Miami Dolphins",
        "Home Team": "Kansas City Chiefs",
        "Date Time": "2024-01-13T20:00:00"
    },
    {
        "NFL Playoffs Round": 1,
        "Away Team": "Pittsburgh Steelers",
        "Home Team": "Buffalo Bills",
        "Date Time": "2024-01-14T13:00:00"
    },
    {
        "NFL Playoffs Round": 1,
        "Away Team": "Green Bay Packers",
        "Home Team": "Dallas Cowboys",
        "Date Time": "2024-01-14T16:30:00"
    },
    {
        "NFL Playoffs Round": 1,
        "Away Team": "Los Angeles Rams",
        "Home Team": "Detroit Lions",
        "Date Time": "2024-01-14T20:00:00"
    },
    {
        "NFL Playoffs Round": 1,
        "Away Team": "Philadelphia Eagles",
        "Home Team": "Tampa Bay Buccaneers",
        "Date Time": "2024-01-15T20:00:00"
    }
]

def send_message(text, attachments=None):
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    response = requests.post(post_url, json=data)
    return response.status_code == 202


def get_group_messages(since_id=None):
    """Retrieve recent messages from the group."""
    params = {"token": ACCESS_TOKEN}
    if since_id:
        params["since_id"] = since_id

    get_url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
    response = requests.get(get_url, params=params)
    if response.status_code == 200:
        return response.json().get("response", {}).get("messages", [])
    return []

def format_schedule_message(schedule):
    message_lines = []
    for game in schedule:
        game_time = datetime.datetime.fromisoformat(game["Date Time"])
        formatted_time = game_time.strftime("%H:%M")
        line = f"NFL Playoffs Round {game['NFL Playoffs Round']}: {game['Away Team']} at {game['Home Team']}, Time: {formatted_time}"
        message_lines.append(line)
    return "\n".join(message_lines)

def process_message(message):
    """Process and respond to a message."""
    global LAST_MESSAGE_ID
    text = message["text"].lower()
    s_id = message["sender_id"]

    if s_id == BOT_ID:
        return
    
    if s_id == MY_S_ID:
        if "good morning" in text:
            send_message(f"Good morning, {message['name']}!")
        elif "good night" in text:
            send_message(f"Good night, {message['name']}!")
     
        if "hello bot" in text:
            send_message("sup")

        if "bot, nfl schedule for" in text:
            requested_date = text.split("for ")[-1].strip() 
            try:
                requested_date = datetime.datetime.strptime(requested_date,"%Y-%m-%d").date()
                schedule =get_nfl_playoff_schedule()
                filtered_schedule =[game for game in schedule if datetime.datetime.fromisoformat(game["Date Time"]).date()== requested_date]
                if filtered_schedule:
                    schedule_message = format_schedule_message(filtered_schedule)
                    send_message(schedule_message)
                else:
                    send_message(f"No games found for {requested_date.strftime('%Y-%m-%d')}.")
            except ValueError:
                send_message("Please provide a valid date in the YYYY-MM-DD format.")
        return

def main():
    global LAST_MESSAGE_ID
    while True:
        messages = get_group_messages(LAST_MESSAGE_ID)
        for message in reversed(messages):
            if message["id"]!= LAST_MESSAGE_ID:
                process_message(message)
                LAST_MESSAGE_ID = message["id"]
        time.sleep(10)


if __name__ == "__main__":
    main()
