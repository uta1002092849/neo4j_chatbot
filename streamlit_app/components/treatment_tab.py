import streamlit as st
from api.dao.treatment import TreatmentDAO

def treatment_tab_component(driver):
    st.title("Treatment Exploration:")

    col1, col2 = st.columns(2)
    with col1:
        # Tillage and Residue Management
        tillage_options = ["All", "Conventional Till", "Conservation Till", "No Till", "Not Reported", "Sub Till"]
        tillage_help_text = "Tillage is the mechanical preparation of soil for planting and cultivation after planting. Choose 'All' to see all tillage types."
        selected_tillage = st.selectbox("Tillage Descriptor", tillage_options, help=tillage_help_text)
        
        residue_removal_options = ["All", "No", "Partial", "Yes"]
        residue_removal_help_text = "Residue removal is the process of removing crop remnants, such as leaves, stalks, and roots, from a field after harvest. Choose 'All' to see all residue removal types."
        selected_residue_removal = st.selectbox("Residue Removal", residue_removal_options, help=residue_removal_help_text)

    with col2:
        # Nutrient Management
        nitrogen_options = [
            "All", "0 N", "0 kg N/ha", "0 kgN/ha (N1)", "0 kg N/ha/y", "60 kgN/ha (N2)",
            "120 kgN/ha (N3)", "125 kg N/ha/y", "168 kg N/ha", "180 kgN/ha (N4)", "200 kg N/ha/y",
            "202 kg N/ha", "High N", "Low N"
        ]
        selected_nitrogen = st.selectbox("Nitrogen Amount", nitrogen_options)
        
        # Crop Management
        rotation_options = [
            "All", "Corn", "Corn, Oat/Clover, Sorghum, Soybean", "Corn, Soybean", "Corn, Soybean, Sorghum, Oat/Clover",
            "Soybean", "Soybean, Corn", "Soybean, Sorghum", "Sorghum", "Switchgrass"
        ]
        rotation_help_text = "Crop rotation is the practice of planting different crops in the same field over time. Choose 'All' to see all crop rotations."
        selected_rotation = st.selectbox("Rotation", rotation_options, help=rotation_help_text)
    
    # Second row of columns
    col3, col4, col5 = st.columns(3)
    
    with col3:
        help_text = "Belong to Experiment is a boolean value that indicates whether a treatment is part of an experiment. If selected, only treatments that are part of an experiment will be shown."
        belong_to_experiment = st.checkbox("Belong to Experiment", help=help_text)
    with col4:
        help_text = "Treatment Organic Management is value that indicates whether a treatment uses organic management. If selected, only treatments that use organic management will be shown."
        treatment_organic_management = st.checkbox("Treatment Organic Management", help=help_text)
    with col5:
        help_text = "Irrigation is a boolean value that indicates whether a treatment uses irrigation. If selected, only treatments that use irrigation will be shown."
        selected_irrigation = st.checkbox("Irrigation", help=help_text)
    
    # Get filtered treatments
    treatment_dao = TreatmentDAO(driver)
    filtered_treatments = treatment_dao.get_filtered_treatments(selected_tillage, selected_rotation, belong_to_experiment, selected_nitrogen, selected_irrigation, selected_residue_removal, treatment_organic_management)
    
    # select treatment
    if filtered_treatments.empty:
        st.write("No treatments found.")
    else:
        st.info(f"Number of treatments found: {filtered_treatments.shape[0]}")
        st.dataframe(filtered_treatments, use_container_width=True)
        selected_treatment = st.selectbox("Select a treatment to explore:", filtered_treatments['ID'])
        st.write(f"Selected treatment: {selected_treatment}")
        