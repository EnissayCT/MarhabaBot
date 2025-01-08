from dotenv import load_dotenv
import os
from openai import OpenAI
import time
import random
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found in .env file")

pygame.mixer.init()

client = OpenAI(api_key=api_key)
recognizer = sr.Recognizer()
microphone = sr.Microphone()

with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

system_message = {
    "role": "system",
    "content": """be concise and friendly, You are Karim, a warm and knowledgeable Moroccan tour guide with 15 years of experience. 
    You speak with enthusiasm and often use Moroccan Arabic phrases (followed by translations) to add authenticity.
    You have deep knowledge of:
    - Moroccan history, culture, and traditions
    - The best local restaurants, riads, and hotels in different price ranges
    - Hidden gems and authentic experiences in each city
    - Local customs, etiquette, and safety tips
    - Seasonal events and festivals
    - Traditional cuisine and where to find the best examples
    
    Your responses should be friendly and conversational, as if walking with tourists through the streets of Morocco.
    Occasionally mention sensory details (smells of spices, sounds of the medina, etc.) to make the experience more immersive.
    When recommending places, always provide context about why they're special and any practical tips for visiting."""
}

welcome_messages = [
    "Marhaba! (Hello!) I'm Karim, your Moroccan guide. How can I help you explore our beautiful country?",
    "Ahlan wa sahlan! Welcome to Morocco! I'm Karim, and I'm here to help you discover our magnificent kingdom.",
    "As-salaam-alaikum! I'm Karim, your guide to Morocco's treasures. What would you like to know about our wonderful country?"
]

ambiance_messages = [
    "🎵 [In the background, you can hear the melodic call to prayer echoing through the ancient medina]",
    "☕ [The gentle clink of mint tea glasses and the buzz of the souk fill the air]",
    "🎨 [Around us, the vibrant colors of spice mountains and handwoven carpets create a feast for the eyes]"
]

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
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        pygame.mixer.music.unload()
        os.remove(temp_filename)

def get_voice_input():
    with microphone as source:
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

def add_ambiance():
    if random.random() < 0.3:
        return random.choice(ambiance_messages)
    return ""

def chat_terminal():
    print("="*50)
    print("🕌 Welcome to Your Moroccan Adventure! 🐪")
    print("="*50)
    print("\nSpeak or type 'text mode' to switch to text input")
    print("Say 'exit' or type 'exit' to end the conversation\n")
    welcome = random.choice(welcome_messages)
    print(f"Guide: {welcome}")
    speak(welcome)
    messages = [system_message]
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
            farewell = "Ma'a salama! (Goodbye!) I hope you enjoyed learning about Morocco. Have a wonderful journey!"
            print(f"\nGuide: {farewell}")
            speak(farewell)
            break
        try:
            messages.append({"role": "user", "content": user_input})
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response = chat_completion.choices[0].message.content
            ambiance = add_ambiance()
            print(f"\nGuide: {response}")
            if ambiance:
                print(f"\n{ambiance}")
            speak(response)
            messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"Sorry, I'm having trouble connecting to the network. Could you please repeat that? Error: {e}"
            print(f"\nGuide: {error_msg}")
            speak(error_msg)

if __name__ == "__main__":
    chat_terminal()
