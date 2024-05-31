import streamlit as st
from agent import generate_response
import time
from api.neo4j import init_driver, close_driver
from api.dao.experimentalUnit import ExperimentalUnitDAO
from api.dao.field import FieldDAO

# Initialize Neo4j driver
uri = st.secrets["NEO4J_URI"]
user = st.secrets["NEO4J_USERNAME"]
password = st.secrets["NEO4J_PASSWORD"]
driver = init_driver(uri, user, password)


# Page config and icon
st.set_page_config("SOCKG Chat Bot", page_icon=":evergreen_tree:")


# Initialize bot messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the sockg assistant bot! How can I help you?"},
    ]

# stream data
def stream_data(sentences):
    for word in sentences.split(" "):
        yield word + " "
        time.sleep(0.02)


def reset_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the sockg assistant bot! How can I help you?"},
    ]
    message_container.empty()

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

    col1, col2 = st.columns([3.5, 1])
    with col2:
        # Clear chat history button
        st.button("Reset", type="primary", on_click=reset_chat_history)


# Main content
field_tab, expUnit_tab, treatment_tab = st.tabs(["Fields", "Experimental Units", "Treatments"])


with field_tab:
    st.write("Fields")

    # Get all fields from the database
    field_dao = FieldDAO(driver)
    fields = field_dao.get_all_ids()

    option = st.selectbox("Select a field to explore:", fields)

    # Get experimental unit data
    exp_units = field_dao.get_all_experimental_unit(option)
    st.write("Total experimental units:", len(exp_units))

    # print out a table of experimental units
    st.dataframe(exp_units)
    
    # Get latitude and longitude of the selected field
    df = field_dao.get_lat_long_dataframe(option)
    
    # map
    st.map(df, latitude='latitude', longitude='longitude')

    # get rainfall data
    rainfall_df = field_dao.get_rainfall_df(option)
    st.bar_chart(rainfall_df, x='period', y='totalPrecipitation')

with expUnit_tab:
    st.write("Experimental Units")

with treatment_tab:
    st.write("Treatments")



