
import streamlit as st
import pandas as pd
import numpy as np
import datetime

class LRP_View:
    
    def __init__(self, df):
        self.df = df

    def df_group_by(self, df, col1, col2):
        grouped_data = df.groupby([col1, col2])
        groups = list(grouped_data.groups.keys())

        for group in groups:
            group_data = grouped_data.get_group(group)
            group_data = group_data.reset_index()
            st.write(f"{group_data['Product Name'][0]} {group_data['Skew Name'][0]}")
            group_data = group_data.set_index('Milestone')
            if str(group_data['PQS'][0]) == 'N/A':
                group_data = group_data.drop(['Product Name', 'index', 'PQS', 'Skew Name', 'Package Type'], axis=1)
            else:
                group_data = group_data.drop(['Product Name', 'index', 'Skew Name', 'Package Type'], axis=1)
            st.dataframe(group_data)

    def view(self):
        m=st.markdown("""
                        <style>

                        div.stTitle {

                        font-size:0.5px;

                        }

                        div.stHeader {

                        font-size:0.2px;

                        }

                        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                            font-size:1rem;
                        }

                        </style>
                        """, unsafe_allow_html=True)
        st.title("LRP Summary")
        client, server, graphics, asic, psg = st.tabs(["**:blue[Client]**", "**:blue[Server]**", "**:blue[Graphics]**", "**:blue[ASIC]**", "**:blue[PSG]**"])

        with client:
            df_client = self.df[self.df['Package Type'] == 'Client']
            self.df_group_by(df_client, 'Product Name', 'Skew Name')
        
        with server:
            df_server = self.df[self.df['Package Type'] == 'Server']
            self.df_group_by(df_server, 'Product Name', 'Skew Name')

        with graphics:
            df_graphics = self.df[self.df['Package Type'] == 'Graphics']
            self.df_group_by(df_graphics, 'Product Name', 'Skew Name')

        with asic:
            df_asic = self.df[self.df['Package Type'] == 'ASIC']
            self.df_group_by(df_asic, 'Product Name', 'Skew Name')

        with psg:
            df_psg = self.df[self.df['Package Type'] == 'PSG']
            self.df_group_by(df_psg, 'Product Name', 'Skew Name')

class PA_View():
    def __init__(self):
        pass
    
    def view(self):
        st.write("Product Architecture")


class Data_Entry_View():
    def __init__(self, de_model):
        self.de_model = de_model

    def rot_view(self):
        self.de_model.submission.create_Form('RoT')

        col1, col2 = st.columns(2)
        m=st.markdown("""
                        <style>

                        div.stTitle {

                        font-size:0.5px;

                        }

                        div.stHeader {

                        font-size:0.2px;

                        }

                        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                            font-size:1rem;
                        }

                        </style>
                        """, unsafe_allow_html=True)
        
        if 'RoT_Button' not in st.session_state:
            st.session_state['RoT_Button'] = False

        if 'DB_Submission' not in st.session_state:
            st.session_state['DB_Submission'] = False

        def rerun():
            st.session_state['RoT_Button'] = False


        with col1:
            st.write('**_General Information_**')

            product_name_input = st.text_input(label=self.de_model.submission.form.fields['Product_Name']['Field_Question'], value='', key='product_name_rot', on_change=rerun)
            optional_skew_checkbox_input = st.checkbox(label=self.de_model.submission.form.fields['Skew_Name']['Field_Question'], key='optional_skew_rot', on_change=rerun)

            if optional_skew_checkbox_input:
                skew_name_input = st.text_input(label='Skew Name', value='', key='skew_name_rot', on_change=rerun)
            else:
                skew_name_input = ''

            package_type_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Package_Type']['Field_Selection'], key='package_type_rot', on_change=rerun)
            
            package_type_estim_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type_Estimation']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Package_Type_Estimation']['Field_Selection'], key='package_type_estimation_rot', on_change=rerun)
            
            num_main = st.number_input(label=self.de_model.submission.form.fields['Number_of_Main_Die']['Field_Question'], \
                                        min_value=self.de_model.submission.form.fields['Number_of_Main_Die']['Min_Value'], \
                                        max_value=self.de_model.submission.form.fields['Number_of_Main_Die']['Max_Value'], \
                                        value=self.de_model.submission.form.fields['Number_of_Main_Die']['Default_Value'], key='num_main_rot', on_change=rerun)
            exist_emib_input = st.selectbox(label=self.de_model.submission.form.fields['Exist_EMIB']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Exist_EMIB']['Field_Selection'], key='exist_emib_rot', on_change=rerun)
            
            exist_point_input = st.selectbox(label=self.de_model.submission.form.fields['Exist_POINT']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Exist_POINT']['Field_Selection'], key='exist_point_rot', on_change=rerun)
        with col2:
            st.write('**_WLA Information_**') 
            wla_architect_input = st.selectbox(label=self.de_model.submission.form.fields['WLA_Architecture']['Field_Question'], \
                                                options=self.de_model.submission.form.fields['WLA_Architecture']['Field_Selection'], key='wla_architect_rot', on_change=rerun)
            
            chiplet_num = st.number_input(label=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Field_Question'], \
                                        min_value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Min_Value'], \
                                        max_value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Max_Value'], \
                                        value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Default_Value'], key='chiplet_num_rot', on_change=rerun)
            
            dow_architect_input = 'No WLA'
            odi_chiplet_size_input = 'No WLA'
            hbi_architect_input = 'No WLA'
            signal_area_hbi = 0
            if wla_architect_input == 'Foveros DoW':
                dow_architect_input = st.selectbox(label=self.de_model.submission.form.fields['DoW_Architecture']['Field_Question'], \
                                                options=self.de_model.submission.form.fields['DoW_Architecture']['Field_Selection'], key='dow_architect_rot', on_change=rerun)
            elif wla_architect_input == 'ODI':
                odi_chiplet_size_input = st.selectbox(label=self.de_model.submission.form.fields['ODI_Chiplet_Size']['Field_Question'], \
                                                options=self.de_model.submission.form.fields['ODI_Chiplet_Size']['Field_Selection'], key='odi_chiplet_size_rot', on_change=rerun)
            elif wla_architect_input == 'HBI':
                hbi_architect_input = st.selectbox(label=self.de_model.submission.form.fields['HBI_Architecture']['Field_Question'], \
                                                options=self.de_model.submission.form.fields['HBI_Architecture']['Field_Selection'], key='hbi_architect_rot', on_change=rerun)
                
                signal_area_hbi = st.number_input(label=self.de_model.submission.form.fields['Signal_Area']['Field_Question'], \
                                        min_value=self.de_model.submission.form.fields['Signal_Area']['Min_Value'], \
                                        max_value=self.de_model.submission.form.fields['Signal_Area']['Max_Value'], \
                                        value=self.de_model.submission.form.fields['Signal_Area']['Default_Value'], key='signal_area_rot', on_change=rerun)
            st.write('**_Other Information_**')
            die_architect_input = st.selectbox(label=self.de_model.submission.form.fields['Die_Architecture_Summary']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Die_Architecture_Summary']['Field_Selection'], key='die_architect_rot', on_change=rerun)
            
            type_num_satellite = st.number_input(label=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Field_Question'], \
                                                min_value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Min_Value'], \
                                                max_value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Max_Value'], \
                                                value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Default_Value'], key='type_num_satellite_rot', on_change=rerun)
            
            exist_hbm = st.selectbox(label=self.de_model.submission.form.fields['Exist_HBM']['Field_Question'], \
                                    options=self.de_model.submission.form.fields['Exist_HBM']['Field_Selection'], key='exist_hbm_rot', on_change=rerun)
            
            lifetime_volume = st.selectbox(label=self.de_model.submission.form.fields['Lifetime_Volume']['Field_Question'], \
                                        options=self.de_model.submission.form.fields['Lifetime_Volume']['Field_Selection'], key='lifetime_vol_rot', on_change=rerun)

            architecture_maturity_input = st.selectbox(label=self.de_model.submission.form.fields['Architecture_Maturity']['Field_Question'], \
                                        options=self.de_model.submission.form.fields['Architecture_Maturity']['Field_Selection'], key='architecture_mat_rot', on_change=rerun)

        result, lrp_output = self.de_model.rot_model.lrp_prediction(product_name=product_name_input, skew_name=skew_name_input, chiplet_num=chiplet_num, \
                                            pkg_type=package_type_estim_input, pkg_class=package_type_input, main_num=num_main, exist_emib=exist_emib_input, \
                                            point_pkg=exist_point_input, lifetime_vol_input_val=lifetime_volume, \
                                            wla_architect=wla_architect_input, dow_architect_input_val=dow_architect_input, \
                                            odi_chiplet_size=odi_chiplet_size_input, hbi_architect=hbi_architect_input, signal_area_hbi=signal_area_hbi,  \
                                            exist_hbm_input_val=exist_hbm, die_architect_input_val=die_architect_input, type_num_satellite_input_val=type_num_satellite, \
                                            architecture_maturity_val=architecture_maturity_input)

        st.divider()
        
        if st.button('**Run Data Prediction**'):
            st.session_state['RoT_Button'] = True
            st.write(f'Product Name: {product_name_input} {skew_name_input}')
            st.write(f'Package Type: {package_type_input}')
            st.dataframe(result)

        if st.session_state['RoT_Button']:
            if st.button('**Submit to Database?**'):
                with st.spinner('Writing to Database...'):
                    st.session_state['DB_Submission'] = not st.session_state['DB_Submission']        
                    user_id='vpillai'
                    field_values_dict = lrp_output
                    self.de_model.submission.set_Submission_Attributes(user_id=user_id, field_values_dict=field_values_dict)
                    record = self.de_model.submission.publish_Submission()
                    st.write(record)
                st.session_state['RoT_Button'] = False


    def me_view(self):
        col1, col2 = st.columns(2)
        m=st.markdown("""
                        <style>

                        div.stTitle {

                        font-size:0.5px;

                        }

                        div.stHeader {

                        font-size:0.2px;

                        }

                        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                            font-size:1rem;
                        }

                        </style>
                        """, unsafe_allow_html=True)
        
        if 'ME_Button' not in st.session_state:
            st.session_state['ME_Button'] = False

        def rerun():
            st.session_state['ME_Button'] = False
        
        with col1:

            st.write('**_Product Information_**')
            
            self.de_model.submission.create_Form('Manual Entry')
            self.de_model.submission.form.set_Fields()

            product_type_input = st.text_input(label=self.de_model.submission.form.fields['Product_Name']['Field_Question'], value='', key='product_name_me', on_change=rerun)
            
            optional_skew_checkbox_input = st.checkbox(label=self.de_model.submission.form.fields['Skew_Name']['Field_Question'], key='optional_skew_me', on_change=rerun)

            if optional_skew_checkbox_input:
                skew_name_input = st.text_input(label='Skew Name', value='', key='skew_name_me', on_change=rerun)
            else:
                skew_name_input = ''

            package_type_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Package_Type']['Field_Selection'], key='package_type_me', on_change=rerun)

        with col2:
            st.write('**_Other Information_**')
            die_architect_input = st.selectbox(label=self.de_model.submission.form.fields['Die_Architecture']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Die_Architecture']['Field_Selection'], key='die_arch_me', on_change=rerun)
            
            if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
                wla_arch_maturity_input = st.selectbox(label=self.de_model.submission.form.fields['WLA_Architecture_Maturity']['Field_Question'], \
                                                    options=self.de_model.submission.form.fields['WLA_Architecture_Maturity']['Field_Selection'], key='wla_maturity_me', on_change=rerun)

            pkg_assemb_maturity_input = st.selectbox(label=self.de_model.submission.form.fields['Pkg_Assembly_Architecture_Maturity']['Field_Question'], \
                                                    options=self.de_model.submission.form.fields['Pkg_Assembly_Architecture_Maturity']['Field_Selection'], key='pkg_assemb_maturity_me', on_change=rerun)
        
        if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
            with col2:
                st.write('**_PRQ WLA Information_**')
                prq_wla_rtd_input = st.number_input(label='PRQ WLA RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f", on_change=rerun)
                prq_wla_test_input = st.number_input(label='PRQ WLA Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f", on_change=rerun)
            with col1:
                st.write('**_PRQ Pkg Information_**')
                prq_pkg_assemb_rtd_input = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f", on_change=rerun)
                prq_pkg_test_piyl_input = st.number_input(label='PRQ Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f", on_change=rerun)
                prq_pkg_assemb_finish_input = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f", on_change=rerun)
        else:
            with col1:
                st.write('**_PRQ Pkg Information_**')
                prq_pkg_assemb_rtd_input = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f", on_change=rerun)
                prq_pkg_test_piyl_input = st.number_input(label='PRQ Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f", on_change=rerun)
                prq_pkg_assemb_finish_input = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f", on_change=rerun)
        
        if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
            result, lrp_output = self.de_model.me_model.lrp_prediction(product_name=product_type_input, skew_name=skew_name_input, pkg_class=package_type_input, \
                                Die_Architecture_Info_val=die_architect_input, WLA_Maturity=wla_arch_maturity_input, \
                                Pkg_Assemb_Maturity=pkg_assemb_maturity_input, PRQ_WLA_RtD=prq_wla_rtd_input, \
                                PRQ_WLA_Test_PIYL=prq_wla_test_input, PRQ_Pkg_Assemb_RtD=prq_pkg_assemb_rtd_input, \
                                PRQ_Pkg_Test_PIYL=prq_pkg_test_piyl_input, PRQ_Pkg_Assemb_Finish=prq_pkg_assemb_finish_input)
        else:
            result, lrp_output = self.de_model.me_model.lrp_prediction(product_name=product_type_input, skew_name=skew_name_input, pkg_class=package_type_input, \
                            Die_Architecture_Info_val=die_architect_input, WLA_Maturity=None, \
                            Pkg_Assemb_Maturity=pkg_assemb_maturity_input, PRQ_WLA_RtD=None, \
                            PRQ_WLA_Test_PIYL=None, PRQ_Pkg_Assemb_RtD=prq_pkg_assemb_rtd_input, \
                            PRQ_Pkg_Test_PIYL=prq_pkg_test_piyl_input, PRQ_Pkg_Assemb_Finish=prq_pkg_assemb_finish_input)
        
        st.divider()

        if st.button('**Run Data Prediction**', key='run_prediction_me'):
            st.session_state['ME_Button'] = True
            st.write(f'Product Name: {product_type_input} {skew_name_input}')
            st.write(f'Package Type: {package_type_input}')
            st.dataframe(result)
        
        if st.session_state['ME_Button']:
            if st.button('**Submit to Database?**', key='submit_database_me'):
                with st.spinner('Writing to Database...'):
                    user_id='vpillai'
                    field_values_dict = lrp_output
                    self.de_model.submission.set_Submission_Attributes(user_id=user_id, field_values_dict=field_values_dict)
                    record = self.de_model.submission.publish_Submission()
                    st.write(record)
                st.session_state['ME_Button'] = False

    def view(self):
        st.title("Data Entry")
        rot, man_ent = st.tabs(["**:blue[RoT]**", "**:blue[Manual Entry]**"])

        with rot:
            self.rot_view()
    
        with man_ent:
            self.me_view()



class Data_Review_View():
    
    def __init__(self, dr_model):
        self.dr_model = dr_model
        self.pending_options = {}
    
    def create_pending_options(self):
        self.dr_model.get_Pending_Submissions()
        for pending_submission in self.dr_model.pending_submissions:
            self.pending_options[f'Submission ID: {pending_submission.submission_id}, ' + \
                                f'User ID: {pending_submission.user_id}, ' +  f'Submission Date: {pending_submission.submission_date}'] = pending_submission.submission_id
        return self.pending_options


    def view(self):

        m=st.markdown("""
                        <style>

                        div.stTitle {

                        font-size:0.5px;

                        }

                        div.stHeader {

                        font-size:0.2px;

                        }

                        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                            font-size:1rem;
                        }

                        </style>
                        """, unsafe_allow_html=True)
        
        st.title("Data Review")
        
        # hardcoding user, need to update later with SSO
        user_id = 'vpillai' 

        self.create_pending_options()
        options=list(self.pending_options.keys())
        selected_pending_option = st.selectbox(label='Pick a Pending Submission to be Reviewed:', options=options)
        
        col1, col2 = st.columns([1,1])


        if options:
            with col1:
                get_submission_button = st.button(label='**Pull Data for Review**')
            with col2:
                reset_button = st.button(label='**:red[Reset]**')
        
        if 'get_sub_key' not in st.session_state:
            st.session_state['get_sub_key'] = False

        if options and reset_button:
            st.session_state['get_sub_key'] = False

        if options and get_submission_button:
            st.session_state['get_sub_key'] = True
        
        if options and st.session_state['get_sub_key']:
            self.dr_model.set_Submission_to_Review(self.pending_options[selected_pending_option])
            table = pd.Series(self.dr_model.submission_review.field_values_dict)
            st.table(table)
            reviewed = st.selectbox(label='Change Status: ', options=['Leave as Pending', 'Approve', 'Reject'], index=0)
            if st.button(label='**Submit to Database**', key='Review_DB'):
                if reviewed=='Approve':
                    with st.spinner('Writing to Database...'):
                        record = self.dr_model.create_Approval(user_id=user_id, field_values_dict=self.dr_model.submission_review.field_values_dict)
                        st.write(record)

                elif reviewed=='Reject':
                    with st.spinner('Writing to Database...'):
                        record = self.dr_model.submission_review.update_Submission(status='Rejected', field_values_dict=self.dr_model.submission_review.field_values_dict)
                        st.write(record)
                else:
                    st.write('Submission has been left as pending.')
                st.session_state['get_sub_key'] = False


class Resubmission_View():

    def __init__(self, rs_model):
        self.rs_model = rs_model
        self.rejected_options = {}

    def create_rejected_options(self, user_id):
        self.rs_model.get_Rejected_Submissions(user_id)
        for rejected_submission in self.rs_model.rejected_submissions:
            self.rejected_options[f'Submission ID: {rejected_submission.submission_id}, ' + \
                                f'User ID: {rejected_submission.user_id}, ' + \
                                f'Submission Date: {rejected_submission.submission_date}'] = rejected_submission.submission_id
        return self.rejected_options
    
    def get_index_selection(self, selection_options, value):
        if str(value) == 'None':
            return 0
        else:
            return selection_options.index(value)
    
    def get_PRQ_value(self, key):
        if key not in self.rs_model.submission_resubmit.field_values_dict:
            return 99.0
        else:
            return float(self.rs_model.submission_resubmit.field_values_dict[key])

    def view(self):
        m=st.markdown("""
                        <style>

                        div.stTitle {

                        font-size:0.5px;

                        }

                        div.stHeader {

                        font-size:0.2px;

                        }

                        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                            font-size:1rem;
                        }

                        </style>
                        """, unsafe_allow_html=True)
        
        st.title("Resubmission")

        # hardcoding user, need to update later with SSO
        user_id = 'vpillai' 
        self.create_rejected_options(user_id)
        options=list(self.rejected_options.keys())
        selected_rejected_option = st.selectbox(label='Pick a Rejected Submission to be Resubmitted:', options=options)
        col1, col2 = st.columns([1,1], gap='small')

        if options:
            with col1:
                get_submission_button = st.button(label='**Pull Data for Resubmission**')
            with col2:
                reset_button = st.button(label='**:red[Reset]**', key='Resubmit')
 
        if 'get_sub_rej_key' not in st.session_state:
            st.session_state['get_sub_rej_key'] = False
    
        if options and reset_button:
            st.session_state['get_sub_rej_key'] = False

        if options and get_submission_button:
            st.session_state['get_sub_rej_key'] = True

        if options and st.session_state['get_sub_rej_key']:   
            self.rs_model.set_Submission_to_Resubmit(self.rejected_options[selected_rejected_option])

            if 'RoT' in self.rs_model.submission_resubmit.form.form_name:
            
                if 'RoT_RS_Button' not in st.session_state:
                    st.session_state['RoT_RS_Button'] = False

                if 'RoT_DB_RS_Submission_Disable' not in st.session_state:
                    st.session_state['RoT_DB_RS_Submission_Disable'] = True
            
                def rerun():
                    st.session_state['RoT_RS_Button'] = False
                    st.session_state['RoT_DB_RS_Submission_Disable'] = True
            
                with col1:
                    st.write('**_Product Information_**')
                    product_name_input = st.text_input(label=self.rs_model.submission_resubmit.form.fields['Product_Name']['Field_Question'], \
                                                    value=self.rs_model.submission_resubmit.field_values_dict['Product_Name'], key='product_name_rs_rot', on_change=rerun)
                    skew_name_input = st.text_input(label=self.rs_model.submission_resubmit.form.fields['Skew_Name']['Field_Question'], 
                                                        value=self.rs_model.submission_resubmit.field_values_dict['Skew_Name'], key='skew_name_rs_rot', on_change=rerun)

                    package_type_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Package_Type']['Field_Question'], \
                                                    options=self.rs_model.submission_resubmit.form.fields['Package_Type']['Field_Selection'], \
                                                    index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Package_Type']['Field_Selection'], \
                                                    self.rs_model.submission_resubmit.field_values_dict['Package_Type']), key='package_type_rs_rot', on_change=rerun)
                    
                    package_type_estim_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Package_Type_Estimation']['Field_Question'], \
                                                options=self.rs_model.submission_resubmit.form.fields['Package_Type_Estimation']['Field_Selection'], \
                                                index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Package_Type_Estimation']['Field_Selection'], \
                                                self.rs_model.submission_resubmit.field_values_dict['Package_Type_Estimation']), key='package_type_estimation_rs_rot', on_change=rerun)
                    
                    num_main = st.number_input(label=self.rs_model.submission_resubmit.form.fields['Number_of_Main_Die']['Field_Question'], \
                                                min_value=self.rs_model.submission_resubmit.form.fields['Number_of_Main_Die']['Min_Value'], \
                                                max_value=self.rs_model.submission_resubmit.form.fields['Number_of_Main_Die']['Max_Value'], \
                                                value=int(self.rs_model.submission_resubmit.field_values_dict['Number_of_Main_Die']), key='num_main_rs_rot', on_change=rerun)
                    
                    exist_emib_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Exist_EMIB']['Field_Question'], \
                                                    options=self.rs_model.submission_resubmit.form.fields['Exist_EMIB']['Field_Selection'], \
                                                    index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Exist_EMIB']['Field_Selection'], \
                                                    self.rs_model.submission_resubmit.field_values_dict['Exist_EMIB']), key='exist_emib_rs_rot', on_change=rerun)
                    
                    exist_point_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Exist_POINT']['Field_Question'], \
                                                    options=self.rs_model.submission_resubmit.form.fields['Exist_POINT']['Field_Selection'], \
                                                    index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Exist_POINT']['Field_Selection'], \
                                                    self.rs_model.submission_resubmit.field_values_dict['Exist_POINT']), key='exist_point_rs_rot', on_change=rerun)
                with col2:
                    st.write('**_WLA Information_**') 
                    wla_architect_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['WLA_Architecture']['Field_Question'], \
                                                    options=self.rs_model.submission_resubmit.form.fields['WLA_Architecture']['Field_Selection'], \
                                                    index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['WLA_Architecture']['Field_Selection'], \
                                                    self.rs_model.submission_resubmit.field_values_dict['WLA_Architecture']), key='wla_architect_rs_rot', on_change=rerun)
                    
                    chiplet_num = st.number_input(label=self.rs_model.submission_resubmit.form.fields['Number_of_Chiplet_Base_Die']['Field_Question'], \
                                                min_value=self.rs_model.submission_resubmit.form.fields['Number_of_Chiplet_Base_Die']['Min_Value'], \
                                                max_value=self.rs_model.submission_resubmit.form.fields['Number_of_Chiplet_Base_Die']['Max_Value'], \
                                                value=int(self.rs_model.submission_resubmit.field_values_dict['Number_of_Chiplet_Base_Die']), key='chiplet_num_rs_rot', on_change=rerun)
                    
                    dow_architect_input = 'No WLA'
                    odi_chiplet_size_input = 'No WLA'
                    hbi_architect_input = 'No WLA'
                    signal_area_hbi = 0
                    if wla_architect_input == 'Foveros DoW':
                        dow_architect_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['DoW_Architecture']['Field_Question'], \
                                                        options=self.rs_model.submission_resubmit.form.fields['DoW_Architecture']['Field_Selection'], \
                                                        index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['DoW_Architecture']['Field_Selection'], \
                                                        self.rs_model.submission_resubmit.field_values_dict['DoW_Architecture']), key='dow_architect_rs_rot', on_change=rerun)
                    elif wla_architect_input == 'ODI':
                        odi_chiplet_size_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['ODI_Chiplet_Size']['Field_Question'], \
                                                        options=self.rs_model.submission_resubmit.form.fields['ODI_Chiplet_Size']['Field_Selection'], \
                                                        index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['ODI_Chiplet_Size']['Field_Selection'], \
                                                        self.rs_model.submission_resubmit.field_values_dict['ODI_Chiplet_Size']), key='odi_chiplet_size_rs_rot', on_change=rerun)
                    elif wla_architect_input == 'HBI':
                        hbi_architect_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['HBI_Architecture']['Field_Question'], \
                                                        options=self.rs_model.submission_resubmit.form.fields['HBI_Architecture']['Field_Selection'], \
                                                        index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['HBI_Architecture']['Field_Selection'], \
                                                        self.rs_model.submission_resubmit.field_values_dict['HBI_Architecture']), key='hbi_architect_rs_rot', on_change=rerun)
                        
                        signal_area_hbi = st.number_input(label=self.rs_model.submission_resubmit.form.fields['Signal_Area']['Field_Question'], \
                                                min_value=self.rs_model.submission_resubmit.form.fields['Signal_Area']['Min_Value'], \
                                                max_value=self.rs_model.submission_resubmit.form.fields['Signal_Area']['Max_Value'], \
                                                value=int(self.rs_model.submission_resubmit.field_values_dict['Signal_Area']), key='signal_area_rs_rot', on_change=rerun)

                    st.write('**_Other Information_**')
                    die_architect_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Die_Architecture_Summary']['Field_Question'], \
                                                options=self.rs_model.submission_resubmit.form.fields['Die_Architecture_Summary']['Field_Selection'], \
                                                index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Die_Architecture_Summary']['Field_Selection'], \
                                                self.rs_model.submission_resubmit.field_values_dict['Die_Architecture_Summary']), key='die_architect_rs_rot', on_change=rerun)
                    
                    type_num_satellite = st.number_input(label=self.rs_model.submission_resubmit.form.fields['Number_of_Satellite_Die']['Field_Question'], \
                                                        min_value=self.rs_model.submission_resubmit.form.fields['Number_of_Satellite_Die']['Min_Value'], \
                                                        max_value=self.rs_model.submission_resubmit.form.fields['Number_of_Satellite_Die']['Max_Value'], \
                                                        value=int(self.rs_model.submission_resubmit.field_values_dict['Number_of_Satellite_Die']), key='type_num_satellite_rs_rot', on_change=rerun)
                    
                    exist_hbm = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Exist_HBM']['Field_Question'], \
                                            options=self.rs_model.submission_resubmit.form.fields['Exist_HBM']['Field_Selection'], \
                                            index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Exist_HBM']['Field_Selection'], \
                                            self.rs_model.submission_resubmit.field_values_dict['Exist_HBM']), key='exist_hbm_rs_rot', on_change=rerun)
                    
                    lifetime_volume = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Lifetime_Volume']['Field_Question'], \
                                            options=self.rs_model.submission_resubmit.form.fields['Lifetime_Volume']['Field_Selection'],  \
                                            index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Lifetime_Volume']['Field_Selection'], \
                                            self.rs_model.submission_resubmit.field_values_dict['Lifetime_Volume']), key='lifetime_vol_rs_rot', on_change=rerun)

                    architecture_maturity_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Architecture_Maturity']['Field_Question'], \
                                            options=self.rs_model.submission_resubmit.form.fields['Architecture_Maturity']['Field_Selection'],  \
                                            index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Architecture_Maturity']['Field_Selection'], \
                                            self.rs_model.submission_resubmit.field_values_dict['Architecture_Maturity']), key='architecture_mat_rs_rot', on_change=rerun)

                result, lrp_output = self.rs_model.rot_model.lrp_prediction(product_name=product_name_input, skew_name=skew_name_input, chiplet_num=chiplet_num, \
                                                    pkg_type=package_type_estim_input, pkg_class=package_type_input, main_num=num_main, exist_emib=exist_emib_input, \
                                                    point_pkg=exist_point_input, lifetime_vol_input_val=lifetime_volume, \
                                                    wla_architect=wla_architect_input, dow_architect_input_val=dow_architect_input, \
                                                    odi_chiplet_size=odi_chiplet_size_input, hbi_architect=hbi_architect_input, signal_area_hbi=signal_area_hbi,  \
                                                    exist_hbm_input_val=exist_hbm, die_architect_input_val=die_architect_input, type_num_satellite_input_val=type_num_satellite, \
                                                    architecture_maturity_val=architecture_maturity_input)
                
                st.divider()

                run_prediction = st.button('**Run Data Prediction**', key = 'run_prediction_rs_rot')
                if run_prediction:
                    st.session_state['RoT_RS_Button'] = True
                    st.session_state['RoT_DB_RS_Submission_Disable'] = False
                    st.write(f'Product Name: {product_name_input} {skew_name_input}')
                    st.write(f'Package Type: {package_type_input}')
                    st.dataframe(result)

                if st.session_state['RoT_RS_Button']:
                    submit_database = st.button('**Submit to Database?**', key='submit_database_rs_rot', disabled=st.session_state['RoT_DB_RS_Submission_Disable'])
                    if submit_database:
                        with st.spinner('Writing to Database...'):
                            field_values_dict = lrp_output
                            record = self.rs_model.submission_resubmit.update_Submission(status='Pending', field_values_dict=field_values_dict)
                            st.write(record)
                            st.session_state['get_sub_rej_key'] = False
                            st.session_state['RoT_RS_Button'] = False
            else:
                
                if 'ME_RS_Button' not in st.session_state:
                    st.session_state['ME_RS_Button'] = False

                if ('ME_DB_RS_Submission_Disable' not in st.session_state):
                    st.session_state['ME_DB_RS_Submission_Disable'] = True  

                            
                def rerun():
                    st.session_state['ME_RS_Button'] = False
                    st.session_state['ME_DB_RS_Submission_Disable'] = True  

                with col1:
                    st.write("**_Product Information_**")
                    product_type_input = st.text_input(label=self.rs_model.submission_resubmit.form.fields['Product_Name']['Field_Question'],  \
                                                    value=self.rs_model.submission_resubmit.field_values_dict['Product_Name'], key='product_name_rs_me', on_change=rerun)
                    
                    skew_name_input = st.text_input(label=self.rs_model.submission_resubmit.form.fields['Skew_Name']['Field_Question'], \
                                                value=self.rs_model.submission_resubmit.field_values_dict['Skew_Name'], key='skew_name_rs_me', on_change=rerun)

                    package_type_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Package_Type']['Field_Question'], \
                                                    options=self.rs_model.submission_resubmit.form.fields['Package_Type']['Field_Selection'], \
                                                    index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Package_Type']['Field_Selection'], \
                                                    self.rs_model.submission_resubmit.field_values_dict['Package_Type']), key='package_type_rs_me', on_change=rerun)
                with col2:
                    st.write("**_Other Information_**")
                    die_architect_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Die_Architecture']['Field_Question'], \
                                                    options=self.rs_model.submission_resubmit.form.fields['Die_Architecture']['Field_Selection'], \
                                                    index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Die_Architecture']['Field_Selection'], \
                                                    self.rs_model.submission_resubmit.field_values_dict['Die_Architecture']), key='die_arch_rs_me', on_change=rerun)
                    
                    if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
                        wla_arch_maturity_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['WLA_Architecture_Maturity']['Field_Question'], \
                                                            options=self.rs_model.submission_resubmit.form.fields['WLA_Architecture_Maturity']['Field_Selection'], \
                                                            index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['WLA_Architecture_Maturity']['Field_Selection'], \
                                                            self.rs_model.submission_resubmit.field_values_dict['WLA_Architecture_Maturity']), key='wla_maturity_rs_me', on_change=rerun)

                    pkg_assemb_maturity_input = st.selectbox(label=self.rs_model.submission_resubmit.form.fields['Pkg_Assembly_Architecture_Maturity']['Field_Question'], \
                                                            options=self.rs_model.submission_resubmit.form.fields['Pkg_Assembly_Architecture_Maturity']['Field_Selection'], \
                                                            index=self.get_index_selection(self.rs_model.submission_resubmit.form.fields['Pkg_Assembly_Architecture_Maturity']['Field_Selection'], \
                                                            self.rs_model.submission_resubmit.field_values_dict['Pkg_Assembly_Architecture_Maturity']), key='pkg_assemb_maturity_rs_me', on_change=rerun)
                
                if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
                    with col2:
                        st.write('**_PRQ WLA Information_**')
                        prq_wla_rtd_input = st.number_input(label='PRQ WLA RtD', min_value=0.0, max_value=100.0, \
                                                            value=self.get_PRQ_value('WLA RtD;PRQ'),  \
                                                            step=0.1, format="%.2f", on_change=rerun)
                        prq_wla_test_input = st.number_input(label='PRQ WLA Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=self.get_PRQ_value('WLA Test PIYL;PRQ'),  \
                                                            step=0.1, format="%.2f", on_change=rerun)
                    with col1:
                        st.write('**_PRQ Pkg Information_**')
                        prq_pkg_assemb_rtd_input = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                            value=self.get_PRQ_value('Pkg Assemb RtD;PRQ'),  \
                                                            step=0.1, format="%.2f", on_change=rerun)
                        prq_pkg_test_piyl_input = st.number_input(label='PRQ Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=self.get_PRQ_value('Pkg Assemb Test PIYL;PRQ'),  \
                                                            step=0.1, format="%.2f", on_change=rerun)
                        prq_pkg_assemb_finish_input = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                            value=self.get_PRQ_value('Pkg Assemb Finish;PRQ'),  \
                                                            step=0.1, format="%.2f", on_change=rerun)
                else:
                    with col1: 
                        st.write('**_PRQ Pkg Information_**')
                        prq_pkg_assemb_rtd_input = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                            value=self.get_PRQ_value('Pkg Assemb RtD;PRQ'),  \
                                                            step=0.1, format="%.2f", on_change=rerun)
                        prq_pkg_test_piyl_input = st.number_input(label='PRQ Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=self.get_PRQ_value('Pkg Assemb Test PIYL;PRQ'),  \
                                                            step=0.1, format="%.2f", on_change=rerun)
                        prq_pkg_assemb_finish_input = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                            value=self.get_PRQ_value('Pkg Assemb Finish;PRQ'),  \
                                                            step=0.1, format="%.2f", on_change=rerun)

                record = ''         

                if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
                    result, lrp_output = self.rs_model.me_model.lrp_prediction(product_name=product_type_input, skew_name=skew_name_input, pkg_class=package_type_input, \
                                        Die_Architecture_Info_val=die_architect_input, WLA_Maturity=wla_arch_maturity_input, \
                                        Pkg_Assemb_Maturity=pkg_assemb_maturity_input, PRQ_WLA_RtD=prq_wla_rtd_input, \
                                        PRQ_WLA_Test_PIYL=prq_wla_test_input, PRQ_Pkg_Assemb_RtD=prq_pkg_assemb_rtd_input, \
                                        PRQ_Pkg_Test_PIYL=prq_pkg_test_piyl_input, PRQ_Pkg_Assemb_Finish=prq_pkg_assemb_finish_input)
                else:
                    result, lrp_output = self.rs_model.me_model.lrp_prediction(product_name=product_type_input, skew_name=skew_name_input, pkg_class=package_type_input, \
                                    Die_Architecture_Info_val=die_architect_input, WLA_Maturity=None, \
                                    Pkg_Assemb_Maturity=pkg_assemb_maturity_input, PRQ_WLA_RtD=None, \
                                    PRQ_WLA_Test_PIYL=None, PRQ_Pkg_Assemb_RtD=prq_pkg_assemb_rtd_input, \
                                    PRQ_Pkg_Test_PIYL=prq_pkg_test_piyl_input, PRQ_Pkg_Assemb_Finish=prq_pkg_assemb_finish_input)

                st.divider()

                run_prediction =  st.button('**Run Data Prediction**', key='run_prediction_rs_me')
                if run_prediction:
                    st.session_state['ME_RS_Button'] = True
                    st.session_state['ME_DB_RS_Submission_Disable'] = False
                    st.write(f'Product Name: {product_type_input} {skew_name_input}')
                    st.write(f'Package Type: {package_type_input}')
                    st.dataframe(result)
                
                if st.session_state['ME_RS_Button']:
                    submit_database = st.button('**Submit to Database?**', key='submit_database_rs_me', \
                                disabled=st.session_state['ME_DB_RS_Submission_Disable'])
                    
                    if submit_database:
                        with st.spinner('Writing to Database...'):
                            field_values_dict = lrp_output
                            record = self.rs_model.submission_resubmit.update_Submission(status='Pending', field_values_dict=field_values_dict)              
                            st.write(record)
                            st.session_state['get_sub_rej_key'] = False
                            st.session_state['ME_RS_Button'] = False

