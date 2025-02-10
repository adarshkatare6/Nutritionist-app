import requests
import os
from dotenv import load_dotenv
import cv2 as cv
import time
import pytesseract
from termcolor import colored
import uuid
import json

#capture image
# cap = cv.VideoCapture(0)
# while True:
#     ret, frame = cap.read()  # Read frame from the camera
#     if not ret:
#         print("Error: Could not read frame.")
#         break
#     cv.imshow("image is",frame)
#     key = cv.waitKey(1) & 0xFF
#     if key == ord('c'):
#         cv.imwrite("captured_image.jpg", frame)
#         print("Image saved as captured_image.jpg")
#     elif key == ord('q'):
#         break
# cap.release()
# cv.destroyAllWindows()


# detecting anf extracting text
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = cv.imread("captured_image.jpg")
extracted_text = pytesseract.image_to_string(img)




# passsing text and gettting output
load_dotenv()
APPLICATION_TOKEN = os.getenv("Langflow_Token")

API_URL = "https://api.langflow.astra.datastax.com/lf/7a679269-fb01-4575-a6fa-c6d42f0c8595/api/v1/run/30cbba02-3cad-4c23-99e8-7745c74ed896?stream=false"
API_URL += f"&nocache={int(time.time())}" 
# extracted_text=os.getenv("extract")
if not APPLICATION_TOKEN :
    print("❌ ERROR: LangFlow Token is missing! Check your .env file.")
    exit()
if not extracted_text:
    print("❌ ERROR: Extracted text is missing! Check your .env file.")
    exit()

headers = {
    "Authorization": f"Bearer {APPLICATION_TOKEN}", 
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Expires": "0"
}
 
print(colored('Extracted Text::', 'green', attrs=['bold']))
print(extracted_text)

payload = {
    "input_value": f"{extracted_text} | {uuid.uuid4()}",
    "output_type": "chat",
    "input_type": "chat",
    "stream": False, 
    "tweaks": {
        "TextInput-bk4UF": {"value": extracted_text},
        "Agent-fko44": {},
        "TextOutput-ycyr8": {}
    }
}

response = requests.post(API_URL, json=payload, headers=headers)
result =  response.json()
# print("Payload being sent:", json.dumps(payload, indent=2))

try:
    text_output = result["outputs"][0]["outputs"][0]["results"]["text"]["text"]
    print(colored('Final Output::', 'red', attrs=['bold']))
    print(text_output)
except KeyError:
    print("Error: Could not extract text from response.")
    print(result)
