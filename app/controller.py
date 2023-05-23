import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

import model
import view
import config

from dotenv import load_dotenv

load_dotenv()

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
# lrp_m = model.LRP_Model()
# lrp_m.create_LRP_master()
# lrp_v = view.LRP_View(lrp_m.master)

# Create data entry view based on form chosen by user
de_m = model.Data_Entry_Model()
de_v = view.Data_Entry_View(de_model=de_m)

page_names_to_funcs = {
    #"LRP": lrp_v.view,
    "Data Entry": de_v.view,
}

selected_page = st.sidebar.selectbox("Select a View", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

