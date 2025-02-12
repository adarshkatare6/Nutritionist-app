import os
import requests
from typing import Optional
from dotenv import load_dotenv
import cv2 as cv
import time
import pytesseract
import json
import subprocess
import sys

# detecting anf extracting text
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = cv.imread("captured_image.jpg")
extracted_text = pytesseract.image_to_string(img)


# Passing text and gettttting o/p

load_dotenv()
APPLICATION_TOKEN = os.getenv("Langflow_Token")

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "7a679269-fb01-4575-a6fa-c6d42f0c8595"

def get_suggestions(extracted):
    TWEAKS = {
    "TextInput-QMYA4": {
        "input_value": extracted}
    }
    return run_flow("",tweaks=TWEAKS,application_token=APPLICATION_TOKEN)

def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    api_url = f"https://api.langflow.astra.datastax.com/lf/7a679269-fb01-4575-a6fa-c6d42f0c8595/api/v1/run/90684aef-88c0-453d-a41e-86ae3d92fae4?stream=false"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

result=get_suggestions(extracted_text)
print(result["outputs"][0]["outputs"][0]["results"]["text"]["text"])