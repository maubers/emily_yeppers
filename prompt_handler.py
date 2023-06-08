'''
This file contains functions that format the prompt before it is passed to the GPT-2 model.
This makes it easier for the bot to understand what the user is saying, not that she listens well.
I think she just likes the sound of her own voice.
add_default_phrase probably has a major impact on that.
'''
from bot_config import *

import re
import string

def strip_user_mentions(prompt):
    pattern = r"\[u/[a-zA-Z0-9]+\\_[a-zA-Z0-9]+\]"
    prompt = re.sub(pattern, '', prompt, flags=re.IGNORECASE)
    return prompt


def strip_urls(prompt):
    return re.sub(r'http\S+', '', prompt)


def add_punctuation(prompt):
    if prompt[-1] not in string.punctuation:
        prompt += "."
    return prompt


def process_sentences(prompt):
    sentences = re.findall(r'[^.!?]+[.!?]', prompt)

    new_sentences = []
    for sentence in sentences:
        stripped_sentence = sentence.strip()

        if len(stripped_sentence) > 0:
            new_sentences.append(stripped_sentence)

    return " ".join(new_sentences)


def remove_unwanted_characters(prompt):
    # Remove newline and carriage return characters
    prompt = prompt.replace('\n', ' ').replace('\r', ' ')

    # Remove any random punctuation at the beginning of the sentence
    prompt = prompt.lstrip(string.punctuation + ' ')

    # Add punctuation to the end of the prompt if none is found
    if prompt and prompt[-1] not in string.punctuation:
        prompt += "."

    return prompt


def add_relationship(prompt, user):
    for related_user, relationship in relationships.items():
        if related_user.lower() == user.lower():
            prompt = f"{prompt}. I am {relationship}."
    return prompt


# This is the part that makes her extra obsessed with cum. She's already bad enough without it
# This just ensures that she never shuts up about cum
def add_default_phrase(prompt):
    prompt += " Cum will absolutely win. Everyone loves cum. Don't you just love cum? I'm horny."
    return prompt


def format_prompt(prompt, user):
    prompt = strip_user_mentions(prompt)
    prompt = strip_urls(prompt)
    prompt = add_punctuation(prompt)
    prompt = process_sentences(prompt)
    prompt = remove_unwanted_characters(prompt)
    prompt = add_relationship(prompt, user)
    prompt = add_default_phrase(prompt)

    return prompt
