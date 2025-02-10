from fastapi import FastAPI, File, UploadFile
import io
import os
import cv2 as cv
import pytesseract
from PIL import Image
import shutil

app = FastAPI()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Read frame from the camera
    if not ret:
        print("Error: Could not read frame.")
        break
    cv.imshow("image is",frame)
    key = cv.waitKey(1) & 0xFF
    if key == ord('c'):
        cv.imwrite("capturedwe_image.jpg", frame)
        print("Image saved as captured_image.jpg")
    elif key == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

img = cv.imread("nutrition-label1.jpg")
extracted_text = pytesseract.image_to_string(img)
print("Extracted Text:", extracted_text)

with open(".env", "a") as env_file:
    env_file.write(f"extract=str{extracted_text}\n") 
    print("done")



# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# @app.post("/upload/")
# async def upload_image(file: UploadFile = File(...)):
#     try:
#         # Read the uploaded image
#         image_bytes = await file.read()
#         image = Image.open(io.BytesIO(image_bytes))

#         img_cv = cv.cvtColor(cv.imread(io.BytesIO(image_bytes)), cv.COLOR_BGR2RGB)

#         extracted_text = pytesseract.image_to_string(img_cv)
#         print("Extracted Text:", extracted_text)

#         with open(".env", "a") as env_file:
#             env_file.write(f"extract={extracted_text}\n")

#         return {"status": "success", "extracted_text": extracted_text}

#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)