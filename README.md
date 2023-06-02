# emily_yeppers
A very mentally unwell Reddit bot

## Overview

This repository contains the code for Emily Yeppers, a bot who likes to talk about very inappropriate things and how vital they are to the existence of our species (the truth, technically) using GPT-2.  The bot streams new content from specified subreddits and responds when certain target phrases are detected in comments and submissions, or when it is mentioned or directly replied to.


## Setup and Installation

1. Clone this repository, of course.

2. Install the necessary Python libraries:

    `pip install -r requirements.txt`

3. Set up a Reddit app for the bot from your Reddit account's developer applications page. Ideally, create a new account for this. Click on 'Create App' or 'Create Another App', fill out the form, and note the 'client id' and 'client secret'. 

4. Update the bot_config.py file with your Reddit app's client id, client secret, your new bot's Reddit username and password, and the bot's user agent. The format for the user agent is something like 'python:EmilyYeppersBot:v3.0 (by u/<your reddit username>)'.

5. Execute the main script to start the bot:

    `python __main__.py`

  
## How the bot works

The bot streams new content from specified subreddits and enqueues items for processing. It checks comments and submissions for target phrases along with any direct replies to the bot. It also responds to mentions.

The bot uses OpenAI's GPT-2 model for generating responses. The responses are formatted and checked against a blacklist of unwanted words.

  
 ## Files

- \_\_main\_\_.py: Contains the main loop for the bot.
- bot_config.py: Contains the configuration for the bot, including Reddit API keys and target phrases.
- prompt_handler.py: Contains functions for processing prompts (comments or submissions).
- response_handler.py: Contains functions for generating and formatting responses.
- stream_handler.py: Contains functions for streaming new content from Reddit.

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.
This bot is a hobby project and is not officially affiliated with Reddit or OpenAI. 

  
## Support
  
If you have any questions or run into issues, please open an issue on this GitHub repository.
