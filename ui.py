import streamlit as st
import subprocess
import numpy as np
import cv2 as cv 
import os
st.title("Welcome to Expert Nutritionist")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Convert uploaded image to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv.imdecode(file_bytes, 1)

    st.image(image, caption="Uploaded Image")

    if st.button("Save Image"):
        cv.imwrite("captured_image.jpg", image)
        st.success("Image saved successfully!")

# Button to run the script
if st.button("Run Script"):
    try:
        # script_path = os.path.join(os.getcwd(), "Nutritionist-app", "goals.py")

        # Run the script
        process = subprocess.Popen(["python","goals.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output, error = process.communicate()  # Get stdout and stderr
       
        if output:
            st.header("Script Output:")
            st.text_area("Output", output, height=400)
        
        if error:
            st.subheader("Script Errors:")
            st.text_area("Errors", error, height=200, help="Check the errors if the script failed.")

    except Exception as e:
        st.error(f"Error executing script: {e}")

st.header("THANKYOU!")
