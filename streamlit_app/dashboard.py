from api.neo4j import init_driver
import streamlit as st


from models.llms import gemini_pro
from components.sidebar_chatbot import sidebar_chatbot
from components.field_tab import field_tab_component
from components.expUnit_tab import expUnit_tab_component
from components.text2cypher_tab import text2cypher_component

# Page config and icon
st.set_page_config(layout="wide", page_title="SOCKG Chat Bot", page_icon=":evergreen_tree:")

# hide hamburger menu, deploy button, and footer
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

driver = init_driver()


# Initialize bot messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the sockg assistant bot! How can I help you?"},
    ]

sidebar_chatbot()

# Main content
field_tab, expUnit_tab, text2cypher = st.tabs(["Fields", "Experimental Units", "Text2Cypher"])


with field_tab:
    field_tab_component(driver)

with expUnit_tab:
    expUnit_tab_component(driver)

# with treatment_tab:
#     treatment_tab_component(driver)

with text2cypher:
    text2cypher_component(driver, gemini_pro)