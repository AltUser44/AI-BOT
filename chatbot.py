import os
from openai import OpenAI
import streamlit as st
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
api_key = os.getenv("OPEN_API_KEY")

# Check if the API key was loaded properly
if not api_key:
    st.error("API key not found. Please make sure it is set in your environment variables.")

# Set OpenAI API key
client = OpenAI(api_key=api_key)

# Add custom CSS for hover effects
st.markdown(
    """
    <style>
    /* Style for the input box */
    .stTextInput {
        background-color: #f9f9f9;
        border: 2px solid #ddd;
        border-radius: 5px;
        transition: all 0.3s ease-in-out;
    }

    /* Hover effect for the input box */
    .stTextInput:hover {
        border-color: #66cc66; /* Green border on hover */
        box-shadow: 0 0 10px rgba(102, 204, 102, 0.5); /* Green glow */
    }

    /* Style for messages */
    .stMarkdown {
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    /* Hover effect for user messages */
    .stMarkdown:hover {
        background-color: #e6ffe6; /* Light green on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Use relative or absolute path for the GIF
gif_path = "hello-there-hi.gif"

# Verify file existence and display the resized GIF
if os.path.exists(gif_path):
    st.image(gif_path, caption="")
else:
    st.error(f"File not found: {gif_path}")

# Initialize chat history
if "messages" not in st.session_state:
    positive_messages = [
        "Hi! I'm here to help 😊",
        "How can I assist you today?",
        "You're awesome! Let's chat 🤩",
        "Need help? Just ask! 💡",
    ]
    # Choose a random positive message for the system role
    system_message = random.choice(positive_messages)
    st.session_state["messages"] = [{"role": "system", "content": system_message}]

# Display chat messages from history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Respond to user input
prompt = st.chat_input("What's up?")
if prompt:
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # API Call using GPT-4
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=st.session_state["messages"],
                model="gpt-4",
            )

            # Extract the assistant's response
            assistant_response = response.choices[0].message.content

            # Display the response
            st.markdown(assistant_response)

            # Add assistant response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": assistant_response})

        except Exception as e:
            # Handle API errors gracefully
            st.error(f"Error communicating with OpenAI API: {e}")
