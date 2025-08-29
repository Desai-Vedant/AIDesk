#Import required Libraries
import speech_recognition as sr
from google import generativeai as genai
import webbrowser
import pyttsx3
import pyautogui
import datetime
import requests
import json
import pyperclip
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#Assistant Class to contain all the Functions
class Assistant:
    #Initializing Owner Name, Assistant Name, API Keys
    def __init__(self):
        # Initialize API keys from environment variables
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')

        # Initialize Gemini AI model
        if self.gemini_api_key:
            from google import genai
            from google.genai import types
            
            # Initialize the Gemini client
            self.client = genai.Client(api_key=self.gemini_api_key)

            # Configure generation config
            self.generation_config = types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                candidate_count=1,
                max_output_tokens=2048,
                stop_sequences=[],
                # Safety settings with new format
                safety_settings=[
                    types.SafetySetting(
                        category='HARM_CATEGORY_HARASSMENT',
                        threshold='BLOCK_ONLY_HIGH'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_HATE_SPEECH',
                        threshold='BLOCK_ONLY_HIGH'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
                        threshold='BLOCK_ONLY_HIGH'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_DANGEROUS_CONTENT',
                        threshold='BLOCK_ONLY_HIGH'
                    )
                ]
            )

        # Set user configuration
        self.owner_name = os.getenv('OWNER_NAME', "--YOUR NAME--")
        self.assistant_name = os.getenv('ASSISTANT_NAME', "AIDesk")
        
        # Initialize speech components
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
            # Use streaming for longer queries that might need detailed responses
            if len(input_string.split()) > 10:
                response = self.generate_streaming_response(input_string)
            else:
                response = self.generate_gemini_response(input_string)
            self.print_response(response)
            self.speak(response)

    #Function to start Listening
    def start_listening(self):
        self.speak(f"Hello {self.owner_name}!")
        user_input = self.listen()
        self.decide_action(user_input)

    #Functions to get AI Response from Gemini AI Google
    def generate_streaming_response(self, command):
        """Generate AI response using Gemini API with streaming"""
        if not self.gemini_api_key:
            self.print_response("No AI API keys configured!")
            return "I apologize, but I don't have access to AI services at the moment. Please check your API configuration."
        
        try:
            # Use streaming for longer responses
            response_stream = self.client.models.generate_content_stream(
                model='gemma-3-27b-it',
                contents=[{
                    "role": "user",
                    "parts": [{"text": command}]
                }],
                config=self.generation_config
            )

            # Collect the streamed response
            full_response = []
            for chunk in response_stream:
                if chunk.text:
                    full_response.append(chunk.text)
                    # Print each chunk as it arrives
                    print(chunk.text, end='', flush=True)

            complete_response = ''.join(full_response)
            if complete_response:
                self.copy_to_clipboard(complete_response)
                return complete_response.replace('*', '')

            return "Sorry, I couldn't generate a response at this time."

        except Exception as e:
            error_msg = str(e)
            if "safety" in error_msg.lower():
                return "I apologize, but I cannot provide a response to that query due to safety considerations."
            elif "rate" in error_msg.lower():
                return "I'm receiving too many requests right now. Please try again in a moment."
            else:
                self.print_response(f"Error with Gemini streaming: {error_msg}")
                return "I encountered an error while processing your request. Please try again later."
    def generate_gemini_response(self, command):
        """Generate AI response using Gemini API"""
        if not self.gemini_api_key:
            self.print_response("No AI API keys configured!")
            return "I apologize, but I don't have access to AI services at the moment. Please check your API configuration."
        
        try:
            # Create response using the configured client
            response = self.client.models.generate_content(
                model='gemma-3-27b-it',
                contents=[{
                    "role": "user",
                    "parts": [{"text": command}]
                }],
                config=self.generation_config
            )

            if response.candidates:
                answer = response.text
                # Copy response to clipboard
                if answer:
                    self.copy_to_clipboard(answer)
                    return answer.replace('*', '')

            return "Sorry, I couldn't generate a response at this time."

        except Exception as e:
            error_msg = str(e)
            # Check for specific error types
            if "safety" in error_msg.lower():
                return "I apologize, but I cannot provide a response to that query due to safety considerations."
            elif "rate" in error_msg.lower():
                return "I'm receiving too many requests right now. Please try again in a moment."
            else:
                self.print_response(f"Error with Gemini: {error_msg}")
                return "I encountered an error while processing your request. Please try again later."

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
            screenshot_path = os.getenv('SCREENSHOT_PATH', "C:/Users/Admin/Pictures/Screenshots/")
            filepath = os.path.join(screenshot_path, file_name)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            screenshot.save(filepath)
            return True
        except Exception as e:
            self.print_response(f"Error taking a screenshot: {str(e)}")
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
            url = f'https://api.weatherapi.com/v1/current.json?key={self.weather_api_key}&q={city}'
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
