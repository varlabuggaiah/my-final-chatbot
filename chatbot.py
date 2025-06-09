# Import necessary libraries
import os
from openai import OpenAI
import datetime # Library to get the current date and time for filenames

# --- A Function to Save the Conversation ---
# It's good practice to put reusable code into a function.
def save_conversation(history, model_name):
    # Create a unique filename using the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chatlog_{timestamp}.txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- Chat Log from {timestamp} ---\n")
            f.write(f"--- Model Used: {model_name} ---\n\n")
            
            # Write each message from the history to the file
            for message in history:
                # Capitalize the role (e.g., "user" becomes "User")
                role = message['role'].capitalize()
                content = message['content']
                f.write(f"{role}:\n{content}\n\n")
                
        print(f"\n--- Conversation saved to {filename} ---\n")
    except Exception as e:
        print(f"\n--- Error saving file: {e} ---\n")

# ------------------- CONFIGURATION -------------------
# ### MOST IMPORTANT STEP ###
# Paste your secret OpenRouter API key here.
OPENROUTER_API_KEY = "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"

# You can change the model or the AI's personality here anytime.
MODEL_NAME = "mistralai/mistral-7b-instruct-v0.2"
AI_PERSONALITY = "You are a helpful and friendly assistant."
# -----------------------------------------------------

# Initialize the OpenAI client, pointing it to the OpenRouter API
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

# This list will store the conversation history
conversation_history = [
    {"role": "system", "content": AI_PERSONALITY}
]

# --- Welcome Message ---
print(f"--- Chatbot Initialized with model: {MODEL_NAME} ---")
print("--- Special Commands: 'quit', 'clear', 'save' ---")

# --- Main Chat Loop ---
while True:
    # Get input from the user
    user_input = input("You: ")

    # --- Command Handling ---
    if user_input.lower() == 'quit':
        print("Goodbye! Your session is over.")
        break
    
    elif user_input.lower() == 'clear':
        # Reset the conversation history
        conversation_history = [{"role": "system", "content": AI_PERSONALITY}]
        print("\n--- Conversation history cleared. ---\n")
        continue # Skip the API call and ask for new input
        
    elif user_input.lower() == 'save':
        save_conversation(conversation_history, MODEL_NAME)
        continue # Continue the chat after saving

    # --- API Call ---
    # Add the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Send the request to OpenRouter
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=conversation_history
        )

        # Get the AI's response message
        ai_message = response.choices[0].message
        
        # Add the AI's response to the history
        conversation_history.append(ai_message)

        # Print the AI's response
        print(f"AI: {ai_message.content}")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Remove the last user message from history if the API call failed
        conversation_history.pop()