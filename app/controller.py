import streamlit as st
import pandas as pd
import numpy as np

import model
import view
from dotenv import load_dotenv

load_dotenv()

# dev or prod choice with LRP_DB
modes = {'d': 'dev', 'p': 'prod'}
mode = modes['d']

st.set_page_config(
    page_title="ATTD LRP Portal",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create a sidebar
st.sidebar.image('theme/logo.png', use_column_width=True)

new_title = '<p style="color:#333333; font-size: 28px; text-align:center;">ATTD LRP Portal</p>'
st.sidebar.markdown(new_title, unsafe_allow_html=True)

# Create lrp view based on master table
lrp_m = model.LRP_Model(mode)
lrp_m.create_LRP_master()
lrp_v = view.LRP_View(lrp_m.master)

# Create data entry view based on form chosen by user
de_m = model.Data_Entry_Model(mode)
de_v = view.Data_Entry_View(de_model=de_m)

# Create resubmission review for users to resubmit their rejected data
rs_m = model.Resubmission_Model(mode)
rs_v = view.Resubmission_View(rs_model=rs_m)

# Create data review view for admin to review pending data
dr_m = model.Data_Review_Model(mode)
dr_v = view.Data_Review_View(dr_model=dr_m)

page_names_to_funcs = {
    "LRP": lrp_v.view,
    "Data Entry": de_v.view,
    "Resubmission": rs_v.view,
    "Data Review": dr_v.view
}

selected_page = st.sidebar.selectbox("Select a View", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

