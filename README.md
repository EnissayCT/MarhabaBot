# MarhabaBot 

This project integrates **Azure Computer Vision** and **OpenAI GPT-3.5** to create a smart, interactive Moroccan guide for tourists.  

## Features  
1. **Image Analysis** (`AzureComputerVision.py`)  
   - Uses Azure Computer Vision API to analyze images.  
   - Extracts scene descriptions, tags, and colors.  

2. **Voice-Based Chatbot** (`VoiceChatOpenAI.py`)  
   - Implements a Moroccan tour guide chatbot named Karima.  
   - Provides travel recommendations, cultural insights, and personalized suggestions.  
   - Supports both voice input and text responses using GPT-3.5 and Google Text-to-Speech (gTTS).  

3. **Integrated Solution** (`MarhabaBot.py`)  
   - Combines image analysis with conversational intelligence.  
   - Predicts the location based on image content and chat context.  
   - Provides detailed descriptions of the predicted location.
   - Helps the tourist wander to the best places in Morocco.
   - Gives suggesstions of restaurants, monuments and more...
   - Provides accurate facts of Morocco's rich history...

## Prerequisites  
- **Python 3.8+**  
- Required libraries:  
  - `requests`  
  - `openai`  
  - `gtts`  
  - `pygame`  
  - `speechrecognition`  
  - `tkinter`  
  - `dotenv`

Install libraries using pip:  
```bash
pip install requests openai gtts pygame SpeechRecognition python-dotenv
```
# Setup  

## Clone the repository:  
```bash
git clone https://github.com/EnissayCT/MarhabaBot.git
cd MarhabaBot
```
Create a .env file in the root directory and add your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key
AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key
AZURE_ENDPOINT=your_azure_endpoint
```

Run each script based on the functionality you want:
## Image Analysis:
python AzureComputerVision.py

## Chatbot:
python VoiceChatOpenAI.py

## Combined Solution:
python MarhabaBot.py

### How It Works
#### AzureComputerVision.py:
  Prompts you to upload an image.
  Extracts visual insights using Azure’s Computer Vision API.
#### VoiceChatOpenAI.py:
  A voice-enabled chatbot that responds to travel-related questions.
  Features a Moroccan cultural theme with voice input/output.
#### MarhabaBot.py:
  Combines image analysis with conversational capabilities.
  Analyzes the uploaded image, predicts the location, and provides relevant details based on the conversation context.
  Guides and accompanies the tourist in his travels inside the kingdom.
## Notes
You must fill in your API keys in the .env file for both Azure and OpenAI.
Ensure all required libraries are installed before running the scripts.
## Future Enhancements
Add multi-language support for broader accessibility.
Improve location prediction using advanced AI models.
Enhance voice response speed and naturalness.
