
'''
This file contains all of the variables that need to be set for the bot to run.
A config file of sorts.
'''

import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Load GPT-2 model and tokenizer
model_path = "emily_yeppers_3.0"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.pad_token_id = tokenizer.eos_token_id
model = GPT2LMHeadModel.from_pretrained(model_path, pad_token_id=tokenizer.pad_token_id)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

crazy_factor = 1.2      # Keep high if you want her to act crazy
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
TARGET_PHRASES = ['emily yeppers', 'cum will win', 'olive juice']
subreddits = ['shittyaskreddit', 'AssCredit']
bot_mention = "u/EMILY\_YEPPERS"
relationships = {}      # Use this dictionary to make the bot behave differently with specific users