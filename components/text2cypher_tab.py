import streamlit as st
from tools.text2cypher import generate_cypher
from api.dao.general import GeneralDAO
from pandasai import SmartDataframe

def text2cypher_component(driver, gemini_pro):
    # Initialize session state
    if 'response' not in st.session_state:
        st.session_state.response = None
    if 'query_result' not in st.session_state:
        st.session_state.query_result = None

    # Main input for text2cypher model
    st.write("Text2Cypher")
    st.write("This is a text2cypher model that generates cypher queries based on natural language input.")
    st.write("Example: How to find the total number of experimental unit for all treatment?")
    prompt_text = st.text_input("Enter a question")

    if prompt_text:
        # Only regenerate response if the prompt_text is updated
        if st.session_state.get('last_prompt') != prompt_text:
            st.session_state.last_prompt = prompt_text
            with st.spinner("Thinking..."):
                st.session_state.response = generate_cypher(prompt_text)
            
            if st.session_state.response['constructed_cypher'] == "":
                st.write("Sorry, I'm not able to generate a cypher query for this question. Please rephrase the question to be more concise or ask another question.")
            else:
                st.session_state.query_result = None  # Reset query result when a new cypher is generated
                st.code(st.session_state.response['constructed_cypher'], language='cypher')

    # Execute the cypher query against the database and display results
    if st.session_state.response and st.session_state.response['constructed_cypher']:
        if st.session_state.query_result is None:  # Run query only once
            general_dao = GeneralDAO(driver)
            st.session_state.query_result = general_dao.run_query(st.session_state.response['constructed_cypher'])
        st.dataframe(data=st.session_state.query_result, hide_index=False)

        # Inner input for visualization query
        viz_query = st.text_area("Do you want to visualize the data? (Ask something like show me a bar chart of ...)")
        if st.button("Visualize"):
            with st.spinner("Thinking..."):
                try:
                    sdf = SmartDataframe(
                        st.session_state.query_result,
                        config={
                            "llm": gemini_pro,
                        },
                    )
                    st.image(sdf.chat(viz_query))
                except Exception as e:
                    st.write("Sorry, I'm not able to visualize the data. Please rephrase the prmopt to be more percific or try another question.")
