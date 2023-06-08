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
            output = model.generate(input_ids=input_ids, max_length=response_length, temperature=crazy_factor, do_sample=True, num_beams=5, repetition_penalty=2.5, length_penalty=0.8, no_repeat_ngram_size=2)[0]
        
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
        ### THE WONDERFUL SECTION WITH REGEX PATTERNS. GOD I HATE REGEX PATTERNS
        
        # Replace this weird header thing that I can only guess originates from quotes if it appears
        pattern = r"\w+\s\d{2}/\d{2}/\d{2}\s\((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\)\s\d{2}:\d{2}:\d{2}\s(?:AM|PM)\sNo\.\s\d+(?:\s>>\d+)?"
        response = re.sub(pattern, '', response)
        print(f"First regex pattern check complete (post date/time header). New response: {response}")
        
        # Replace this gif link shit. It doesn't work. I gave up.
        pattern = (r"gif\]\((giphy\|\w+)\)")
        match = re.sub(pattern, '', response)
        print(f"Second regex pattern check complete (gif links). New response: {response}")
        
        # Replace any urls
        response = re.sub(r'http\S+', '', response)
        print(f"Third regex pattern check complete (regular ol' hyperlinks). New response: {response}")
        
        # Split text into sentences
        sentences = [s.strip() for s in re.split('(?<=[.!?]) +', response) if s.strip()]
        print("Split response into sentences.")

        ### NO MORE REGEX - next part deals with any repeating sentences
        # Remove any repeating sentences from the response
        new_sentences = []
        for i, s in enumerate(sentences):
            unique = True
            for j in range(i):
                if similarity_score(s, sentences[j]) > 0.8:
                    unique = False
                    break

            if unique and not any(phrase in s.lower() for phrase in omit_phrases):
                if s[:-1] not in prompt:
                    # Append "!!!" to the last sentence - Emily style
                    if i == len(sentences) - 1:
                        s = s[:-1] + "!!!"
                    new_sentences.append(s)

        # Join sentences
        response = " ".join(new_sentences)
        response = response.strip()

    return response


# Assigns a similarity score to use with the generated response to remove repeating words/sentences
def similarity_score(sentence1, sentence2):
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
