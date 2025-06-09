import streamlit as st
from openai import OpenAI
import os # We need this to check if the key file exists

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="my-chatbot-ai",
    page_icon="🦇",
    layout="centered"
)

st.title("🦇Bat-Bot AI")
st.caption("Designed by Mr.Varla Buggaiah")

# --- AUTHENTICATION - NEW DIRECT FILE READ METHOD ---

# --- AUTHENTICATION - DUAL MODE (SECURE FOR DEPLOYMENT) ---

api_key = None

# First, try to get the key from Streamlit's secrets (for cloud deployment).
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    st.info("The night is dark. What knowledge do you seek?", icon="🌙")
# If that fails, it means we are running locally. Try to read from the key.txt file.
except:
    st.info("Cloud secrets not found. Attempting to read API key from local 'key.txt' file.", icon="💻")
    try:
        with open("key.txt", "r") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        st.error("No API key found. For cloud deployment, add a secret named OPENROUTER_API_KEY. For local use, create a 'key.txt' file.", icon="🚨")
        st.stop()

# Check if the key is empty
if not api_key:
    st.error("Your API key is empty. Please check your cloud secret or your local 'key.txt' file.", icon="🚨")
    st.stop()

# Initialize the OpenAI client with the key we found
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# --- END OF NEW AUTHENTICATION METHOD ---


# --- CHATBOT LOGIC (This part is the same as before) ---
# Initialize chat history in session state if it doesn't exist.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content":"You are the Joker from The Dark Knight. Your worldview is that chaos is the only true fairness. You see plans and rules as a bad joke. You speak with a slightly unhinged and theatrical tone, often using rhetorical questions and laughing unexpectedly (like 'heheh' or 'ha!'). You end your responses with a question or a thought-provoking, cynical statement about society or human nature. Introduce a little anarchy."}
    ]

# Display existing chat messages.
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Get user input from the chat input box.
if prompt := st.chat_input("What would you like to ask?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct-v0.2",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred with the AI model: {e}", icon="🚨")
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})