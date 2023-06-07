
import streamlit as st
import pandas as pd
import numpy as np
import datetime

class Home_View:
    def __init__(self):
        pass

    def view(self):
        st.write("User info:", st.session_state.user_info)


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
            
            create_pqs_input = st.selectbox(label=self.de_model.submission.form.fields['Create_PQS']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Create_PQS']['Field_Selection'], key='create_pqs_rot', on_change=rerun)

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
                                            architecture_maturity_val=architecture_maturity_input, create_pqs_input=create_pqs_input)

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

            product_name_input = st.text_input(label=self.de_model.submission.form.fields['Product_Name']['Field_Question'], value='', key='product_name_me', on_change=rerun)
            
            optional_skew_checkbox_input = st.checkbox(label=self.de_model.submission.form.fields['Skew_Name']['Field_Question'], key='optional_skew_me', on_change=rerun)

            if optional_skew_checkbox_input:
                skew_name_input = st.text_input(label='Skew Name', value='', key='skew_name_me', on_change=rerun)
            else:
                skew_name_input = ''

            package_type_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Package_Type']['Field_Selection'], key='package_type_me', on_change=rerun)

            create_pqs_input = st.selectbox(label=self.de_model.submission.form.fields['Create_PQS']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Create_PQS']['Field_Selection'], key='create_pqs_me', on_change=rerun)
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
            result, lrp_output = self.de_model.me_model.lrp_prediction(product_name=product_name_input, skew_name=skew_name_input, pkg_class=package_type_input, \
                                Die_Architecture_Info_val=die_architect_input, WLA_Maturity=wla_arch_maturity_input, \
                                Pkg_Assemb_Maturity=pkg_assemb_maturity_input, PRQ_WLA_RtD=prq_wla_rtd_input, \
                                PRQ_WLA_Test_PIYL=prq_wla_test_input, PRQ_Pkg_Assemb_RtD=prq_pkg_assemb_rtd_input, \
                                PRQ_Pkg_Test_PIYL=prq_pkg_test_piyl_input, PRQ_Pkg_Assemb_Finish=prq_pkg_assemb_finish_input, create_pqs_input=create_pqs_input)
        else:
            result, lrp_output = self.de_model.me_model.lrp_prediction(product_name=product_name_input, skew_name=skew_name_input, pkg_class=package_type_input, \
                            Die_Architecture_Info_val=die_architect_input, WLA_Maturity=None, \
                            Pkg_Assemb_Maturity=pkg_assemb_maturity_input, PRQ_WLA_RtD=None, \
                            PRQ_WLA_Test_PIYL=None, PRQ_Pkg_Assemb_RtD=prq_pkg_assemb_rtd_input, \
                            PRQ_Pkg_Test_PIYL=prq_pkg_test_piyl_input, PRQ_Pkg_Assemb_Finish=prq_pkg_assemb_finish_input, create_pqs_input=create_pqs_input)
        
        st.divider()

        if st.button('**Run Data Prediction**', key='run_prediction_me'):
            st.session_state['ME_Button'] = True
            st.write(f'Product Name: {product_name_input} {skew_name_input}')
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

    
    def commit_view(self):
        col1, col2, col3 = st.columns(3)
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
        
        if 'Commit_Button' not in st.session_state:
            st.session_state['Commit_Button'] = False

        def rerun():
            st.session_state['Commit_Button'] = False
        
        with col1:

            st.write('**_Product Information_**')
            self.de_model.submission.create_Form('Commit')
            self.de_model.submission.form.set_Fields()

            product_name_input = st.text_input(label=self.de_model.submission.form.fields['Product_Name']['Field_Question'], value='', key='product_name_commit', on_change=rerun)
            
            optional_skew_checkbox_input = st.checkbox(label=self.de_model.submission.form.fields['Skew_Name']['Field_Question'], key='optional_skew_commit', on_change=rerun)

            if optional_skew_checkbox_input:
                skew_name_input = st.text_input(label='Skew Name', value='', key='skew_name_me', on_change=rerun)
            else:
                skew_name_input = ''

        with col2:
            package_type_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Package_Type']['Field_Selection'], key='package_type_commit', on_change=rerun)
        
            note_input = st.text_input(label=self.de_model.submission.form.fields['Note']['Field_Question'], value='', key='note_commit', on_change=rerun)

        with col3:
            exist_wla_input = st.selectbox(label=self.de_model.submission.form.fields['Exist_WLA']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Exist_WLA']['Field_Selection'], key='exist_wla_commit', on_change=rerun)
            
            create_pqs_input = st.selectbox(label=self.de_model.submission.form.fields['Create_PQS']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['Create_PQS']['Field_Selection'], key='create_pqs_commit', on_change=rerun)
        if create_pqs_input == 'Yes':
            create_pqs_val = 1
        else:
            create_pqs_val = 0

        with col1:
            st.write('**_PIYL Table_**')
            if exist_wla_input:
                po_es0_wla_rtd = st.number_input(label='PO/ES0 WLA RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PO/ES0 WLA RtD_commit')
                po_es0_wla_test_piyl = st.number_input(label='PO/ES0 WLA Test PIYL', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PO/ES0 WLA Test PIYL_commit')
                po_es0_wla_inv_yield = st.number_input(label='PO/ES0 WLA Inventory Yield', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PO/ES0 WLA Inventory Yield_commit')
            po_es0_pkg_assemb_rtd = st.number_input(label='PO/ES0 Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PO/ES0 Pkg Assemb RtD_commit')
            po_es0_pkg_assemb_test_piyl = st.number_input(label='PO/ES0 Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PO/ES0 Pkg Assemb Test PIYL_commit')
            po_es0_pkg_assemb_finish = st.number_input(label='PO/ES0 Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PO/ES0 Pkg Assemb Finish_commit')
            po_es0_pkg_assemb_inv_yield = st.number_input(label='PO/ES0 Pkg Assemb Inventory Yield', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PO/ES0 Pkg Assemb Inventory Yield_commit')
            
            if exist_wla_input:
                qs_wla_rtd = st.number_input(label='QS WLA RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='QS WLA RtD_commit')
                qs_wla_test_piyl = st.number_input(label='QS WLA Test PIYL', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='QS WLA Test PIYL_commit')
                qs_wla_inv_yield = st.number_input(label='QS WLA Inventory Yield', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='QS WLA Inventory Yield_commit')
            qs_pkg_assemb_rtd = st.number_input(label='QS Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='QS Pkg Assemb RtD_commit')
            qs_pkg_assemb_test_piyl = st.number_input(label='QS Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='QS Pkg Assemb Test PIYL_commit')
            qs_pkg_assemb_finish = st.number_input(label='QS Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='QS Pkg Assemb Finish_commit')
            qs_pkg_assemb_inv_yield = st.number_input(label='QS Pkg Assemb Inventory Yield', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='QS Pkg Assemb Inventory Yield_commit')

            if create_pqs_val:
                if exist_wla_input:
                    pqs_wla_rtd = st.number_input(label='PQS WLA RtD', min_value=0.0, max_value=100.0, \
                                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PQS WLA RtD_commit')
                    pqs_wla_test_piyl = st.number_input(label='PQS WLA Test PIYL', min_value=0.0, max_value=100.0, \
                                                        value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PQS WLA Test PIYL_commit')
                    pqs_wla_inv_yield = st.number_input(label='PQS WLA Inventory Yield', min_value=0.0, max_value=100.0, \
                                                        value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PQS WLA Inventory Yield_commit')
                pqs_pkg_assemb_rtd = st.number_input(label='PQS Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PQS Pkg Assemb RtD_commit')
                pqs_pkg_assemb_test_piyl = st.number_input(label='PQS Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PQS Pkg Assemb Test PIYL_commit')
                pqs_pkg_assemb_finish = st.number_input(label='PQS Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PQS Pkg Assemb Finish_commit')
                pqs_pkg_assemb_inv_yield = st.number_input(label='PQS Pkg Assemb Inventory Yield', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PQS Pkg Assemb Inventory Yield_commit')
                
        with col2:
            if exist_wla_input:
                es1_wla_rtd = st.number_input(label='ES1 WLA RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES1 WLA RtD_commit')
                es1_wla_test_piyl = st.number_input(label='ES1 WLA Test PIYL', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES1 WLA Test PIYL_commit')
                es1_wla_inv_yield = st.number_input(label='ES1 WLA Inventory Yield', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES1 WLA Inventory Yield_commit')
            es1_pkg_assemb_rtd = st.number_input(label='ES1 Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES1 Pkg Assemb RtD_commit')
            es1_pkg_assemb_test_piyl = st.number_input(label='ES1 Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES1 Pkg Assemb Test PIYL_commit')
            es1_pkg_assemb_finish = st.number_input(label='ES1 Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES1 Pkg Assemb Finish_commit')
            es1_pkg_assemb_inv_yield = st.number_input(label='ES1 Pkg Assemb Inventory Yield', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES1 Pkg Assemb Inventory Yield_commit')
            
            if exist_wla_input:
                prq_wla_rtd = st.number_input(label='PRQ WLA RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ WLA RtD_commit')
                prq_wla_test_piyl = st.number_input(label='PRQ WLA Test PIYL', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ WLA Test PIYL_commit')
                prq_wla_inv_yield = st.number_input(label='PRQ WLA Inventory Yield', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ WLA Inventory Yield_commit')
            prq_pkg_assemb_rtd = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ Pkg Assemb RtD_commit')
            prq_pkg_assemb_test_piyl = st.number_input(label='PRQ Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ Pkg Assemb Test PIYL_commit')
            prq_pkg_assemb_finish = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ Pkg Assemb Finish_commit')
            prq_pkg_assemb_inv_yield = st.number_input(label='PRQ Pkg Assemb Inventory Yield', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ Pkg Assemb Inventory Yield_commit')
        
        with col3:
            if exist_wla_input:
                es2_wla_rtd = st.number_input(label='ES2 WLA RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES2 WLA RtD_commit')
                es2_wla_test_piyl = st.number_input(label='ES2 WLA Test PIYL', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES2 WLA Test PIYL_commit')
                es2_wla_inv_yield = st.number_input(label='ES2 WLA Inventory Yield', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES2 WLA Inventory Yield_commit')
            es2_pkg_assemb_rtd = st.number_input(label='ES2 Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES2 Pkg Assemb RtD_commit')
            es2_pkg_assemb_test_piyl = st.number_input(label='ES2 Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES2 Pkg Assemb Test PIYL_commit')
            es2_pkg_assemb_finish = st.number_input(label='ES2 Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES2 Pkg Assemb Finish_commit')
            es2_pkg_assemb_inv_yield = st.number_input(label='ES2 Pkg Assemb Inventory Yield', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='ES2 Pkg Assemb Inventory Yield_commit')
            
            if exist_wla_input:
                prq_1q_wla_rtd = st.number_input(label='PRQ+1Q WLA RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ+1Q WLA RtD_commit')
                prq_1q_wla_test_piyl = st.number_input(label='PRQ+1Q WLA Test PIYL', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ+1Q WLA Test PIYL_commit')
                prq_1q_wla_inv_yield = st.number_input(label='PRQ+1Q WLA Inventory Yield', min_value=0.0, max_value=100.0, \
                                                    value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ+1Q WLA Inventory Yield_commit')
            prq_1q_pkg_assemb_rtd = st.number_input(label='PRQ+1Q Pkg Assemb RtD', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ+1Q Pkg Assemb RtD_commit')
            prq_1q_pkg_assemb_test_piyl = st.number_input(label='PRQ+1Q Pkg Assemb Test PIYL', min_value=0.0, max_value=100.0, \
                                                            value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ+1Q Pkg Assemb Test PIYL_commit')
            prq_1q_pkg_assemb_finish = st.number_input(label='PRQ+1Q Pkg Assemb Finish', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ+1Q Pkg Assemb Finish_commit')
            prq_1q_pkg_assemb_inv_yield = st.number_input(label='PRQ+1Q Pkg Assemb Inventory Yield', min_value=0.0, max_value=100.0, \
                                                value=99.0, step=0.1, format="%.2f", on_change=rerun, key='PRQ+1Q Pkg Assemb Inventory Yield_commit')       

        if create_pqs_val:
            result = pd.DataFrame(columns = ['PO/ES0', 'ES1', 'ES2', 'PQS', 'QS', 'PRQ', 'PRQ+1Q'])
            if exist_wla_input:
                result.loc[len(result)] = [po_es0_wla_rtd, es1_wla_rtd, es2_wla_rtd, pqs_wla_rtd, qs_wla_rtd, prq_wla_rtd, prq_1q_wla_rtd]
                result.loc[len(result)] = [po_es0_wla_test_piyl, es1_wla_test_piyl, es2_wla_test_piyl, pqs_wla_test_piyl, qs_wla_test_piyl, prq_wla_test_piyl, prq_1q_wla_test_piyl]
                result.loc[len(result)] = [po_es0_wla_inv_yield, es1_wla_inv_yield, es2_wla_inv_yield, pqs_wla_inv_yield, qs_wla_inv_yield, prq_wla_inv_yield, prq_1q_wla_inv_yield]
                result.loc[len(result)] = [po_es0_pkg_assemb_rtd, es1_pkg_assemb_rtd, es2_pkg_assemb_rtd, pqs_pkg_assemb_rtd, qs_pkg_assemb_rtd, prq_pkg_assemb_rtd, prq_1q_pkg_assemb_rtd]
                result.loc[len(result)] = [po_es0_pkg_assemb_test_piyl, es1_pkg_assemb_test_piyl, es2_pkg_assemb_test_piyl, pqs_pkg_assemb_test_piyl, qs_pkg_assemb_test_piyl, prq_pkg_assemb_test_piyl, prq_1q_pkg_assemb_test_piyl]
                result.loc[len(result)] = [po_es0_pkg_assemb_finish, es1_pkg_assemb_finish, es2_pkg_assemb_finish, pqs_pkg_assemb_finish, qs_pkg_assemb_finish, prq_pkg_assemb_finish, prq_1q_pkg_assemb_finish]
                result.loc[len(result)] = [po_es0_pkg_assemb_inv_yield, es1_pkg_assemb_inv_yield, es2_pkg_assemb_inv_yield, pqs_pkg_assemb_inv_yield, qs_pkg_assemb_inv_yield, prq_pkg_assemb_inv_yield, prq_1q_pkg_assemb_inv_yield]
                result.index = ["WLA RtD", "WLA Test PIYL", "WLA Inventory Yield", "Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]

            else:
                result.loc[len(result)] = [po_es0_pkg_assemb_rtd, es1_pkg_assemb_rtd, es2_pkg_assemb_rtd, pqs_pkg_assemb_rtd, qs_pkg_assemb_rtd, prq_pkg_assemb_rtd, prq_1q_pkg_assemb_rtd]
                result.loc[len(result)] = [po_es0_pkg_assemb_test_piyl, es1_pkg_assemb_test_piyl, es2_pkg_assemb_test_piyl, pqs_pkg_assemb_test_piyl, qs_pkg_assemb_test_piyl, prq_pkg_assemb_test_piyl, prq_1q_pkg_assemb_test_piyl]
                result.loc[len(result)] = [po_es0_pkg_assemb_finish, es1_pkg_assemb_finish, es2_pkg_assemb_finish, pqs_pkg_assemb_finish, qs_pkg_assemb_finish, prq_pkg_assemb_finish, prq_1q_pkg_assemb_finish]
                result.loc[len(result)] = [po_es0_pkg_assemb_inv_yield, es1_pkg_assemb_inv_yield, es2_pkg_assemb_inv_yield, pqs_pkg_assemb_inv_yield, qs_pkg_assemb_inv_yield, prq_pkg_assemb_inv_yield, prq_1q_pkg_assemb_inv_yield]
                result.index = ["Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]
        else:
            result = pd.DataFrame(columns = ['PO/ES0', 'ES1', 'ES2', 'QS', 'PRQ', 'PRQ+1Q'])
            if exist_wla_input:
                result.loc[len(result)] = [po_es0_wla_rtd, es1_wla_rtd, es2_wla_rtd, qs_wla_rtd, prq_wla_rtd, prq_1q_wla_rtd]
                result.loc[len(result)] = [po_es0_wla_test_piyl, es1_wla_test_piyl, es2_wla_test_piyl, qs_wla_test_piyl, prq_wla_test_piyl, prq_1q_wla_test_piyl]
                result.loc[len(result)] = [po_es0_wla_inv_yield, es1_wla_inv_yield, es2_wla_inv_yield, qs_wla_inv_yield, prq_wla_inv_yield, prq_1q_wla_inv_yield]
                result.loc[len(result)] = [po_es0_pkg_assemb_rtd, es1_pkg_assemb_rtd, es2_pkg_assemb_rtd, qs_pkg_assemb_rtd, prq_pkg_assemb_rtd, prq_1q_pkg_assemb_rtd]
                result.loc[len(result)] = [po_es0_pkg_assemb_test_piyl, es1_pkg_assemb_test_piyl, es2_pkg_assemb_test_piyl, qs_pkg_assemb_test_piyl, prq_pkg_assemb_test_piyl, prq_1q_pkg_assemb_test_piyl]
                result.loc[len(result)] = [po_es0_pkg_assemb_finish, es1_pkg_assemb_finish, es2_pkg_assemb_finish, qs_pkg_assemb_finish, prq_pkg_assemb_finish, prq_1q_pkg_assemb_finish]
                result.loc[len(result)] = [po_es0_pkg_assemb_inv_yield, es1_pkg_assemb_inv_yield, es2_pkg_assemb_inv_yield, qs_pkg_assemb_inv_yield, prq_pkg_assemb_inv_yield, prq_1q_pkg_assemb_inv_yield]
                result.index = ["WLA RtD", "WLA Test PIYL", "WLA Inventory Yield", "Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]

            else:
                result.loc[len(result)] = [po_es0_pkg_assemb_rtd, es1_pkg_assemb_rtd, es2_pkg_assemb_rtd, qs_pkg_assemb_rtd, prq_pkg_assemb_rtd, prq_1q_pkg_assemb_rtd]
                result.loc[len(result)] = [po_es0_pkg_assemb_test_piyl, es1_pkg_assemb_test_piyl, es2_pkg_assemb_test_piyl, qs_pkg_assemb_test_piyl, prq_pkg_assemb_test_piyl, prq_1q_pkg_assemb_test_piyl]
                result.loc[len(result)] = [po_es0_pkg_assemb_finish, es1_pkg_assemb_finish, es2_pkg_assemb_finish, qs_pkg_assemb_finish, prq_pkg_assemb_finish, prq_1q_pkg_assemb_finish]
                result.loc[len(result)] = [po_es0_pkg_assemb_inv_yield, es1_pkg_assemb_inv_yield, es2_pkg_assemb_inv_yield, qs_pkg_assemb_inv_yield, prq_pkg_assemb_inv_yield, prq_1q_pkg_assemb_inv_yield]
                result.index = ["Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]           
        
        st.divider()
        
        lrp_result, lrp_output = self.de_model.commit_model.create_LRP(product_name=product_name_input, skew_name=skew_name_input, \
                                                                package_type=package_type_input, note=note_input, create_pqs=create_pqs_input, \
                                                               result=result, exist_wla=exist_wla_input)

        if st.button('**Run Data Prediction**', key='run_prediction_commit'):
            st.session_state['Commit_Button'] = True
            st.write(f'Product Name: {product_name_input} {skew_name_input}')
            st.write(f'Package Type: {package_type_input}')
            st.dataframe(lrp_result)
        
        if st.session_state['Commit_Button']:
            if st.button('**Submit to Database?**', key='submit_database_me'):
                with st.spinner('Writing to Database...'):
                    user_id='vpillai'
                    field_values_dict = lrp_output
                    self.de_model.submission.set_Submission_Attributes(user_id=user_id, field_values_dict=field_values_dict)
                    record = self.de_model.submission.publish_Submission()
                    st.write(record)
                st.session_state['Commit_Button'] = False


    def view(self):
        if ('SUBMITTER' not in st.session_state.user_info["roles"]) and ('APPROVER' not in st.session_state.user_info["roles"]):
            st.title('**:red[Authorization Unsuccessful]**')
            st.write(':pushpin: :red[For access, apply to the AGS role: **_ATTD Assembly Yield Projection LRP - Submitter on AZAD-CORP_**.]')
        else:
            st.title("Data Entry")
            rot, man_ent, commit = st.tabs(["**:blue[RoT]**", "**:blue[Manual Entry]**",  "**:blue[Commit]**"])

            with rot:
                self.rot_view()
        
            with man_ent:
                self.me_view()

            with commit:
                self.commit_view()

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

    def breakout_tables(self):
        
        if 'RoT' in self.dr_model.submission_review.form.form_name:
            product_keys = ['Product_Name', 'Skew_Name', 'Package_Type', 'Package_Type_Estimation']
            general_keys = ['Number_of_Main_Die', 'Exist_EMIB', 'Exist_POINT']
            wla_keys = ['WLA_Architecture', 'Number_of_Chiplet_Base_Die', 'DoW_Architecture', \
                        'ODI_Chiplet_Size', 'HBI_Architecture', 'Signal_Area']
            other_keys = ['Create_PQS','Die_Architecture_Summary', 'Number_of_Satellite_Die', 'Exist_HBM', \
                          'Lifetime_Volume', 'Architecture_Maturity']
            product_series = pd.Series(data=[self.dr_model.submission_review.field_values_dict[key] for key in product_keys], \
                                       index=product_keys, name='Value')
            general_series =  pd.Series(data=[self.dr_model.submission_review.field_values_dict[key] for key in general_keys], \
                                        index=general_keys, name='Value')
            wla_series =  pd.Series(data=[self.dr_model.submission_review.field_values_dict[key] for key in wla_keys], \
                                        index=wla_keys, name='Value')
            other_series = pd.Series(data=[self.dr_model.submission_review.field_values_dict[key] for key in other_keys], \
                                        index=other_keys, name='Value')
            if self.dr_model.submission_review.field_values_dict['WLA_Architecture'] == 'No WLA':
                is_wla = 0
            else:
                is_wla = 1
            output = {'Product Information': product_series, 'General Information': general_series, 'Other Information': other_series, \
                    'WLA Information': wla_series}
        elif 'Manual' in self.dr_model.submission_review.form.form_name:
            product_keys = ['Product_Name', 'Skew_Name', 'Package_Type']
            other_keys = ['Create_PQS','Die_Architecture', 'WLA_Architecture_Maturity', 'Pkg_Assembly_Architecture_Maturity']
            product_series = pd.Series(data=[self.dr_model.submission_review.field_values_dict[key] for key in product_keys], \
                                       index=product_keys, name='Value')
            other_series = pd.Series(data=[self.dr_model.submission_review.field_values_dict[key] for key in other_keys], \
                                        index=other_keys, name='Value')
            if (self.dr_model.submission_review.field_values_dict['Die_Architecture'] == 'EMIB') or \
                (self.dr_model.submission_review.field_values_dict['Die_Architecture'] == 'Legacy Client'):
                is_wla = 0
            else:
                is_wla = 1
            output = {'Product Information': product_series, 'Other Information': other_series}
        
        elif 'Commit' in self.dr_model.submission_review.form.form_name:
            product_keys = ['Product_Name', 'Skew_Name', 'Package_Type']
            product_series = pd.Series(data=[self.dr_model.submission_review.field_values_dict[key] for key in product_keys], \
                                       index=product_keys, name='Value')
            other_keys = ['Note', 'Exist_WLA', 'Create_PQS']
            other_series = pd.Series(data=[self.dr_model.submission_review.field_values_dict[key] for key in other_keys], \
                            index=other_keys, name='Value')
            if (self.dr_model.submission_review.field_values_dict['Exist_WLA'] == 'No'):
                is_wla = 0
            else:
                is_wla = 1
            
            output = {'Product Information': product_series, 'Other Information': other_series}

      
        if is_wla:
            if self.dr_model.submission_review.field_values_dict['Create_PQS'] == 'Yes':
                prq_columns = ['PO/ES0', 'ES1', 'ES2', 'PQS', 'QS', 'PRQ', 'PRQ+1Q']
            else:
                prq_columns = ['PO/ES0', 'ES1', 'ES2', 'QS', 'PRQ', 'PRQ+1Q']

            prq_index = ["WLA RtD", "WLA Test PIYL", "WLA Inventory Yield", "Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]
            prq_table = pd.DataFrame(columns = prq_columns, index = prq_index)
            for prq_ind in prq_index:
                row = []
                for prq_col in prq_columns:
                    str_key = prq_ind + ';' + prq_col
                    row.append(self.dr_model.submission_review.field_values_dict[str_key])
                prq_table.loc[prq_ind] = row
        else:
            if self.dr_model.submission_review.field_values_dict['Create_PQS'] == 'Yes':
                prq_columns = ['PO/ES0', 'ES1', 'ES2', 'PQS', 'QS', 'PRQ', 'PRQ+1Q']
            else:
                prq_columns = ['PO/ES0', 'ES1', 'ES2', 'QS', 'PRQ', 'PRQ+1Q']
            prq_index = ["Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]
            prq_table = pd.DataFrame(columns = prq_columns, index = prq_index)
            for prq_ind in prq_index:
                row = []
                for prq_col in prq_columns:
                    str_key = prq_ind + ';' + prq_col
                    row.append(self.dr_model.submission_review.field_values_dict[str_key])
                prq_table.loc[prq_ind] = row
        
        output['PRQ Table'] = prq_table

        return output

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
            tables = self.breakout_tables()
            table_i = 0
            for key, value in tables.items():
                key_title = '*_' + key + '_*'
                if table_i % 2:
                    with col2:
                        st.write(key_title)
                        st.dataframe(value)
                else:
                    with col1:
                        st.write(key_title)
                        st.dataframe(value)    
                table_i+=1

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

            elif 'Manual' in self.rs_model.submission_resubmit.form.form_name:
                
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

