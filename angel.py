# Voice Assistant Code

import wikipedia 
import requests
import pyttsx3
import datetime
import speech_recognition as sr  # pip install SpeechRecognition
import os
import smtplib
import psutil  # pip install psutil
import pyjokes  # pip install pyjokes
import pyautogui  # pip install pyautogui
import webbrowser as wb
import random
import wolframalpha  # pip install wolframalpha
import cv2  # pip install opencv-python
import numpy as np
from playsound import playsound  # pip install playsound
from ultralytics import YOLO  # pip install ultralytics
import supervision as sv  # pip install supervision
import torch
import subprocess  # For opening Spotify

# Directory for screenshots
screenshot_dir = "E:\\test1"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Directory to save diary notes
diary_dir = "E:\\diary_notes"
if not os.path.exists(diary_dir):
    os.makedirs(diary_dir)

# Voice assistant initialization
today = datetime.date.today()
r = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
wolframalpha_app_id = "6YKJH2-45J43UPXHV"  # Replace with your Wolfram Alpha App ID

# YOLO Zone polygon for object detection
ZONE_POLYGON = np.array([
    [0, 0],
    [0.5, 0],
    [0.5, 1],
    [0, 1]
])

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Greeting function
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Angel, how can I help you, sir?")

# Listening for voice command
def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 500
        r.dynamic_energy_threshold = False
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

# Email function
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent.")
    except Exception as e:
        speak("Unable to send email.")

# Screenshot function
def screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
    img = pyautogui.screenshot()
    img.save(screenshot_path)
    speak("Screenshot taken.")

# Open latest screenshot
def show_screenshot():
    screenshots = sorted(os.listdir(screenshot_dir), reverse=True)
    if screenshots:
        latest_screenshot = os.path.join(screenshot_dir, screenshots[0])
        os.startfile(screenshot_dir)  # Opens the folder
        os.startfile(latest_screenshot)  # Opens the latest screenshot
        speak("Here is the latest screenshot.")
    else:
        speak("No screenshots available to show.")

# CPU usage function
def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at ' + usage)
    battery = psutil.sensors_battery()
    speak('Battery is at')
    speak(battery.percent)

# Tell a joke
def joke():
    speak(pyjokes.get_joke())

# Close the current tab
def close_tab():
    pyautogui.hotkey('ctrl', 'w')
    speak("Closed the current tab.")

# Close a specified application
def close_application(app_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == app_name:
            proc.terminate()  # Use terminate instead of os.kill
            speak(f"{app_name} has been closed.")
            return
    speak(f"No running instance of {app_name} found.")

# Object Detection with YOLOv8 using Webcam
def start_object_detection():
    speak("Starting object detection...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Unable to access the webcam.")
        return

    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    model = YOLO("yolov8l.pt")  # Load YOLOv8 model
    
    box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)
    zone_polygon = (ZONE_POLYGON * np.array([1280, 720])).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=(1280, 720))
    zone_annotator = sv.PolygonZoneAnnotator(text_thickness=2, text_scale=2)

    speak("Starting object detection. Press 'Esc' to exit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Failed to capture video frame.")
            break

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)

        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _ in detections
        ]
        
        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)

        cv2.imshow("YOLOv8 Object Detection", frame)

        if cv2.waitKey(30) == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()
    speak("Object detection has ended.")

# Diary Note Taking
def take_note():
    speak("What would you like to write in your diary?")
    content = TakeCommand()
    if content.lower() != "none":
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        note_path = os.path.join(diary_dir, f"note_{timestamp}.txt")
        with open(note_path, "w") as file:
            file.write(content)
        speak("Your note has been saved.")
    else:
        speak("No content to save.")

def open_latest_note():
    notes = sorted(os.listdir(diary_dir), reverse=True)
    if notes:
        latest_note = os.path.join(diary_dir, notes[0])
        os.startfile(latest_note)
        speak("Here is your latest note.")
    else:
        speak("No notes available to show.")

# Play music on Spotify
def play_music(song_name):
    speak(f"Playing {song_name} on Spotify.")
    subprocess.run(['spotify', song_name])

# Main program loop
if __name__ == "__main__":
    wishme()
    while True:
        query = TakeCommand().lower()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(result)
            speak(result)
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = TakeCommand()
                speak('Who is the receiver?')
                receiver = input("Enter Receiver's Email: ")
                sendEmail(receiver, content)
            except Exception as e:
                speak("Unable to send Email.")
        elif 'open chrome' in query:
            speak('What should I search?')
            chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search + '.com')
        elif 'cpu' in query:
            cpu()
        elif 'joke' in query:
            joke()
        elif 'stop' in query:
            speak("Going offline, sir.")
            quit()
        elif 'screenshot' in query:
            screenshot()
        elif 'show screenshot' in query:
            show_screenshot()
        elif 'play music' in query:
            speak("What song would you like to play?")
            song_name = TakeCommand()
            play_music(song_name)
        elif 'open youtube' in query:
            speak('What should I search?')
            search_Term = TakeCommand().lower()
            wb.open(f'https://www.youtube.com/results?search_query={search_Term}')
        elif 'open google' in query:
            speak("What should I search?")
            search_Term = TakeCommand().lower()
            wb.open(f'https://www.google.com/search?q={search_Term}')
        elif 'where is' in query:
                query = query.replace("where is", "")
                location = query
                speak("User asked to locate " + location)
                wb.open_new_tab("https://www.google.com/maps/place/" + location)
        elif 'calculate' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            speak(f'The answer is {answer}')
        elif 'who is' in query or 'what is' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            res = client.query(query)
            try:
                answer = next(res.results).text
                speak(answer)
            except StopIteration:
                speak("No results found.")
        elif 'close tab' in query:
            close_tab()
        elif 'close chrome' in query:
            close_application('chrome.exe')
        elif 'start object detection' in query:
            start_object_detection()
        elif 'take note' in query or 'write diary' in query:
            take_note()
        elif 'open notepad' in query or 'open latest note' in query:
            open_latest_note()
        else:
            speak("I didn't understand. Can you repeat that, please?")
