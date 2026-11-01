import streamlit as st
import requests

st.title("Pokémon Classifier 🔴⚪")

# 1. The Portfolio Password
# Ask the user for a password before showing the upload tool
demo_password = st.text_input("Enter the Demo Password (found in my resume/README):", type="password")

# Check against a new secret we will add to Streamlit Cloud
if demo_password == st.secrets["DEMO_PASSWORD"]:
    
    # 2. The Session Limit
    # Initialize a counter in the browser's session memory
    if "request_count" not in st.session_state:
        st.session_state.request_count = 0

    st.write(f"Requests remaining: {10 - st.session_state.request_count}")

    # Lock the app if they spam the button more than 10 times in one visit
    if st.session_state.request_count >= 10:
        st.error("Demo limit reached for this session. Thank you for testing!")
    else:
        # Show the normal upload widget
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            if st.button("Predict"):
                # Increment the spam counter
                st.session_state.request_count += 1
                
                with st.spinner("Analyzing..."):
                    API_URL = "https://pokemon-classifier-app.wittypond-c9cb0b4a.canadacentral.azurecontainerapps.io/predict"
                    headers = {"X-API-Key": st.secrets["API_KEY_SECRET"]}
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    try:
                        response = requests.post(API_URL, headers=headers, files=files)
                        if response.status_code == 200:
                            prediction = response.json()
                            st.success(f"Predicted Class Index: {prediction['class_index']}")
                        else:
                            st.error(f"API Error {response.status_code}: {response.text}")
                    except Exception as e:
                        st.error(f"Failed to connect to the API: {e}")

elif demo_password:
    st.error("Incorrect password.")