#Import required Libraries
import speech_recognition as sr
import google.generativeai as genai
import webbrowser
import pyttsx3
import pyautogui
import datetime
import requests
import json
import openai
import pyperclip

#Assistant Class to contain all the Functions
class Assistant:
    #Initializing Owner Name, Assistant Name, API Keys
    def __init__(self):
        openai.api_key = '--YOUR OPENAI API KEY--'
        genai.configure(api_key='--YOUR GEMINI API KEY--')
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat()
        self.owner_name = "--YOUR NAME--"
        self.assistant_name = "AIDesk"
        self.weather_api_key = "--YOUR WEATHER API KEY--"
        self.speech_recognizer = sr.Recognizer()
        self.listener = sr.Microphone()
        self.engine = self.initialize_engine()

    #Initializing Speaking Engine using Pyttsx3
    def initialize_engine(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        voice_index = 0  # Set the desired voice index
        engine.setProperty('voice', voices[voice_index].id)
        engine.setProperty('rate', 150)
        return engine

    #Speak Function
    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.print_response(f"Oh no, an error occurred: {str(e)}")

    #Function to Copy Results to clipboard
    def copy_to_clipboard(self, text):
        try:
            pyperclip.copy(text)
            return True
        except:
            error = "Error occurred while copying to clipboard"
            return False, error

    #Listen Function
    def listen(self):
        with self.listener as source:
            self.print_response("Speak something...")
            audio = self.speech_recognizer.listen(source)
            self.print_response("Recognizing audio...")
        try:
            text = self.speech_recognizer.recognize_google(audio, show_all=False)
            if text == 'exit':
                return "Bye Bye Vedant!"
            self.print_query(f"{text}")
            return text
        except sr.UnknownValueError:
            self.print_response("Sorry, I could not understand audio input.")
            return "Sorry, I could not understand audio input."
        except sr.RequestError as e:
            self.print_response("Error occurred during speech recognition")
            return "Error occurred!"

    #Function to Print Response in textbox
    def print_response(self, text):
        print(f">>> {self.assistant_name}: {text}")

    #Function to Print Query in textbox
    def print_query(self, query):
        print(f">>> {self.owner_name}: {query}")

    #Function to decide which action to be taken
    def decide_action(self, input_string):
        input_string = str(input_string).lower()
        intro = ["who are you", "tell me about yourself", "what can you do", "hello", "hello hello"]
        if "search" in input_string:
            action, query = input_string.split(" ", 1)
            if "on youtube" in query:
                topic = query.replace("on youtube", "").strip()
                if self.youtube_search(topic):
                    response = f"Searching {topic} on YouTube!"
                    self.print_response(response)
                    self.speak(response)
            elif "on google" in query:
                topic = query.replace("on google", "").strip()
                if self.google_search(topic):
                    response = f"Searching {topic} on Google!"
                    self.print_response(response)
                    self.speak(response)
            elif "on youtube music" in query or "on yt music" in query:
                topic = query.replace("on youtube music", "").replace("on yt music", "").strip()
                if self.yt_music_search(topic):
                    response = f"Searching {topic} on YouTube Music!"
                    self.print_response(response)
                    self.speak(response)
            else:
                if self.google_search(query):
                    response = f"Searching {query} on Google!"
                    self.print_response(response)
                    self.speak(response)

        elif "play music" in input_string:
            if self.open_website("youtube music"):
                response = "Opening YouTube Music!"
                self.print_response(response)
                self.speak(response)

        elif "date" in input_string:
            if self.get_date():
                response = self.get_date()
                self.print_response(response)
                self.speak(response)

        elif "open" in input_string:
            action, website = input_string.split(" ", 1)
            if self.open_website(website):
                response = f"Opening {website}!"
                self.print_response(response)
                self.speak(response)
            else:
                response = f"Sorry, I don't know about {website}!"
                self.print_response(response)
                self.speak(response)

        elif "screenshot" in input_string:
            if self.take_screenshot():
                response = "Screenshot taken successfully!"
                self.print_response(response)
                self.speak(response)

        elif "time" in input_string:
            if self.tell_time():
                response = self.tell_time()
                self.print_response(response)
                self.speak(response)

        elif any(keyword in input_string for keyword in ["temperature", "weather"]):
            city = self.extract_city(input_string)
            if not city:
                city = "Ajra"
            if self.tell_temp(city):
                response = self.tell_temp(city)
                self.print_response(response)
                self.speak(response)

        elif input_string in intro:
            response = f"Hello, I'm {self.assistant_name}, your Desktop Assistant. " \
                       f"I can help with tasks like taking screenshots, opening websites, " \
                       f"performing Google and YouTube searches, and providing date, time, and temperature."
            self.print_response(response)
            self.speak(response)

        else:
            try:
                response = self.generate_gemini_response(input_string)
            except:
                response = self.generate_ai_response(input_string)
            self.print_response(response)
            self.speak(response)

    #Function to start Listening
    def start_listening(self):
        self.speak(f"Hello {self.owner_name}!")
        user_input = self.listen()
        self.decide_action(user_input)

    #Function to Generate AI based responce from Chat GPT
    def generate_ai_response(self, command):
        try:
            # Send a request to the GPT-3.5 Turbo model
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=command,
                max_tokens=50,
                temperature=0.7,
                n=1,
                stop=None,
            )
            # Retrieve the generated response
            output = response.choices[0].text.strip()
            self.copy_to_clipboard(output)
            return output
        except:
            self.print_response("Error occurred while generating response")
            return False

    #Function to get AI Response from Gemini AI Google
    def generate_gemini_response(self, command):
        try:
            response = self.chat.send_message(command)
            self.copy_to_clipboard(response.text)
            return response.text.replace('*','')
        except:
            self.print_response("Error occurred while generating response")
            return False

    #Function to get today's Date
    def get_date(self):
        try:
            today = datetime.date.today()
            month_name = today.strftime("%B")
            date_string = f"Today is {today.day} {month_name} {today.year}"
            return date_string
        except:
            self.print_response("Error occurred while getting date")
            return False

    #Function to Search on Google a Specific Query
    def google_search(self, query):
        try:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return True
        except:
            return False
    
    #Function to Search on Youtube a Specific Query
    def youtube_search(self,query):
        try:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return True
        except:
            self.print_response("Error Occoured while searching !")
            return False

    #Function to take a Screenshot
    def take_screenshot(self):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot = pyautogui.screenshot()
            file_name = f"screenshot_{timestamp}.png"
            filepath = f"C:/Users/Admin/Pictures/Screenshots/{file_name}"
            screenshot.save(filepath)
            return True
        except:
            self.print_response("Error taking a screenshot!")
            return False

    #Function to get current time
    def tell_time(self):
        try:
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute
            meridiem = "morning" if hour < 12 else "evening"
            hour = hour if hour <= 12 else hour - 12
            time_string = f"It's {hour} {minute:02d} in {meridiem}"
            return time_string
        except:
            self.print_response("Error getting time!")
            return False

    #Function to Search on YT music a Specific Query
    def yt_music_search(self, query):
        try:
            webbrowser.open(f"https://music.youtube.com/search?q={query}")
            return True
        except:
            self.print_response("Error occurred while searching!")
            return False

    #Function to open Specific website
    def open_website(self, website_name):
        websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "google maps": "https://www.google.com/maps",
            "youtube music": "https://music.youtube.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "reddit": "https://www.reddit.com",
            "linkedin": "https://www.linkedin.com",
            "amazon": "https://www.amazon.com",
            "flipkart": "https://www.flipkart.com",
            "netflix": "https://www.netflix.com",
            "github": "https://www.github.com",
            "stackoverflow": "https://www.stackoverflow.com",
            "spotify": "https://www.spotify.com",
            "pinterest": "https://www.pinterest.com",
            "wikipedia": "https://www.wikipedia.org",
            "wordpress": "https://www.wordpress.com",
            "bbc": "https://www.bbc.co.uk",
            "yahoo": "https://www.yahoo.com",
            "microsoft": "https://www.microsoft.com",
            "openai": "https://www.openai.com"
        }

        if website_name in websites:
            website_url = websites[website_name]
            webbrowser.open(website_url)
            return True
        else:
            return False

    #Function to get tempreature of a city
    def tell_temp(self, city):
        try:
            url = f'https://api.weatherapi.com/v1/current.json?key={self.weather_api_key}={city}'
            r = requests.get(url)
            r.raise_for_status()  # Raise an exception if there is an HTTP error
            weatherdic = json.loads(r.text)
            temp = weatherdic['current']['temp_c']
            response = f"Temperature of {city} is {temp} Degree Celsius!"
            return response
        except:
            self.print_response("Error occurred while getting temperature!")
            return False

    #Function to get city name from a string
    def extract_city(self, input_string):
        keywords = ["temperature", "weather"]
        city = ""
        for keyword in keywords:
            if keyword in input_string:
                city = input_string.replace(keyword, "").strip()
                break
        return city

    def run(self):
        self.start_listening()
