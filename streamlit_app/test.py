import streamlit as st

pg = st.navigation([st.Page("pages/_ExperimentalUnits.py"), st.Page("pages/_Treatments.py")])

st.sidebar.selectbox("Group", ["A", "B", "C"], key="group")
st.sidebar.slider("Size", 1, 5, key="size")

# initialize selected experimental unit in session state if not already initialized
if 'selected_exp_unit' not in st.session_state:
    st.session_state.selected_exp_unit = None

pg.run()