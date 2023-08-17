import openai
import os
import pandas as pd
import numpy as np

def get_completion(input_prompt, model="gpt-3.5-turbo", temperature = 0.8, system_prompt_fpath = './model/prompt-inventory/system-prompt.txt',):
    
    with open(system_prompt_fpath, 'r') as file:
        system_prompt = file.read()
    
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": input_prompt},
               ]
    
    response = openai.ChatCompletion.create(model=model,
                                            messages=messages,
                                            temperature=temperature
                                           )
    return response.choices[0].message["content"]

def get_coverletter(cv, jd, word_count, prompt_head_fpath = './model/prompt-inventory/prompt-head.txt'):
    
    # Load prompt head
    with open(prompt_head_fpath, 'r') as file:
        input_prompt_head = file.read()

    # Construct full input prompt
    input_prompt = f"""{input_prompt_head} 

    You are REQUIRED to limit your output to only within {int(word_count * 0.80)} words.

    My first input is:

    >>>{cv}<<< 

    ###{jd}###"""
    
    return get_completion(input_prompt)
    