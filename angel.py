from cgitb import text
from email.mime import audio
from itertools import takewhile
from logging.config import listen
from unittest import result
import wikipedia #pip install wikipedia
import requests
from pprint import pprint
import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import random
import wolframalpha
from playsound import playsound





engine = pyttsx3.init('sapi5')
wolframalpha_app_id = "###id####"
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time=datetime.datetime.now().strftime("%I:%M:%S")
    speak(" the current time is")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak("the current date is")
    speak(date)
    speak(month)
    speak(year)

def wishme():
    speak("Welcome back sir")

    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning! , i am angel , how can i help you,sir?")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!, i am angel , how can i help you,sir?")

    else:
        speak("Good Evening! i am angel , how can i help you,sir?")
