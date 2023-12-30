# P0: GroupMe Bot

## Overview

- create a GroupMe bot that will be able to read/respond to messages in a GroupMe chat

## Pre-Requisites

- `python3` installed
  - see [here](https://www.python.org/downloads/) for download
- GroupMe:
  - Account, sign up [here](https://groupme.com/en-US/register)
  - Bot, see how to create one [here](https://dev.groupme.com/tutorials/bots)
    - Group, join our class GroupMe [here](https://groupme.com/join_group/98324520/GpX1Owv6)

## Setup

```bash
# clone repo and cd into it
git clone <repo> && cd <repo>

# create virtual environment (this creates a folder called venv)
python3 -m venv venv

# activate virtual environment
source venv/bin/activate # for mac/linux
venv\Scripts\activate # for windows

# install dependencies
pip install -r requirements.txt
```

## Tasks

We have provided you with an outline of the bot in `bot.py` that is able to read/send messages to the GroupMe chat. Your task is to implement the following features:

- [ ] respond to **you**
  - you should be able to run your script and send a message in the GroupMe chat and have your bot respond to you and only you
    - hint: you should probably look at the [`sample.json`](./groupme-bot/sample.json) that shows what other fields you can extract from a response
- [ ] good morning/good night
  - if *anyone* says good morning/good night, your bot should respond with a good morning/good night with their name
    - i.e. if someone says "good morning", your bot should respond with "good morning, <name>"
    - think about how you're going to stop your bot from responding to itself and the other bots in the chat
    - **caution:** if you start spamming the chat, please `ctrl+c` your script to stop it
