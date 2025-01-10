import os
import requests
import tkinter as tk
from tkinter import filedialog

subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")
endpoint = "https://marhabaanalyser.cognitiveservices.azure.com/"
analyze_url = f"{endpoint}vision/v3.1/analyze"

def analyze_image(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    return response.json()

def main():
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if not image_path:
        print("No file selected.")
        return
    try:
        analysis = analyze_image(image_path)
        if "description" in analysis and "captions" in analysis["description"] and analysis["description"]["captions"]:
            description = analysis["description"]["captions"][0]["text"]
            print(f"Description: {description}")
        else:
            print("No description available for this image.")
        print("\nTags:")
        for tag in analysis.get("description", {}).get("tags", []):
            print(f"- {tag}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
