
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
            st.write(f"Group: {group}")
            group_data = grouped_data.get_group(group)
            st.dataframe(group_data)

    def view(self):
        st.write("LRP View")
        client, server, graphics, asic, psg = st.tabs(["Client", "Server", "Graphics", "ASIC", "PSG"])

        with client:
            st.write("Client")
            df_client = self.df[self.df['Package Type'] == 'Client']
            self.df_group_by(df_client, 'Product', 'Skew')
        
        with server:
            st.write("Server")
            df_server = self.df[self.df['Package Type'] == 'Server']
            self.df_group_by(df_server, 'Product', 'Skew')

        with graphics:
            st.write("Graphics")
            df_graphics = self.df[self.df['Package Type'] == 'Graphics']
            self.df_group_by(df_graphics, 'Product', 'Skew')

        with asic:
            st.write("ASIC")
            df_asic = self.df[self.df['Package Type'] == 'ASIC']
            self.df_group_by(df_asic, 'Product', 'Skew')

        with psg:
            st.write("PSG")
            df_psg = self.df[self.df['Package Type'] == 'PSG']
            self.df_group_by(df_psg, 'Product', 'Skew')

class PA_View():
    def __init__(self):
        pass
    
    def view(self):
        st.write("Product Architecture")


class Data_Entry_View():
    def __init__(self, de_model):
        self.de_model = de_model

    def rot_view(self):
        st.write('LRP Data Update: RoT')
        st.write('General Information')
        self.de_model.submission.create_Form('RoT')
        
        product_name_input = st.text_input(label=self.de_model.submission.form.fields['Product_Name']['Field_Question'], value='', key='product_name_rot')
        optional_skew_checkbox_input = st.checkbox(label=self.de_model.submission.form.fields['Skew_Name']['Field_Question'], key='optional_skew_rot')

        if optional_skew_checkbox_input:
            skew_name_input = st.text_input(label='Skew Name', value='', key='skew_name_rot')
        else:
            skew_name_input = ''

        package_type_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type']['Field_Question'], \
                                          options=self.de_model.submission.form.fields['Package_Type']['Field_Selection'], key='package_type_rot')
        
        package_type_estim_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type_Estimation']['Field_Question'], \
                                          options=self.de_model.submission.form.fields['Package_Type_Estimation']['Field_Selection'], key='package_type_estimation_rot')
        
        num_main = st.number_input(label=self.de_model.submission.form.fields['Number_of_Main_Die']['Field_Question'], \
                                    min_value=self.de_model.submission.form.fields['Number_of_Main_Die']['Min_Value'], \
                                    max_value=self.de_model.submission.form.fields['Number_of_Main_Die']['Max_Value'], \
                                    value=self.de_model.submission.form.fields['Number_of_Main_Die']['Default_Value'], key='num_main_rot')
        
        exist_emib_input = st.selectbox(label=self.de_model.submission.form.fields['Exist_EMIB']['Field_Question'], \
                                        options=self.de_model.submission.form.fields['Exist_EMIB']['Field_Selection'], key='exist_emib_rot')
        
        exist_point_input = st.selectbox(label=self.de_model.submission.form.fields['Exist_POINT']['Field_Question'], \
                                        options=self.de_model.submission.form.fields['Exist_POINT']['Field_Selection'], key='exist_point_rot')

        st.write('WLA Information') 
        wla_architect_input = st.selectbox(label=self.de_model.submission.form.fields['WLA_Architecture']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['WLA_Architecture']['Field_Selection'], key='wla_architect_rot')
        
        chiplet_num = st.number_input(label=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Field_Question'], \
                                    min_value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Min_Value'], \
                                    max_value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Max_Value'], \
                                    value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Default_Value'], key='chiplet_num_rot')
        
        dow_architect_input = 'No WLA'
        odi_chiplet_size_input = 'No WLA'
        hbi_architect_input = 'No WLA'
        signal_area_hbi = 0
        if wla_architect_input == 'Foveros DoW':
            dow_architect_input = st.selectbox(label=self.de_model.submission.form.fields['DoW_Architecture']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['DoW_Architecture']['Field_Selection'], key='dow_architect_rot')
        elif wla_architect_input == 'ODI':
            odi_chiplet_size_input = st.selectbox(label=self.de_model.submission.form.fields['ODI_Chiplet_Size']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['ODI_Chiplet_Size']['Field_Selection'], key='odi_chiplet_size_rot')
        elif wla_architect_input == 'HBI':
            hbi_architect_input = st.selectbox(label=self.de_model.submission.form.fields['HBI_Architecture']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['HBI_Architecture']['Field_Selection'], key='hbi_architect_rot')
            
            signal_area_hbi = st.number_input(label=self.de_model.submission.form.fields['Signal_Area']['Field_Question'], \
                                    min_value=self.de_model.submission.form.fields['Signal_Area']['Min_Value'], \
                                    max_value=self.de_model.submission.form.fields['Signal_Area']['Max_Value'], \
                                    value=self.de_model.submission.form.fields['Signal_Area']['Default_Value'], key='signal_area_rot')

        st.write('Other Information')
        die_architect_input = st.selectbox(label=self.de_model.submission.form.fields['Die_Architecture_Summary']['Field_Question'], \
                                         options=self.de_model.submission.form.fields['Die_Architecture_Summary']['Field_Selection'], key='die_architect_rot')
        
        type_num_satellite = st.number_input(label=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Field_Question'], \
                                             min_value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Min_Value'], \
                                             max_value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Max_Value'], \
                                             value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Default_Value'], key='type_num_satellite_rot')
        
        exist_hbm = st.selectbox(label=self.de_model.submission.form.fields['Exist_HBM']['Field_Question'], \
                                  options=self.de_model.submission.form.fields['Exist_HBM']['Field_Selection'], key='exist_hbm_rot')
        
        lifetime_volume = st.selectbox(label=self.de_model.submission.form.fields['Lifetime_Volume']['Field_Question'], \
                                    options=self.de_model.submission.form.fields['Lifetime_Volume']['Field_Selection'], key='lifetime_vol_rot')

        architecture_maturity_input = st.selectbox(label=self.de_model.submission.form.fields['Architecture_Maturity']['Field_Question'], \
                                    options=self.de_model.submission.form.fields['Architecture_Maturity']['Field_Selection'], key='architecture_mat_rot')
            

        if 'RoT_Button' not in st.session_state:
            st.session_state['RoT_Button'] = False

        if 'DB_Submission' not in st.session_state:
            st.session_state['DB_Submission'] = False

        result, lrp_output = self.de_model.rot_model.lrp_prediction(product_name=product_name_input, skew_name=skew_name_input, chiplet_num=chiplet_num, \
                                            pkg_type=package_type_estim_input, pkg_class=package_type_input, main_num=num_main, exist_emib=exist_emib_input, \
                                            point_pkg=exist_point_input, lifetime_vol_input_val=lifetime_volume, \
                                            wla_architect=wla_architect_input, dow_architect_input_val=dow_architect_input, \
                                            odi_chiplet_size=odi_chiplet_size_input, hbi_architect=hbi_architect_input, signal_area_hbi=signal_area_hbi,  \
                                            exist_hbm_input_val=exist_hbm, die_architect_input_val=die_architect_input, type_num_satellite_input_val=type_num_satellite, \
                                            architecture_maturity_val=architecture_maturity_input)
        
        if st.button('Run Data Prediction'):
            st.session_state['RoT_Button'] = not st.session_state['RoT_Button']
            st.write(f'Product Name: {product_name_input} {skew_name_input}')
            st.write(f'Package Type: {package_type_input}')
            st.dataframe(result)

        if st.session_state['RoT_Button']:
            if st.button('Submit to Database?'):
                st.session_state['DB_Submission'] = not st.session_state['DB_Submission']        
                user_id='vpillai'
                field_values_dict = lrp_output
                self.de_model.submission.set_Submission_Attributes(user_id=user_id, field_values_dict=field_values_dict)
                record = self.de_model.submission.publish_Submission()
                st.write(record)

    def me_view(self):
        st.write('LRP Data Update: Manual Entry')
        st.write('Product Information')
        
        self.de_model.submission.create_Form('Manual Entry')
        self.de_model.submission.form.set_Fields()

        product_type_input = st.text_input(label=self.de_model.submission.form.fields['Product_Name']['Field_Question'], value='', key='product_name_me')
        
        optional_skew_checkbox_input = st.checkbox(label=self.de_model.submission.form.fields['Skew_Name']['Field_Question'], key='optional_skew_me')

        if optional_skew_checkbox_input:
            skew_name_input = st.text_input(label='Skew Name', value='', key='skew_name_me')
        else:
            skew_name_input = ''

        package_type_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type']['Field_Question'], \
                                        options=self.de_model.submission.form.fields['Package_Type']['Field_Selection'], key='package_type_me')
        
        die_architect_input = st.selectbox(label=self.de_model.submission.form.fields['Die_Architecture']['Field_Question'], \
                                        options=self.de_model.submission.form.fields['Die_Architecture']['Field_Selection'], key='die_arch_me')
        
        if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
            wla_arch_maturity_input = st.selectbox(label=self.de_model.submission.form.fields['WLA_Architecture_Maturity']['Field_Question'], \
                                                options=self.de_model.submission.form.fields['WLA_Architecture_Maturity']['Field_Selection'], key='wla_maturity_me')

        pkg_assemb_maturity_input = st.selectbox(label=self.de_model.submission.form.fields['Pkg_Assembly_Architecture_Maturity']['Field_Question'], \
                                                options=self.de_model.submission.form.fields['Pkg_Assembly_Architecture_Maturity']['Field_Selection'], key='pkg_assemb_maturity_me')
        
        if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
            prq_wla_rtd_input = st.number_input(label='PRQ WLA RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f")
            prq_wla_test_input = st.number_input(label='PRQ WLA Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f")
            prq_pkg_assemb_rtd_input = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f")
            prq_pkg_test_piyl_input = st.number_input(label='PRQ Pkg Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f")
            prq_pkg_assemb_finish_input = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f")
        else:
            prq_pkg_assemb_rtd_input = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f")
            prq_pkg_test_piyl_input = st.number_input(label='PRQ Pkg Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f")
            prq_pkg_assemb_finish_input = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, value=99.0, step=0.1, format="%.2f")

        if 'ME_Button' not in st.session_state:
            st.session_state['ME_Button'] = False

        if 'ME_DB_Submission' not in st.session_state:
            st.session_state['ME_DB_Submission'] = False
        
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

        if st.button('Run Data Prediction', key='run_prediction_me'):
            st.session_state['ME_Button'] = not st.session_state['ME_Button']
            st.write(f'Product Name: {product_type_input} {skew_name_input}')
            st.write(f'Package Type: {package_type_input}')
            st.dataframe(result)
        
        if st.session_state['ME_Button']:
            if st.button('Submit to Database?', key='submit_database_me'):
                st.session_state['ME_DB_Submission'] = not st.session_state['ME_DB_Submission']        
                user_id='vpillai'
                field_values_dict = lrp_output
                self.de_model.submission.set_Submission_Attributes(user_id=user_id, field_values_dict=field_values_dict)
                record = self.de_model.submission.publish_Submission()
                st.write(record)

    def view(self):
        st.write("Data Entry")
        rot, man_ent = st.tabs(["RoT", "Manual Entry"])

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
        if 'get_sub_key' not in st.session_state:
            st.session_state['get_sub_key'] = False
        
        st.write("Data Review")
        self.create_pending_options()
        selected_pending_option = st.selectbox(label='Pick a Pending Submission to be Reviewed:', options=list(self.pending_options.keys()))
        get_submission_button = st.button(label='Pull Submission Data')
        if get_submission_button:
            st.session_state['get_sub_key'] = not st.session_state['get_sub_key']
            self.dr_model.set_Submission_to_Review(self.pending_options[selected_pending_option])
            table = pd.Series(self.dr_model.submission_review.field_values_dict)
            st.table(table)
        




    