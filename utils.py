import streamlit as st

def write_message(role, content, save = True):
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    with st.chat_message(role):
        st.markdown(content)
