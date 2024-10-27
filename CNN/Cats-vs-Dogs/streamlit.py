import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image

# Load pre-trained model (ensure the path is correct)
@st.cache_resource  # Cache the model to avoid reloading on every interaction
def load_model():
    model = tf.keras.models.load_model("model.h5")  # or use SavedModel directory
    return model

model = load_model()

# Function to preprocess and predict
def predict_image(image, model):
    image = image.resize((224, 224))  # Ensure the input size matches your model's input
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image (if your model requires it)

    # Predict using the loaded model
    predictions = model.predict(img_array)
    
    # Assuming it's a binary classification (cat = 0, dog = 1)
    class_names = ["cat", "dog"]
    predicted_class = class_names[np.argmax(predictions)]  # Get the highest probability class
    return predicted_class

# Streamlit app
st.title("Cat vs Dog Classifier")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Classifying...")
    
    prediction = predict_image(image, model)
    st.write(f"The image is a **{prediction}**.")