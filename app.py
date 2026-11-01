import streamlit as st
import requests

st.title("Pokémon Classifier 🔴⚪")
st.write("Upload an image of a Generation 1 Pokémon to see what the model predicts!")

# 1. Create the file upload widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image on the screen
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Predict"):
        with st.spinner("Analyzing..."):
            # REPLACE THIS with your actual Azure Container App URL
            API_URL = "https://pokemon-classifier-app.[your-domain].azurecontainerapps.io/predict"
            
            # Fetch the secret API key from Streamlit's secure storage
            headers = {"X-API-Key": st.secrets["API_KEY_SECRET"]}
            
            # Extract the raw image bytes from the Streamlit uploader
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            # Make the POST request to your Azure API
            try:
                response = requests.post(API_URL, headers=headers, files=files)
                
                if response.status_code == 200:
                    prediction = response.json()
                    st.success(f"Predicted Class Index: {prediction['class_index']}")
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to the API: {e}")