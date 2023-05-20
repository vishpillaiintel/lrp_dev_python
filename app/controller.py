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


@st.cache_data(show_spinner="Fetching data...")
def get_lrp_data():  
    lrp_m = model.LRP_Model()
    df = lrp_m.get_data_csv()
    return df

def get_db_data():
    lrp_m2 = model.LRP_Model()
    
    df = lrp_m2.get_data(table_name='Forms')
    return df

df = get_lrp_data()
form = model.Form(form_name='RoT')
form.get_Form_Attributes()



# Create model instances
rot_m = model.RoT_Model()
me_m = model.Manual_Entry_Model()

# Create view instances
lrp_v = view.LRP_View(df)
pa_v = view.PA_View()
de_v = view.Data_Entry_View(rot_m, me_m)

page_names_to_funcs = {
    "LRP": lrp_v.view,
    "Product Architecture": pa_v.view,
    "Data Entry": de_v.view,
}

selected_page = st.sidebar.selectbox("Select a View", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

