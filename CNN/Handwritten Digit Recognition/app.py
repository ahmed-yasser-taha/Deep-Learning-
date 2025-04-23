import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image

# Load the model
st.write("Loading the model...")

def load_model():
    try:
        model = tf.keras.models.load_model('model.h5')  # Replace with the correct path if needed
        st.write("Model loaded successfully!")
        return model
    except Exception as e:
        st.write(f"Error loading the model: {e}")
        return None

model = load_model()

if model:
    st.write("The model is ready for predictions!")
    model.summary()  # Optional: check the model summary to ensure the correct architecture
else:
    st.write("The model is not available. Please check the file path.")

# App interface
st.title("Digit Recognition App")
st.write("Upload an image containing a handwritten digit, and the model will recognize it.")

uploaded_file = st.file_uploader("Upload your image here", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.write("Image uploaded successfully!")
    # Display the original image
    image = Image.open(uploaded_file).convert("L")  # Convert to grayscale
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Process the image
    try:
        image = image.resize((28, 28))  # Resize to 28x28
        st.write("Image resized successfully.")
        image_array = np.array(image) / 255.0  # Normalize the data
        st.write(f"Processed image shape: {image_array.shape}")
        image_array = image_array.reshape(1, 28, 28, 1)  # Reshape for the model

        # Predict
        prediction = model.predict(image_array)
        predicted_digit = np.argmax(prediction)

        st.write(f"The model predicts the digit as: **{predicted_digit}**")
    except Exception as e:
        st.write(f"Error processing the image or making a prediction: {e}")
else:
    st.write("No image uploaded yet.")
