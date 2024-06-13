import streamlit as st
from tools.text2cypher import generate_cypher
from api.dao.general import GeneralDAO
from tools.rating import save_ratings

def text2cypher_component(driver, gemini_pro):
    
    state = st.session_state
    
    def upvote_callback():
        save_ratings(state['user_input'], state['cypher_code'], "up")
        state.rated = True

    def downvote_callback():
        save_ratings(state['user_input'], state['cypher_code'], "down")
        state.rated = True

    def init_state(key, value):
        if key not in state:
            state[key] = value
    
    # generic callback to set state
    def _set_state_cb(**kwargs):
        for state_key, widget_key in kwargs.items():
            val = state.get(widget_key, None)
            if val is not None or val == "":
                setattr(state, state_key, state[widget_key])
        
    # initialize state
    init_state('cypher_code', None)
    init_state('query_result', None)
    init_state('user_input', None)
    init_state('rated', False)
    init_state('run_query', False)

    def _set_run_query_cb():
        state['run_query'] = True
        state['rated'] = False
        state['cypher_code'] = None
        state['query_result'] = None
            

    # Main input for text2cypher model
    st.write("Text2Cypher")
    st.write("This is a text2cypher model that generates cypher queries based on natural language input.")
    st.write("Example: Return all experimental units?")
    
    # Use the session state for the text input
    st.text_input(
        "Query: ", value=state.user_input, key='user_input',
        on_change=_set_state_cb, kwargs={'user_input': 'user_input'}
    )

    st.button(
        "Generate", on_click=_set_run_query_cb, args=()
    )
    
    if state['run_query']:
        with st.spinner("Generating Cypher..."):
            try:
                response = generate_cypher(state['user_input'])
                state['cypher_code'] = response['constructed_cypher']
                state['run_query'] = False
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    # Update the session state when the input changes
    if state['cypher_code']:
        # display the cypher code
        st.code(state['cypher_code'], language='cypher')
        
        # display query result
        general_dao = GeneralDAO(driver)
        query_result = general_dao.run_query(state['cypher_code'])
        st.dataframe(data=query_result, hide_index=False)
        
    if not state['rated'] and state['cypher_code']:
        st.write("Rate this response:")
        col1, col2 = st.columns(2)
        with col1:
            st.button("👍", key="upvote", on_click=upvote_callback)
        with col2:
            st.button("👎", key="downvote", on_click=downvote_callback)
    
    if state['rated'] and state['cypher_code']:
        st.write("Thanks for your feedback!")