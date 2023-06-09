
'''
This file contains all of the variables that need to be set for the bot to run.
A config file of sorts.
'''

import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

# Load GPT-2 model and tokenizer
model_path = "maubers/emily_yeppers"
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.pad_token_id = tokenizer.eos_token_id
model = AutoModelForCausalLM.from_pretrained(model_path, pad_token_id=tokenizer.pad_token_id)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

crazy_factor = 1.3     # Keep high if you want her to act crazy
response_length = 150   # She will rant about cum forever at a higher temperature if you don't keep this lower

# Define list of words that neither prompts nor replies should contain
unwanted_words = ["disney", "applebees", "scientology", "scientologist", "scientologists", "applebee's"]
default_response = """
# CUM WILL WIN

"""

# Environment variables for authentication
clientID = os.environ["CLIENT_ID"]
clientSecret = os.environ["CLIENT_SECRET"]
userAgent = os.environ["USER_AGENT"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]


# Set the target phrase, subreddit, and user relationships
TARGET_PHRASES = ['emily yeppers', 'cum', 'olive juice']
trigger_pattern = r'\b(' + '|'.join(TARGET_PHRASES) + r')\b'
trigger_regex = re.compile(trigger_pattern, flags=re.IGNORECASE)
subreddits = ['testthewalrus', 'AssCredit', 'shittyaskreddit', 'Shittieraskreddit']
bot_mention = "u/EMILY\_YEPPERS"
shutup_mention = "shut the fuck up"
omit_phrases = ["serious eats", "instagram", "affiliate", "subscribe", "@"]
donotreply_users = ["EMILY_YEPPERS", "AutoModerator", "HippoBot9000", "radiantskie"]
relationships = {}      # Use this dictionary to make the bot behave differently with specific users
