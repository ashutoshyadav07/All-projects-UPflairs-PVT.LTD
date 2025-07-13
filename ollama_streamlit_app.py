import streamlit as st
import json
import requests

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Streamlit UI
st.title("💬 Chat with Ollama (LLaMA 3)")

user_input = st.text_input("Enter your prompt:")

if st.button("Generate"):
    if user_input:
        payload = {
            "model": "llama3.2",
            "prompt": user_input,
            "stream": False  # Set to True only if you're streaming and handling it line by line
        }

        with st.spinner("Generating response..."):
            try:
                response = requests.post(OLLAMA_URL, json=payload)

                if response.status_code == 200:
                    # Safely handle multiple JSON chunks
                    try:
                        data = response.json()  # this works only if stream=False and one full JSON is returned
                        result = data.get("response", "No response received.")
                    except json.JSONDecodeError:
                        # Fall back: handle line-by-line JSON if needed
                        lines = response.text.strip().splitlines()
                        responses = [json.loads(line) for line in lines if line.strip()]
                        result = "\n".join(r.get("response", "") for r in responses)
                    
                    st.success(result)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")