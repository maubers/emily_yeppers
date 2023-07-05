'''
This file contains the main response generation function. It takes in a prompt and generates a 
response using the GPT-2 model. 
'''
from bot_config import *
from prompt_handler import format_prompt
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def create_gpt_response(prompt):
    print("Generating response for prompt:", prompt)

    print("Checking prompt against blacklist")
    # Check if the prompt contains unwanted words. If it does, return the default response.
    for word in unwanted_words:
        if word in prompt.lower():
            print(f"Blacklisted word detected: {word}. Returning default response.")
            
            if word == "applebees" or word == "applebee's":
                return "I FUCKING HATE APPLEBEE'S! SHUT THE FUCK UP!"
                
            return default_response
            
    print("Blacklist check completed")


    # Initilize response and number of attempts
    response = None
    attempts = 0

    while not response and attempts < 10:
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            output = model.generate(input_ids=input_ids, max_length=response_length, temperature=crazy_factor, do_sample=True, num_beams=8, repetition_penalty=2.8, length_penalty=3.5, no_repeat_ngram_size=4)[0]
        
        print("Generating a response")
        response = tokenizer.decode(output, skip_special_tokens=True)
        print(f"Response is {response}")
        
        if response is not None:
            response = format_response(prompt, response)
            print(f"Response found: {response}")

        print(f"Checking generated response #{attempts} against blacklist(if response exists)")
        # Regenerate the response if it contains an unwanted word
        for word in unwanted_words:

            if response:
                if word in response.lower():
                    print(f"Blacklisted word detected: {word}. Retrying.")
                    response = None
        attempts += 1

    if not response:
        print("Did not find a response")
        response = default_response


    return response


def format_response(prompt, response):
    if response:
        # Replace headers
        pattern = r"\w+\s\d{2}/\d{2}/\d{2}\s\((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\)\s\d{2}:\d{2}:\d{2}\s(?:AM|PM)\sNo\.\s\d+(?:\s>>\d+)?"
        response = re.sub(pattern, '', response)
        
        # Replace gif links
        pattern = (r"gif\]\((giphy\|\w+)\)")
        match = re.sub(pattern, '', response)
        
        # Replace any urls
        response = re.sub(r'http\S+', '', response)

        # Add space after any punctuation if there isn't a space already
        response = re.sub(r'([.!?])([^\s])', r'\1 \2', response)
        
        # Split text into sentences
        sentences = [s.strip() for s in re.split('(?<=[.!?]) +', response) if s.strip()]

        # Remove any repeating sentences from the response
        new_sentences = []
        for i, s in enumerate(sentences):
            unique = True
            for j in range(i):
                if similarity_score(s, sentences[j]) > 0.9:
                    unique = False
                    break

            if unique and not any(phrase in s.lower() for phrase in omit_phrases):
                if s[:-1] not in prompt:
                    new_sentences.append(s)

        # If last sentence is incomplete (i.e., doesn't end with a proper punctuation), remove it
        if len(new_sentences) > 0:
            last_sentence = new_sentences[-1]
            if last_sentence[-1] not in {'.', '!', '?'}:
                new_sentences = new_sentences[:-1]

        # If there's still any sentence left, replace the punctuation of the last sentence with "!!!"
        if len(new_sentences) > 0:
            last_sentence = new_sentences[-1]
            if last_sentence[-1] in {'.', '!', '?'}:
                new_sentences[-1] = last_sentence[:-1] + "!!!"

        # Join sentences
        response = " ".join(new_sentences)
        response = response.strip()

    return response



# Assigns a similarity score to use with the generated response to remove repeating words/sentences
def similarity_score(sentence1, sentence2):
    # If either of the sentences is empty, return 0
    if not sentence1.strip() or not sentence2.strip():
        return 0

    vectorizer = TfidfVectorizer().fit_transform([sentence1, sentence2])
    cosine_similarities = cosine_similarity(vectorizer)
    return cosine_similarities[0, 1]



# "Main" response function - called from handler file
def generate_response(prompt, user):

    # Format the prompt to improve coherence
    prompt = format_prompt(prompt, user)

    print(f"Prompt reformatted to: {prompt}")

    response = create_gpt_response(prompt)

    print(f"Current response is: {response}")
    return response
