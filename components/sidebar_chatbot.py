import streamlit as st
import time
from tools.agent import generate_response

# stream data chunk by chunk
def stream_data(sentences):
    for word in sentences.split(" "):
        yield word + " "
        time.sleep(0.02)

def reset_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the sockg assistant bot! How can I help you?"},
    ]

def sidebar_chatbot():
    with st.sidebar:
        st.title("💬 Chatbot")

        message_container = st.container(height=700)
        for message in st.session_state.messages:
            message_container.chat_message(message["role"], avatar="🐱" if message["role"] == "assistant" else "🤠").write(message["content"])
        

        if prompt_text := st.chat_input("What is up?"):
            
            # add user message to session state
            user_prompt = {"role": "user", "content": prompt_text}
            st.session_state.messages.append(user_prompt)
            message_container.chat_message("user", avatar="🤠").write(prompt_text)
            
            # thinking spinner
            with st.spinner("Thinking..."):
                response_text = generate_response(prompt_text)

            # add bot response to session state
            bot_response = {"role": "assistant", "content": response_text}
            st.session_state.messages.append(bot_response)
            message_container.chat_message("user", avatar="🐱").write_stream(stream_data(response_text))

            st.button("Reset", type="primary", on_click=reset_chat_history)