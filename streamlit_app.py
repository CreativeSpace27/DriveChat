import streamlit as st
import requests
import time

# 1. Page Configuration
st.set_page_config(
    page_title="TailorTalk | AI Assistant",
    page_icon="📂",
    layout="centered"
)

st.markdown("""
    <style>

    
    /* Global Background */
    .stApp {
        background-color: #131314;
    }
    
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    .gemini-header {
        font-family: 'Google Sans', sans-serif;
        font-size: 2.2rem;
        font-weight: 500;
        color: #e3e3e3;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* USER MESSAGE ALIGNMENT */
    [data-testid="stChatMessageUser"] {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        background: transparent !important;
    }

    /* USER MESSAGE BUBBLE */
    [data-testid="stChatMessageUser"] .stMarkdown {
        background-color: #1f2028;
        padding: 1rem 1.5rem;
        border-radius: 18px;
        
        /* IMPORTANT */
        max-width: 65%;
        margin-left: auto;

        color: white;
    }
    
    /* Style User Message Content */
    [data-testid="stChatMessageUser"] .stMarkdown {
        background-color: #2b2c2f;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 4px 20px;
        display: inline-block;
        width: fit-content;
        margin-left: auto;
    }

    /* Target Assistant Messages for Left Alignment */
    [data-testid="stChatMessageAssistant"] {
        flex-direction: row;
        text-align: left;
        background-color: transparent !important;
    }

    /* Style Assistant Message Content */
    [data-testid="stChatMessageAssistant"] .stMarkdown {
        background-color: #1e1f20;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 4px;
        display: inline-block;
        width: fit-content;
    }

    /* Hide Avatars Completely */
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none;
    }

    /* Role Label Styling */
    .role-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #8e918f;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown('<h1 class="gemini-header">TailorTalk</h1>', unsafe_allow_html=True)

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello. I've synced with your Drive. How can I help?"}
    ]

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown('<div class="role-label">You</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="role-label">AI agent</div>', unsafe_allow_html=True)

        st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input("Ask a question..."):

    # User Message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown('<div class="role-label">You</div>', unsafe_allow_html=True)
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        st.markdown('<div class="role-label">Assistant</div>', unsafe_allow_html=True)

        response_placeholder = st.empty()

        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": prompt},
                timeout=60
            )

            if response.status_code == 200:

                answer = response.json().get(
                    "response",
                    "No response."
                )

                # Typewriter Effect
                full_response = ""

                for chunk in answer.split():
                    full_response += chunk + " "
                    time.sleep(0.04)

                    response_placeholder.markdown(
                        full_response + "●"
                    )

                response_placeholder.markdown(full_response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            else:
                st.error("API Error.")

        except Exception:
            st.error("Connection failed.")



