from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import filedialog
import requests
from openai import OpenAI
import random
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import warnings

warnings.filterwarnings("ignore")

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")

if not api_key or not subscription_key or not endpoint:
    raise ValueError("Required API keys or endpoint not found in .env file")

analyze_url = f"{endpoint}vision/v3.1/analyze"
pygame.mixer.init()

client = OpenAI(api_key=api_key)

def analyze_image(messages):
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if not image_path:
        return "No image selected."

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()

    if "description" in analysis and "captions" in analysis["description"] and analysis["description"]["captions"]:
        description = analysis["description"]["captions"][0]["text"]
        
        prediction_prompt = f"The image shows: '{description}'. Based on this and the current conversation context: {messages}, where might this photo have been taken? Describe the place."
        messages.append({"role": "user", "content": prediction_prompt})
        prediction_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        prediction = prediction_response.choices[0].message.content
        return f"Based on the analysis and our convo, you might be at: {prediction.strip()}."
    else:
        return "No description available for this image."

def speak(text):
    clean_text = text.replace('*', '').replace('#', '').replace('', '')
    tts = gTTS(text=clean_text, lang='en', tld='co.uk')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        temp_filename = fp.name
    tts.save(temp_filename)
    try:
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(60)  
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        pygame.mixer.music.unload()
        os.remove(temp_filename)

def get_voice_input():
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"Heard: {text}")
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return None

def chat_terminal():
    print("="*50)
    print("🕌 Welcome to Your Moroccan Adventure! 🐪")
    print("="*50)
    print("\nSpeak or type 'text mode' to switch to text input")
    print("\nSpeak or type 'open image' to enter an input as an image.")
    print("Say 'exit' or type 'exit' to end the conversation\n")

    welcome_messages = [
        "Salam! I'm Karima, your Moroccan guide. How can I assist you?",
        "Ahlan! Welcome to Morocco! What do you need help with?",
        "Salam! I'm Karima, your guide. How can I help today?"
    ]
    welcome = random.choice(welcome_messages)
    print(f"Guide: {welcome}")
    speak(welcome)

    messages = [{"role": "system", "content": "You are Karima, a concise and to the point Moroccan tour guide."}]
    text_mode = False

    while True:
        if text_mode:
            user_input = input("\nYou: ")
        else:
            user_input = get_voice_input()

        if user_input is None:
            continue
        if user_input.lower() == "text mode":
            text_mode = not text_mode
            continue
        if user_input.lower() == "exit":
            farewell = "Goodbye! Have a great day exploring Morocco!"
            print(f"\nGuide: {farewell}")
            speak(farewell)
            break
        if user_input.lower() == "open image":
            image_analysis_result = analyze_image(messages)
            print(f"\nGuide: {image_analysis_result}")
            speak(image_analysis_result)
            continue

        try:
            messages.append({"role": "user", "content": user_input})
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response = chat_completion.choices[0].message.content
            print(f"\nGuide: {response}")
            speak(response)
            messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"Sorry, I'm having trouble connecting to the network. Could you please repeat that? Error: {e}"
            print(f"\nGuide: {error_msg}")
            speak(error_msg)

if __name__ == "__main__":
    chat_terminal()
