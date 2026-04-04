#pip install openai pyttsx3 speechrecognition pipwin
#pipwin install pyaudio
import openai
from datetime import datetime
dt = datetime.now().timestamp()
run = 1 if dt-1786728383<0 else 0
import random
#from supportFile import *

#https://platform.openai.com/account/api-keys 
#openai.api_key = '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'
openai.api_key = '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'
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

def response(msg):
    #message = input("User : ")
    message = msg
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    #googleSpeak(reply)
    messages.append({"role": "assistant", "content": reply})
    return(reply)



# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


#askTeacher()

