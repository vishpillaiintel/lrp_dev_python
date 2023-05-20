# Config files for RoT and ManEntry Forms  
# get field_name, field_id, field_question, field_type, field_selection, field_required

rot_config = {
    'Product_Name': {
        'Field_ID': 5810001,
        'Field_Type': str,
        'Field_Question': 'Product Name',
        'Field_Required': 1
    },
    'Skew_Name': {
        'Field_ID': 9048937,
        'Field_Type': str,
        'Field_Question': 'Need to specify Skew? (Check if Yes)',
        'Field_Required': 1
    },
    'Package_Type': {
        'Field_ID': 7129156,
        'Field_Type': str,
        'Field_Question': 'Package Type',
        'Field_Selection': ['Client','Server','Graphics','ASIC','PSG'],
        'Field_Required': 1
    },
    'Package_Type_Estimation': {
        'Field_ID': 7392235,
        'Field_Type': str,
        'Field_Question': 'Package Type Estimation',
        'Field_Selection': ['Client','Server','Beast (>>SPR-XCC)'],
        'Field_Required': 1
    },
    'Number_of_Main_Die': {
        'Field_ID': 1524252,
        'Field_Type': int,
        'Field_Question': 'Number of Main Die',
        'Field_Required': 1,
        'Max_Value': 50,
        'Min_Value': 0,
        'Default_Value': 2
    },
    'Exist_EMIB': {
        'Field_ID': 4385865,
        'Field_Type': str,
        'Field_Question': 'Does main die have EMIB?',
        'Field_Selection': ['Yes','No'],
        'Field_Required': 1
    },
    'Exist_POINT': {
        'Field_ID': 9925025,
        'Field_Type': str,
        'Field_Question': 'Is this a POINT package?',
        'Field_Selection': ['Yes','No'],
        'Field_Required': 1
    },
    'WLA_Architecture': {
        'Field_ID': 5186361,
        'Field_Type': str,
        'Field_Question': 'WLA Architecture',
        'Field_Selection': ['No WLA','Foveros DoW','ODI','HBI'],
        'Field_Required': 1
    },
    'Number_of_Chiplet_Base_Die': {
        'Field_ID': 6399643,
        'Field_Type': int,
        'Field_Question': 'Number of chiplet/base die',
        'Field_Required': 1,
        'Max_Value': 50,
        'Min_Value': 0,
        'Default_Value': 2
    },
    'DoW_Architecture': {
        'Field_ID': 4604580,
        'Field_Type': str,
        'Field_Question': 'DoW Architecture',
        'Field_Selection': ['DoW50','DoW36','DoW25 w/o IO redundancy', 'DoW25 w/ 2:38 IO redundancy'],
        'Field_Required': 1
    },
    'ODI_Chiplet_Size': {
        'Field_ID': 6520270,
        'Field_Type': str,
        'Field_Question': 'DoW Architecture',
        'Field_Selection': ['ODI25 7-50 mm2','ODI25 50-100 mm2','ODI25 100-200 mm2'],
        'Field_Required': 1
    },
    'HBI_Architecture': {
        'Field_ID': 2320158,
        'Field_Type': str,
        'Field_Question': 'HBI Architecture',
        'Field_Selection': ['W2W HBI'],
        'Field_Required': 1
    },
    'Signal_Area': {
        'Field_ID': 8504148,
        'Field_Type': int,
        'Field_Question': 'Signal Area [mm2]/chiplet',
        'Field_Required': 1,
        'Max_Value': 50,
        'Min_Value': 0,
        'Default_Value': 26
    },
    'Die_Architecture_Summary': {
        'Field_ID': 1324626,
        'Field_Type': str,
        'Field_Question': 'Die Architecture',
        'Field_Selection': ['EMIB, SOD + Subst. Cu FLI, die size: <800mm2, BP (core/bridge):130/55um IO redun:1/1200', \
            'EMIB, Die Cu FLI + ASOS, die size: <400mm2, BP (core/bridge):100/55um IO redun:1/16', \
            'EMIB, Split solder, die size: <800mm2, BP (core/bridge):100/55um IO redun:1/16', \
            'EMIB, Split solder, die size: <800mm2, BP (core/bridge):100/45um IO redun:1/16', \
            'CoEMIB, Split solder, die size: <800mm2, BP (core/bridge):100/55um IO redun:1/16', \
            'Legacy monolithic, Die Cu FLI + Microball', \
            'Foveros Client, Split solder, die size: less than 400mm2, BP (core/bridge):110um IO redun:No'],
        'Field_Required': 1
    },
    'Number_of_Satellite_Die': {
        'Field_ID': 8798100,
        'Field_Type': int,
        'Field_Question': 'Number of Satellite Die (HBM, XCVR, etc.)',
        'Field_Required': 1,
        'Max_Value': 50,
        'Min_Value': 0,
        'Default_Value': 2
    },
    'Exist_HBM': {
        'Field_ID': 2561463,
        'Field_Type': str,
        'Field_Question': 'Does HBM exist?',
        'Field_Selection': ['Yes','No'],
        'Field_Required': 1
    },
    'Lifetime_Volume': {
        'Field_ID': 6829173,
        'Field_Type': str,
        'Field_Question': 'Lifetime Volume',
        'Field_Selection': ['Typical client: about 500Mu', \
                   'Typical Server', \
                   'Low client < 50-100Mu (10-20% of typical client vol.)' \
                   'Low server < 50-100Mu (10-20% of typical server vol.)'],
        'Field_Required': 1
    },
    'Architecture_Maturity': {
        'Field_ID': 8025215,
        'Field_Type': str,
        'Field_Question': 'Lifetime Volume',
        'Field_Selection': ['Client - evolutionary', \
                            'Server - evolutionary', \
                                'Client - revolutionary', 'Server - revolutionary'],
        'Field_Required': 1
    }
}

manual_entry_config = {
    'Product_Name': {
        'Field_ID': 9620264,
        'Field_Type': str,
        'Field_Question': 'Product Name',
        'Field_Required': 1
    },
    'Skew_Name': {
        'Field_ID': 5765678,
        'Field_Type': str,
        'Field_Question': 'Need to specify Skew? (Check if Yes)',
        'Field_Required': 1
    },
    'Package_Type': {
        'Field_ID': 7450508,
        'Field_Type': str,
        'Field_Question': 'Package Type',
        'Field_Selection': ['Client','Server','Graphics','ASIC','PSG'],
        'Field_Required': 1
    },
    'Die_Architecture': {
        'Field_ID': 6360244,
        'Field_Type': str,
        'Field_Question': 'Die Architecture',
        'Field_Selection': ['Legacy Client','Foveros Client', 'EMIB', 'Co-EMIB'],
        'Field_Required': 1
    },
    'WLA_Architecture_Maturity': {
        'Field_ID': 8487360,
        'Field_Type': str,
        'Field_Question': 'WLA Architecture Maturity',
        'Field_Selection': ['Evolutionary','Revolutionary'],
        'Field_Required': 1
    },
    'Pkg_Assembly_Architecture_Maturity': {
        'Field_ID': 9006722,
        'Field_Type': str,
        'Field_Question': 'Pkg Assembly Architecture Maturity',
        'Field_Selection': ['Evolutionary','Revolutionary'],
        'Field_Required': 1
    }
}
