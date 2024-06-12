import streamlit as st
from tools.text2cypher import generate_cypher
from api.dao.general import GeneralDAO
from tools.rating import save_ratings

def text2cypher_component(driver, gemini_pro):

    if "cypher_code" not in st.session_state:
        st.session_state.cypher_code = None
    if "query_result" not in st.session_state:
        st.session_state.query_result = None
    if 'prompt_text' not in st.session_state:
        st.session_state.prompt_text = None
    if 'rated' not in st.session_state:
        st.session_state.rated = False

    def set_result(prompt_text):
        response = generate_cypher(prompt_text)
        st.session_state.prompt_text = prompt_text
        cypher_code = response['constructed_cypher']
        st.session_state.cypher_code = cypher_code
        st.session_state.rated = False

    # Main input for text2cypher model
    st.write("Text2Cypher")
    st.write("This is a text2cypher model that generates cypher queries based on natural language input.")
    st.write("Example: How to find the total number of experimental unit for all treatment?")
    
    # Use the session state for the text input
    prompt_text = st.text_input("Enter your question here:")

    # Display the button if text is entered
    if st.button("Generate"):
        with st.spinner("Generating..."):
            set_result(prompt_text)
    
    # Update the session state when the input changes
    if st.session_state['cypher_code']:
        cypher_code = st.session_state['cypher_code']
        st.code(cypher_code, language='cypher')
        general_dao = GeneralDAO(driver)
        query_result = general_dao.run_query(cypher_code)
        st.dataframe(data=query_result, hide_index=False)
        
        if not st.session_state.rated:
            st.write("Rate this response:")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍", key="upvote"):
                    save_ratings(st.session_state['prompt_text'], st.session_state['cypher_code'], "up")
                    st.session_state.rated = True
                    st.experimental_rerun()
            with col2:
                if st.button("👎", key="downvote"):
                    save_ratings(st.session_state['prompt_text'], st.session_state['cypher_code'], "down")
                    st.session_state.rated = True
                    st.experimental_rerun()
        else:
            st.write("Thanks for your feedback!")