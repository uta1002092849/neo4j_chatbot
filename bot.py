import streamlit as st
from utils import write_message
from agent import generate_response

st.set_page_config("Text2Cypher", page_icon=":movie_camera:")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the sockg assitant bot!  How can I help you?"},
    ]

def handle_submit(message):

    with st.spinner('Thinking...'):
        
        response = generate_response(message)

        write_message('assistant', response)


for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

if prompt := st.chat_input("What is up?"):
    
    # Display user message in chat message container
    write_message('user', prompt)

    # Generate a response
    handle_submit(prompt)