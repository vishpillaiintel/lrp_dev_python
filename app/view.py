
import streamlit as st
import pandas as pd
import numpy as np

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
    def __init__(self, rot_model, me_model):
        self.rot_model = rot_model
        self.me_model = me_model

    def rot_view(self):
        st.write('LRP Data Update: RoT')
        st.write('General Information')
        package_type_input = st.selectbox(label='Package Type', options=['Client','Server','Beast (>>SPR-XCC)'])
        num_main = st.number_input(label='Number of Main Die', min_value=0, max_value=50, value=2)
        exist_emib_input = st.selectbox(label='Does main die have EMIB?', options=['Yes','No'])
        exist_point_input = st.selectbox(label='Is this a POINT package?', options=['Yes','No'])

        st.write('WLA Information') 
        wla_architect_input = st.selectbox(label='WLA Architecture', options=['No WLA','Foveros DoW','ODI','HBI'])
        chiplet_num = st.number_input(label='Number of chiplet/base die', min_value=0, max_value=50, value=2)
        dow_architect_input = 'No WLA'
        odi_chiplet_size_input = 'No WLA'
        hbi_architect_input = 'No WLA'
        signal_area_hbi = 0
        if wla_architect_input == 'Foveros DoW':
            dow_architect_input = st.selectbox(label='DoW Architecture', options=['DoW50','DoW36','DoW25 w/o IO redundancy', 'DoW25 w/ 2:38 IO redundancy'])
        elif wla_architect_input == 'ODI':
            odi_chiplet_size_input = st.selectbox(label='ODI Chiplet Size', options=['ODI25 7-50 mm2','ODI25 50-100 mm2','ODI25 100-200 mm2'])
        elif wla_architect_input == 'HBI':
            hbi_architect_input = st.selectbox(label='HBI Architecture', options=['W2W HBI'])
            signal_area_hbi = st.number_input(label='Signal Area [mm2]/chiplet', min_value=0, max_value=50, value=26)

        st.write('Other Information')
        die_architect_input = st.selectbox(label='Die Architecture', options=['EMIB, SOD + Subst. Cu FLI, die size: <800mm2, BP (core/bridge):130/55um IO redun:1/1200', \
            'EMIB, Die Cu FLI + ASOS, die size: <400mm2, BP (core/bridge):100/55um IO redun:1/16', \
            'EMIB, Split solder, die size: <800mm2, BP (core/bridge):100/55um IO redun:1/16', \
            'EMIB, Split solder, die size: <800mm2, BP (core/bridge):100/45um IO redun:1/16', \
            'CoEMIB, Split solder, die size: <800mm2, BP (core/bridge):100/55um IO redun:1/16', \
            'Legacy monolithic, Die Cu FLI + Microball', \
            'Foveros Client, Split solder, die size: less than 400mm2, BP (core/bridge):110um IO redun:No'])
        type_num_satellite = st.number_input(label='Number of Satellite Die (HBM, XCVR, etc.)', min_value=0, max_value=50, value=2)
        exist_hbm = st.selectbox(label='Does HBM exist?', options=['Yes','No'])
        lifetime_volume = st.selectbox(label='Lifetime Volume', options=['Typical client: about 500Mu', \
                   'Typical Server', \
                   'Low client < 50-100Mu (10-20% of typical client vol.)' \
                   'Low server < 50-100Mu (10-20% of typical server vol.)'])
        architecture_maturity_input = st.selectbox(label='Architecture Maturity', options=['Client - evolutionary', 'Server - evolutionary', 'Client - revolutionary', 'Server - revolutionary'])
        

        if st.button('Run Data Prediction', key='RoT_Button'):
            st.dataframe(self.rot_model.lrp_prediction(chiplet_num=chiplet_num, pkg_type=package_type_input, main_num=num_main, \
                                                    exist_emib=exist_emib_input, point_pkg=exist_point_input, lifetime_vol_input_val=lifetime_volume, \
                                                    wla_architect=wla_architect_input, dow_architect_input_val=dow_architect_input, odi_chiplet_size=odi_chiplet_size_input, \
                                                    hbi_architect=hbi_architect_input, signal_area_hbi=signal_area_hbi, exist_hbm_input_val=exist_hbm, \
                                                    die_architect_input_val=die_architect_input, type_num_satellite_input_val=type_num_satellite, \
                                                    architecture_maturity_val=architecture_maturity_input))
        
    def me_view(self):
        st.write('LRP Data Update: Manual Entry')
        st.write('Product Information')
        product_type_input = st.text_input(label='Product Name', value='')
        optional_skew_checkbox_input = st.checkbox(label='Need to specify Skew? (Check if Yes)', value=False)
        if optional_skew_checkbox_input:
            skew_input = st.text_input(label='Skew Name', value='')
        package_type_input = st.selectbox(label='Package Type', options=['Client','Server','Graphics','ASIC','PSG'])
        die_architect_input = st.selectbox(label='Die Architecture', options=['Legacy Client','Foveros Client', 'EMIB', 'Co-EMIB'])
        if die_architect_input == 'Foveros Client' or die_architect_input == 'Co-EMIB':
            wla_arch_maturity_input = st.selectbox(label='WLA Maturity', options=['Evolutionary','Revolutionary'])
        pkg_assemb_maturity_input = st.selectbox(label='Pkg Assemb Maturity', options=['Evolutionary','Revolutionary'])
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

