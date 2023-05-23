
import streamlit as st
import pandas as pd
import numpy as np
import model

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
        # st.write('LRP Data Update: RoT')
        # st.write('General Information')
        # package_type_input = st.selectbox(label='Package Type', options=['Client','Server','Beast (>>SPR-XCC)'])
        # num_main = st.number_input(label='Number of Main Die', min_value=0, max_value=50, value=2)
        # exist_emib_input = st.selectbox(label='Does main die have EMIB?', options=['Yes','No'])
        # exist_point_input = st.selectbox(label='Is this a POINT package?', options=['Yes','No'])

        # st.write('WLA Information') 
        # wla_architect_input = st.selectbox(label='WLA Architecture', options=['No WLA','Foveros DoW','ODI','HBI'])
        # chiplet_num = st.number_input(label='Number of chiplet/base die', min_value=0, max_value=50, value=2)
        # dow_architect_input = 'No WLA'
        # odi_chiplet_size_input = 'No WLA'
        # hbi_architect_input = 'No WLA'
        # signal_area_hbi = 0
        # if wla_architect_input == 'Foveros DoW':
        #     dow_architect_input = st.selectbox(label='DoW Architecture', options=['DoW50','DoW36','DoW25 w/o IO redundancy', 'DoW25 w/ 2:38 IO redundancy'])
        # elif wla_architect_input == 'ODI':
        #     odi_chiplet_size_input = st.selectbox(label='ODI Chiplet Size', options=['ODI25 7-50 mm2','ODI25 50-100 mm2','ODI25 100-200 mm2'])
        # elif wla_architect_input == 'HBI':
        #     hbi_architect_input = st.selectbox(label='HBI Architecture', options=['W2W HBI'])
        #     signal_area_hbi = st.number_input(label='Signal Area [mm2]/chiplet', min_value=0, max_value=50, value=26)

        # st.write('Other Information')
        # die_architect_input = st.selectbox(label='Die Architecture', options=['EMIB, SOD + Subst. Cu FLI, die size: <800mm2, BP (core/bridge):130/55um IO redun:1/1200', \
        #     'EMIB, Die Cu FLI + ASOS, die size: <400mm2, BP (core/bridge):100/55um IO redun:1/16', \
        #     'EMIB, Split solder, die size: <800mm2, BP (core/bridge):100/55um IO redun:1/16', \
        #     'EMIB, Split solder, die size: <800mm2, BP (core/bridge):100/45um IO redun:1/16', \
        #     'CoEMIB, Split solder, die size: <800mm2, BP (core/bridge):100/55um IO redun:1/16', \
        #     'Legacy monolithic, Die Cu FLI + Microball', \
        #     'Foveros Client, Split solder, die size: less than 400mm2, BP (core/bridge):110um IO redun:No'])
        # type_num_satellite = st.number_input(label='Number of Satellite Die (HBM, XCVR, etc.)', min_value=0, max_value=50, value=2)
        # exist_hbm = st.selectbox(label='Does HBM exist?', options=['Yes','No'])
        # lifetime_volume = st.selectbox(label='Lifetime Volume', options=['Typical client: about 500Mu', \
        #            'Typical Server', \
        #            'Low client < 50-100Mu (10-20% of typical client vol.)' \
        #            'Low server < 50-100Mu (10-20% of typical server vol.)'])
        # architecture_maturity_input = st.selectbox(label='Architecture Maturity', options=['Client - evolutionary', 'Server - evolutionary', 'Client - revolutionary', 'Server - revolutionary'])
        

        # if st.button('Run Data Prediction', key='RoT_Button'):
        #     st.dataframe(self.rot_model.lrp_prediction(chiplet_num=chiplet_num, pkg_type=package_type_input, main_num=num_main, \
        #                                             exist_emib=exist_emib_input, point_pkg=exist_point_input, lifetime_vol_input_val=lifetime_volume, \
        #                                             wla_architect=wla_architect_input, dow_architect_input_val=dow_architect_input, odi_chiplet_size=odi_chiplet_size_input, \
        #                                             hbi_architect=hbi_architect_input, signal_area_hbi=signal_area_hbi, exist_hbm_input_val=exist_hbm, \
        #                                             die_architect_input_val=die_architect_input, type_num_satellite_input_val=type_num_satellite, \
        #                                             architecture_maturity_val=architecture_maturity_input))
        st.write('LRP Data Update: RoT')
        st.write('General Information')
        self.de_model.submission.create_Form('RoT')
        self.de_model.submission.form.set_Fields()
        
        product_name_input = st.text_input(label=self.de_model.submission.form.fields['Product_Name']['Field_Question'], value='', key='product_name_rot')
        optional_skew_checkbox_input = st.checkbox(label=self.de_model.submission.form.fields['Skew_Name']['Field_Question'], key='optional_skew_rot')

        if optional_skew_checkbox_input:
            skew_name_input = st.text_input(label='Skew Name', value='', key='skew_name_rot')
        else:
            skew_name_input = ''

        package_type_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type']['Field_Question'], \
                                          options=self.de_model.submission.form.fields['Package_Type']['Field_Selection'])
        
        package_type_estim_input = st.selectbox(label=self.de_model.submission.form.fields['Package_Type_Estimation']['Field_Question'], \
                                          options=self.de_model.submission.form.fields['Package_Type_Estimation']['Field_Selection'])
        
        num_main = st.number_input(label=self.de_model.submission.form.fields['Number_of_Main_Die']['Field_Question'], \
                                    min_value=self.de_model.submission.form.fields['Number_of_Main_Die']['Min_Value'], \
                                    max_value=self.de_model.submission.form.fields['Number_of_Main_Die']['Max_Value'], \
                                    value=self.de_model.submission.form.fields['Number_of_Main_Die']['Default_Value'])
        
        exist_emib_input = st.selectbox(label=self.de_model.submission.form.fields['Exist_EMIB']['Field_Question'], \
                                        options=self.de_model.submission.form.fields['Exist_EMIB']['Field_Selection'])
        
        exist_point_input = st.selectbox(label=self.de_model.submission.form.fields['Exist_POINT']['Field_Question'], \
                                        options=self.de_model.submission.form.fields['Exist_POINT']['Field_Selection'])

        st.write('WLA Information') 
        wla_architect_input = st.selectbox(label=self.de_model.submission.form.fields['WLA_Architecture']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['WLA_Architecture']['Field_Selection'])
        
        chiplet_num = st.number_input(label=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Field_Question'], \
                                    min_value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Min_Value'], \
                                    max_value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Max_Value'], \
                                    value=self.de_model.submission.form.fields['Number_of_Chiplet_Base_Die']['Default_Value'])
        
        dow_architect_input = 'No WLA'
        odi_chiplet_size_input = 'No WLA'
        hbi_architect_input = 'No WLA'
        signal_area_hbi = 0
        if wla_architect_input == 'Foveros DoW':
            dow_architect_input = st.selectbox(label=self.de_model.submission.form.fields['DoW_Architecture']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['DoW_Architecture']['Field_Selection'])
        elif wla_architect_input == 'ODI':
            odi_chiplet_size_input = st.selectbox(label=self.de_model.submission.form.fields['ODI_Chiplet_Size']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['ODI_Chiplet_Size']['Field_Selection'])
        elif wla_architect_input == 'HBI':
            hbi_architect_input = st.selectbox(label=self.de_model.submission.form.fields['HBI_Architecture']['Field_Question'], \
                                            options=self.de_model.submission.form.fields['HBI_Architecture']['Field_Selection'])
            
            signal_area_hbi = st.number_input(label=self.de_model.submission.form.fields['Signal_Area']['Field_Question'], \
                                    min_value=self.de_model.submission.form.fields['Signal_Area']['Min_Value'], \
                                    max_value=self.de_model.submission.form.fields['Signal_Area']['Max_Value'], \
                                    value=self.de_model.submission.form.fields['Signal_Area']['Default_Value'])

        st.write('Other Information')
        die_architect_input = st.selectbox(label=self.de_model.submission.form.fields['Die_Architecture_Summary']['Field_Question'], \
                                         options=self.de_model.submission.form.fields['Die_Architecture_Summary']['Field_Selection'])
        
        type_num_satellite = st.number_input(label=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Field_Question'], \
                                             min_value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Min_Value'], \
                                             max_value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Max_Value'], \
                                             value=self.de_model.submission.form.fields['Number_of_Satellite_Die']['Default_Value'])
        
        exist_hbm = st.selectbox(label=self.de_model.submission.form.fields['Exist_HBM']['Field_Question'], \
                                  options=self.de_model.submission.form.fields['Exist_HBM']['Field_Selection'],)
        
        lifetime_volume = st.selectbox(label=self.de_model.submission.form.fields['Lifetime_Volume']['Field_Question'], \
                                    options=self.de_model.submission.form.fields['Lifetime_Volume']['Field_Selection'])

        architecture_maturity_input = st.selectbox(label=self.de_model.submission.form.fields['Architecture_Maturity']['Field_Question'], \
                                    options=self.de_model.submission.form.fields['Architecture_Maturity']['Field_Selection'])
        
        run_prediction_input = st.button('Run Data Prediction', key='RoT_Button')
    

        result, lrp_output = self.de_model.rot_model.lrp_prediction(product_name=product_name_input, skew_name=skew_name_input, chiplet_num=chiplet_num, \
                                                                pkg_type=package_type_estim_input, pkg_class=package_type_input, main_num=num_main, exist_emib=exist_emib_input, \
                                                                point_pkg=exist_point_input, lifetime_vol_input_val=lifetime_volume, \
                                                                wla_architect=wla_architect_input, dow_architect_input_val=dow_architect_input, \
                                                                odi_chiplet_size=odi_chiplet_size_input, hbi_architect=hbi_architect_input, signal_area_hbi=signal_area_hbi,  \
                                                                exist_hbm_input_val=exist_hbm, die_architect_input_val=die_architect_input, type_num_satellite_input_val=type_num_satellite, \
                                                                architecture_maturity_val=architecture_maturity_input)
        if run_prediction_input:
            st.dataframe(result)
        
        
        if st.button('Submit to Database?', key='DB_Submission'):
            user_id='vpillai'
            field_values_dict = lrp_output
            self.de_model.submission.set_Submission_Attributes(user_id=user_id, field_values_dict=field_values_dict)
            record = self.de_model.submission.publish_Submission()
            st.write(record)

    def me_view(self):
        st.write('LRP Data Update: Manual Entry')
        st.write('Product Information')
        product_type_input = st.text_input(label='Product Name', value='', key='product_name_me')
        optional_skew_checkbox_input = st.checkbox(label='Need to specify Skew? (Check if Yes)', value=False, key='optional_skew_me')
        if optional_skew_checkbox_input:
            skew_input = st.text_input(label='Skew Name', value='', key='skew_name_me')
        package_type_input = st.selectbox(label='Package Type', options=['Client','Server','Graphics','ASIC','PSG'], key='package_type_me')
        die_architect_input = st.selectbox(label='Die Architecture', options=['Legacy Client','Foveros Client', 'EMIB', 'Co-EMIB'], key='die_arch_me')
        if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
            wla_arch_maturity_input = st.selectbox(label='WLA Maturity', options=['Evolutionary','Revolutionary'], key='wla_maturity_me')
        pkg_assemb_maturity_input = st.selectbox(label='Pkg Assemb Maturity', options=['Evolutionary','Revolutionary'], key='pkg_assemb_maturity_me')
        if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
            prq_wla_rtd_input = st.number_input(label='PRQ WLA RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
            prq_wla_test_input = st.number_input(label='PRQ WLA Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
            prq_pkg_assemb_rtd_input = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
            prq_pkg_test_piyl_input = st.number_input(label='PRQ Pkg Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
            prq_pkg_assemb_finish_input = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
        else:
            prq_pkg_assemb_rtd_input = st.number_input(label='PRQ Pkg Assemb RtD', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
            prq_pkg_test_piyl_input = st.number_input(label='PRQ Pkg Test PIYL', min_value=0.0, max_value=100.0, value=99.0, step=0.1)
            prq_pkg_assemb_finish_input = st.number_input(label='PRQ Pkg Assemb Finish', min_value=0.0, max_value=100.0, value=99.0, step=0.1)

        if st.button('Run Data Prediction', key='ME_Button'):
            if optional_skew_checkbox_input:
                st.write(f'Product Name: {product_type_input} {skew_input}')
                st.write(f'Package Type: {package_type_input}')
            else:
                st.write(f'Product Name: {product_type_input}')
                st.write(f'Package Type: {package_type_input}')    
            if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
                st.dataframe(self.me_model.lrp_prediction(Die_Architecture_Info_val=die_architect_input, WLA_Maturity=wla_arch_maturity_input, \
                                        Pkg_Assemb_Maturity=pkg_assemb_maturity_input, PRQ_WLA_RtD=prq_wla_rtd_input, \
                                        PRQ_WLA_Test_PIYL=prq_wla_test_input, PRQ_Pkg_Assemb_RtD=prq_pkg_assemb_rtd_input, \
                                        PRQ_Pkg_Test_PIYL=prq_pkg_test_piyl_input, PRQ_Pkg_Assemb_Finish=prq_pkg_assemb_finish_input))
            else:
                st.dataframe(self.me_model.lrp_prediction(Die_Architecture_Info_val=die_architect_input, WLA_Maturity=None, \
                            Pkg_Assemb_Maturity=pkg_assemb_maturity_input, PRQ_WLA_RtD=None, \
                            PRQ_WLA_Test_PIYL=None, PRQ_Pkg_Assemb_RtD=prq_pkg_assemb_rtd_input, \
                            PRQ_Pkg_Test_PIYL=prq_pkg_test_piyl_input, PRQ_Pkg_Assemb_Finish=prq_pkg_assemb_finish_input))

    def view(self):
        st.write("Data Entry")
        rot, man_ent = st.tabs(["RoT", "Manual Entry"])

        with rot:
            self.rot_view()
    
        with man_ent:
            self.me_view()



