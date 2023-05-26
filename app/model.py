from operator import index
import os
import pandas as pd
import numpy as np
import mysql.connector
import random
from dotenv import load_dotenv
import config
from datetime import datetime


load_dotenv()


class Database(object):
    def __init__(self, conn_config):
        # Port number needs to be an integer
        conn_config['port'] = int(conn_config['port'])

        # Set config 
        self.db_config = {'host': conn_config['host'], 'db': conn_config['db'], 'port': conn_config['port'], \
                           'user': conn_config['user'], 'passwd': conn_config['passwd']}
        self.db_conn = None
        self.db_cursor = None

    def __enter__(self):
        # This ensure, whenever an object is created using "with"
        # this magic method is called, where you can create the connection.
        self.db_conn = mysql.connector.connect(host=self.db_config['host'], port=self.db_config['port'], \
                                                db=self.db_config['db'], user=self.db_config['user'], \
                                                passwd=self.db_config['passwd'])
        self.db_cursor = self.db_conn.cursor()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # once the with block is over, the __exit__ method would be called
        # with that, you close the connnection
        try:
            self.db_conn.close()
        except AttributeError: # isn't closable
            print('Not closable.')

    def get_row(self, sql):
        df = pd.read_sql(sql, self.db_conn)
        return df


class LRP_Model:
    def __init__(self):
        print(os.environ.get('host'))
        self.db_config =  {
            'host': f"{os.environ.get('host')}",
            'port': f"{os.environ.get('portnum')}",
            'user':f"{os.environ.get('user')}",
            'passwd':f"{os.environ.get('passwd')}",
            'db':f"{os.environ.get('db')}"
        }
        self.approvals = []

    def get_data(self):
        sql = f"""
        SELECT a.ApprovalID, a.ApproverID, fs.SubmissionID, fs.FormID, f.FormName, 
            fs.SubmissionDate, fs.UserID, sf.FieldValue
            FROM Form_Submissions fs
        LEFT JOIN Approvals a on a.SubmissionID
        LEFT JOIN Submission_Fields sf on fs.SubmissionID
        LEFT JOIN Forms f on f.FormID = fs.FormID
            WHERE fs.SubmissionID = sf.SubmissionID
            AND fs.SubmissionID = a.SubmissionID
        """
        with Database(self.db_config) as db_conn:
            df = db_conn.get_row(sql)
        
        approvals = []

        for a in df.itertuples():
            approv = Approval()
            approv.approval_id = a.ApprovalID 
            approv.submission_id = a.SubmissionID
            approv.approver_id = a.ApproverID
            approv.retrieve_Form(form_name=a.FormName, form_id=a.FormID)
            approv.submission_date = a.SubmissionDate
            approv.user_id = a.UserID
            approv.field_values_db = a.FieldValue
            approv.parse_FieldValues_db()
            approvals.append(approv)

        self.approvals = approvals

    def create_LRP_master(self):
        
        # get data from DB and create approval objects as class attribute
        self.get_data()
        
        # initialize dataframe
        lrp_master = pd.DataFrame(columns=["Product Name", "Skew Name", "Package Type", "Milestone", "PO/ES0",  \
                                           "ES1", "ES2", "PQS", "QS", "PRQ", "PRQ+1Q", "Submission Type", "Last LRP Cycle Update"])
        loc_index = 0

        # iterate through approvals and add to LRP master dataframe
        for approval in self.approvals:
            lrp_master, loc_index = self.append_master(approval.field_values_dict, lrp_master, loc_index, approval.form.form_name, approval.submission_date)
        
        self.master = lrp_master
    

    def append_master(self, fv, master_table, index, submission_type, submission_date):
        # utilizing product, skew, package, and milestone values -> create local df and append to master
        product_name = fv['Product_Name']
        skew_name = fv['Skew_Name']
        package_type = fv['Package_Type']
        wla = 0
        pqs = 0 
        for key in fv.keys():
            if (';' in key) and ('WLA' in key):
                wla = 1
                continue
            elif (';' in key) and ('PQS' in key):
                pqs = 1

        if wla:
            milestone_order = ['WLA RtD', 'WLA Test PIYL','WLA Inventory Yield','Pkg Assemb RtD', \
                               'Pkg Assemb Test PIYL','Pkg Assemb Finish','Pkg Assemb Inventory Yield']
        else: 
            milestone_order = ['Pkg Assemb RtD','Pkg Assemb Test PIYL','Pkg Assemb Finish','Pkg Assemb Inventory Yield']

        if pqs:

            for milestone in milestone_order:
                master_table.loc[index] = [product_name, skew_name, package_type, milestone, \
                                    fv[self.idx_milestone(milestone, 0)], fv[self.idx_milestone(milestone, 1)], \
                                    fv[self.idx_milestone(milestone, 2)], fv[self.idx_milestone(milestone, 3)], \
                                    fv[self.idx_milestone(milestone, 4)], fv[self.idx_milestone(milestone, 5)], \
                                    fv[self.idx_milestone(milestone, 6)], submission_type, \
                                    self.get_LRP_Quarter(submission_date=submission_date)]
                index+=1
        else:
            for milestone in milestone_order:
                master_table.loc[index] = [product_name, skew_name, package_type, milestone, \
                                    fv[self.idx_milestone(milestone, 0)], fv[self.idx_milestone(milestone, 1)], \
                                    fv[self.idx_milestone(milestone, 2)], 'N/A', fv[self.idx_milestone(milestone, 4)], \
                                    fv[self.idx_milestone(milestone, 5)], fv[self.idx_milestone(milestone, 6)], \
                                    submission_type, self.get_LRP_Quarter(submission_date=submission_date)]
                index+=1
        return master_table, index

    def idx_milestone(self, milestone, prq_timeline_i):
        prq_timeline_order = ['PO/ES0', 'ES1', 'ES2', 'PQS', 'QS', 'PRQ', 'PRQ+1Q']
        index = milestone + ';' + prq_timeline_order[prq_timeline_i]
        return index

    def get_LRP_Quarter(self, submission_date):
        m = int(submission_date[:2])
        q = (m-1)//3 + 1
        y = int(submission_date[6:10])
        output = 'Q' + str(q) + ' ' + str(y)
        return output
        

class Data_Entry_Model():
    def __init__(self):
        self.submission = Submission()
        self.rot_model = RoT_Model()
        self.me_model = Manual_Entry_Model()

class Data_Review_Model():
    def __init__(self):
        self.db_config =  {
            'host': f"{os.environ.get('host')}",
            'port': f"{os.environ.get('portnum')}",
            'user':f"{os.environ.get('user')}",
            'passwd':f"{os.environ.get('passwd')}",
            'db':f"{os.environ.get('db')}"
        }
        self.rot_model = RoT_Model()
        self.me_model = Manual_Entry_Model()
        self.pending_submissions = []

    def get_Pending_Submissions(self):
        pending = 'Pending'
        sql = f"""
            SELECT fs.SubmissionID, fs.FormID, f.FormName, 
                fs.SubmissionDate, fs.SubmissionStatus, fs.UserID, sf.FieldValue
            FROM Form_Submissions fs
            LEFT JOIN Submission_Fields sf on fs.SubmissionID
            LEFT JOIN Forms f on f.FormID = fs.FormID
                WHERE fs.SubmissionID = sf.SubmissionID
                AND fs.SubmissionStatus = '{pending}'
        """
        with Database(self.db_config) as db_conn:
            df = db_conn.get_row(sql)
        
        submissions = []
        for a in df.itertuples():
            submission = Submission()
            submission.retrieve_Form(form_name=a.FormName, form_id=a.FormID)
            submission.submission_date = a.SubmissionDate
            submission.submission_status = a.SubmissionStatus
            submission.user_id = a.UserID
            submission.submission_id = a.SubmissionID
            submission.field_values_db = a.FieldValue
            submissions.append(submission)

        self.pending_submissions = submissions

    def set_Submission_to_Review(self, submission_id):
        for sub in self.pending_submissions:
            if sub.submission_id == submission_id:
                self.submission_review = sub
                self.submission_review.parse_FieldValues_db()
                return
    
    def create_Approval(self, user_id, field_values_dict):
        new_approval = Approval()
        new_approval.set_Approval_Attributes(submission_id=self.submission_review.submission_id, \
                                            user_id=user_id)
        record = new_approval.publish_Approval(field_values_dict)
        return record

class Resubmission_Model():
    
    def __init__(self):
        self.db_config =  {
            'host': f"{os.environ.get('host')}",
            'port': f"{os.environ.get('portnum')}",
            'user':f"{os.environ.get('user')}",
            'passwd':f"{os.environ.get('passwd')}",
            'db':f"{os.environ.get('db')}"
        }
        self.rot_model = RoT_Model()
        self.me_model = Manual_Entry_Model()
        self.rejected_submissions = []

    def get_Rejected_Submissions(self, user_id):
        rejected = 'Rejected'
        sql = f"""
            SELECT fs.SubmissionID, fs.FormID, f.FormName, 
                fs.SubmissionDate, fs.SubmissionStatus, fs.UserID, sf.FieldValue
                FROM Form_Submissions fs
            LEFT JOIN Submission_Fields sf on fs.SubmissionID
            LEFT JOIN Forms f on f.FormID = fs.FormID
                WHERE fs.SubmissionID = sf.SubmissionID
                AND fs.SubmissionStatus = '{rejected}'
                AND fs.UserID = '{user_id}'
        """

        with Database(self.db_config) as db_conn:
            df = db_conn.get_row(sql)
        
        submissions = []
        for a in df.itertuples():
            submission = Submission()
            submission.retrieve_Form(form_name=a.FormName, form_id=a.FormID)
            submission.submission_date = a.SubmissionDate
            submission.submission_status = a.SubmissionStatus
            submission.user_id = a.UserID
            submission.submission_id = a.SubmissionID
            submission.field_values_db = a.FieldValue
            submissions.append(submission)

        self.rejected_submissions = submissions

    def set_Submission_to_Resubmit(self, submission_id):
        for sub in self.rejected_submissions:
            if sub.submission_id == submission_id:
                self.submission_resubmit = sub
                self.submission_resubmit.parse_FieldValues_db()
                return

class Submission():
    def __init__(self):
        self.field_values_dict = None
        self.field_values_db = None
        self.form = None
        self.user_id = None
        self.submission_status = None
        self.submission_date = None
        self.submission_id = None
        self.db_config =  {
            'host': f"{os.environ.get('host')}",
            'port': f"{os.environ.get('portnum')}",
            'user':f"{os.environ.get('user')}",
            'passwd':f"{os.environ.get('passwd')}",
            'db':f"{os.environ.get('db')}"
        }

    def set_Submission_Attributes(self, user_id, field_values_dict):

        self.field_values_dict = field_values_dict
        self.create_FieldValues_db()
        self.user_id = user_id
        self.submission_status = 'Pending'
        self.set_Submission_ID()
        self.submission_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    def set_Submission_ID(self):
        table_name = 'Form_Submissions'
        column_name = 'SubmissionID'
        sql = f"""
            SELECT 
                {column_name} 
            FROM 
                {table_name}
        """
        with Database(self.db_config) as db_conn:
            df = db_conn.get_row(sql)
        
        id = random.randint(111111, 999999)
        
        while id in df[column_name]:
            id = random.randint(111111, 999999)

        self.submission_id = id


    def create_Form(self, form_name):
        # set form based on user input of form name
        self.form = Form(form_name)
        self.form = self.form.set_Fields()
    
    def publish_Submission(self):
        output_record = ''
        # send to database, insert into Form_Submissions
        with Database(self.db_config) as db_conn:
            mycursor = db_conn.db_cursor
            table = 'Form_Submissions'
            sql = f"INSERT INTO {table} (SubmissionID, UserID, SubmissionDate, SubmissionStatus, FormID) VALUES (%s, %s, %s, %s, %s)"
            val = (str(self.submission_id), str(self.user_id), str(self.submission_date), str(self.submission_status), str(self.form.form_id))
            mycursor.execute(sql, val)
            db_conn.db_conn.commit()
            output_record+=f'{mycursor.rowcount} record inserted into {table}.\n'
        
        # send to database, insert into Submission_Fields 
        with Database(self.db_config) as db_conn:
            mycursor = db_conn.db_cursor
            table = 'Submission_Fields'
            sql = f"INSERT INTO {table} (SubmissionID, FieldValue) VALUES (%s, %s)"
            val = (str(self.submission_id), str(self.field_values_db))
            mycursor.execute(sql, val)
            db_conn.db_conn.commit()
            output_record+=f'{mycursor.rowcount} record inserted into {table}.\n'

        return output_record
    
    def update_Submission(self, status, field_values_dict):
        
        self.field_values_dict = field_values_dict
        self.create_FieldValues_db()
    
        output_record = ''

        # send to Approvals table AND reset_Submission_Status(self):
        self.reset_Submission_Status(status=status)
        
        # first, reset submission status to approved in Form_Submissions
        with Database(self.db_config) as db_conn:
            mycursor = db_conn.db_cursor
            table = 'Form_Submissions'
            submission_status = 'SubmissionStatus'
            submission_id = 'SubmissionID'
            sql = f"UPDATE {table} SET {submission_status} = '{self.submission_status}' WHERE {submission_id} = '{self.submission_id}'"
            mycursor.execute(sql)
            db_conn.db_conn.commit()
            if mycursor.rowcount > 0:
                output_record += f'{mycursor.rowcount} record updated in {table}. '
        
        # send to database, insert into Submission_Fields 
        with Database(self.db_config) as db_conn:
            mycursor = db_conn.db_cursor
            table = 'Submission_Fields'
            field_value = 'FieldValue'
            submission_id = 'SubmissionID'
            sql = f"UPDATE {table} SET {field_value} = '{self.field_values_db}' WHERE {submission_id} = '{self.submission_id}'"
            mycursor.execute(sql)
            db_conn.db_conn.commit()
            if mycursor.rowcount > 0:
                output_record+=f'{mycursor.rowcount} record updated into {table}.\n'

        print(output_record)
        return output_record

    def reset_Submission_Status(self, status):
        # resets SubmissionStatus.
        self.submission_status = status
    
    def retrieve_Form(self, form_name, form_id):
        self.form = Form(form_name=form_name)
        self.form = self.form.get_Form_Attributes(form_id=form_id)

    def retrieve_Submission_Attributes(self, id):
        # get all attributes from database. calls retrieve_Form, and parse_FieldValues_db().
        self.submission_id = id
        sql = f"""
            SELECT fs.SubmissionID, fs.FormID, f.FormName, 
            fs.SubmissionDate, fs.SubmissionStatus, fs.UserID, sf.FieldValue
            FROM Form_Submissions fs
            LEFT JOIN Submission_Fields sf on fs.SubmissionID
            LEFT JOIN Forms f on f.FormID = fs.FormID
            WHERE fs.SubmissionID = sf.SubmissionID
            AND fs.SubmissionID = '{self.submission_id}'
        """
        with Database(self.db_config) as db_conn:
            df = db_conn.get_row(sql)
        
        self.retrieve_Form(form_name=df['FormName'], form_id=df['FormID'])
        self.submission_date = df['SubmissionDate']
        self.submission_status = df['SubmissionStatus'] 
        self.user_id = df['UserID']
        self.field_values_db = df['FieldValue'][0]
        self.parse_FieldValues_db()

    def parse_FieldValues_db(self):
        # parse Field Values string based on "," and "=". Create FieldValues dict.
        df_field_value = self.field_values_db
        split_attrs = df_field_value.split(', ')
        attr_keys = []
        attr_values = []
        for attribute in split_attrs:
            if len(attribute.split('=')) > 1:
                attr_keys.append(attribute.split('=')[0])
                attr_values.append(attribute.split('=')[1])
            else:
                attr_keys.append(attribute.split('=')[0])
                attr_values.append('')

        self.field_values_dict = dict(zip(attr_keys, attr_values))  

    def create_FieldValues_db(self):
        # create Field Values string based on "," and "=" using already created FieldValues dict.
        fv_db = ''
        for key, value in self.field_values_dict.items():
            if key != next(reversed(self.field_values_dict.keys())):
                fv_db += str(key) + "=" + str(value) + ", "
            else:
                fv_db += str(key) + "=" + str(value)
        self.field_values_db = fv_db

class Approval(Submission):
    def __init__(self):
        self.db_config =  {
            'host': f"{os.environ.get('host')}",
            'port': f"{os.environ.get('portnum')}",
            'user':f"{os.environ.get('user')}",
            'passwd':f"{os.environ.get('passwd')}",
            'db':f"{os.environ.get('db')}"
        }
        self.approval_date = None
        self.approval_id = None
        self.approver_id = None
        self.submission_id = None
        
    def set_Approval_Attributes(self, submission_id, user_id):
        # set Approval info given submission_id and user_id (approver/admin)
        self.approver_id = user_id
        self.set_Approval_ID()
        self.approval_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.retrieve_Submission_Attributes(submission_id)

    def set_Approval_ID(self):
        table_name = 'Approvals'
        column_name = 'ApprovalID'
        sql = f"""
            SELECT 
                {column_name} 
            FROM 
                {table_name}
        """
        with Database(self.db_config) as db_conn:
            df = db_conn.get_row(sql)
        
        id = random.randint(111111, 999999)
        print(id)
        
        while id in df['ApprovalID']:
            id = random.randint(111111, 999999)

        self.approval_id = id

    def publish_Approval(self, field_values_dict):
        output_record = ''
        # update Submission tables with status as 'Approved'
        update_record = self.update_Submission(status='Approved', field_values_dict=field_values_dict)
        output_record+=update_record + ' '

        # next, insert new approval record into Approvals 
        with Database(self.db_config) as db_conn:
            mycursor = db_conn.db_cursor
            table = 'Approvals'
            sql = f"INSERT INTO {table} (ApprovalID, ApproverID, ApprovalDate, SubmissionID) VALUES (%s, %s, %s, %s)"
            val = (str(self.approval_id), str(self.approver_id), str(self.approval_date), str(self.submission_id))
            mycursor.execute(sql, val)
            db_conn.db_conn.commit()
            output_record += f'{mycursor.rowcount} record inserted into {table}.'
        
        return output_record
    

class Form():
    def __init__(self, form_name):
        self.fields = None

        if 'RoT' in str(form_name):
            self.form_name = 'RoT - Q2 2023'
            self.form_id = 0
        else:
            self.form_name = 'Manual Entry - Q2 2023'
            self.form_id = 1

    def get_Form_Attributes(self, form_id):

        self.form_id = form_id
        self.set_Fields()
        return self

    def set_Fields(self):
        if 'RoT' in self.form_name:
            self.fields = config.rot_config
        else:
            self.fields = config.manual_entry_config
        return self
    
    def get_Field_Attribute(self, field_name, field_attribute):
        return self.fields[f'{field_name}'][f'{field_attribute}']

        

class RoT_Model:

    # constants
    N_PIYL = 500
    SSDT_YL = 0.5
    WLA_RTD_DOW = 0.5
    WLA_RTD_ODI = 1.6
    WLA_RTD_HBI = 0.5
    SATELLITE_DIE_ATTACH_YL = 0.05

    def __init__(self):
        self.package_type_selection = ['Client','Server','Beast (>>SPR-XCC)']
        self.odi_size_chiplet_selection = ["No WLA", 'ODI25 7-50 mm2','ODI25 50-100 mm2','ODI25 100-200 mm2']
        self.dow_architect_selection = ["No WLA", "DoW50", "DoW36", "DoW25 w/o IO redundancy", "DoW25 w/ 2:38 IO redundancy"]
        self.hbi_architect_selection = ["No WLA", "W2W HBI"]
        self.wla_architect_selection = ["No WLA", "Foveros DoW", "ODI", "HBI"]
        self.die_architect_selection = ['EMIB; SOD + Subst. Cu FLI; die size: <800mm2; BP (core/bridge):130/55um IO redun:1/1200', \
            'EMIB; Die Cu FLI + ASOS; die size: <400mm2; BP (core/bridge):100/55um IO redun:1/16', \
            'EMIB; Split solder; die size: <800mm2; BP (core/bridge):100/55um IO redun:1/16', \
            'EMIB; Split solder; die size: <800mm2; BP (core/bridge):100/45um IO redun:1/16', \
            'CoEMIB; Split solder; die size: <800mm2; BP (core/bridge):100/55um IO redun:1/16', \
            'Legacy monolithic; Die Cu FLI + Microball', \
            'Foveros Client; Split solder; die size: less than 400mm2; BP (core/bridge):110um IO redun:No']
        self.exist_emib_selection = ["Yes", "No"]
        self.exist_point_selection = ["Yes", "No"]
        self.exist_hbm_selection = ["Yes", "No"]
        self.lifetime_vol_selection = ['Typical client: about 500Mu', \
                   'Typical Server', \
                   'Low client < 50-100Mu (10-20% of typical client vol.)' \
                   'Low server < 50-100Mu (10-20% of typical server vol.)']
        self.architecture_maturity_selection = ["Client - evolutionary", "Server - evolutionary", \
                                                 "Client - revolutionary",  "Server - revolutionary"]

        self.lrp_output = {}

    # output functions

    # WLA Yield Loss

    def wla_dow_ssdt(self, chiplet_num, dow_architect_input_val):
        if chiplet_num == 0:
            result = 0
        else:
            if dow_architect_input_val == 1:
                result = 0.1 * chiplet_num + self.SSDT_YL
            elif dow_architect_input_val == 2 or dow_architect_input_val == 4:
                result = 0.15 * chiplet_num + self.SSDT_YL
            elif dow_architect_input_val == 3:
                result = 0.25 * chiplet_num + self.SSDT_YL

        return result

    def wla_odi_ssdt(self, chiplet_num, odi_chiplet_size):
        if chiplet_num == 0:
            result = 0
        else:
            if odi_chiplet_size == 1:
                result = 0.2 * chiplet_num + self.SSDT_YL
            elif odi_chiplet_size == 2:
                result = 0.3 * chiplet_num + self.SSDT_YL
            else: # odi_chiplet_size == 3
                result = 0.4 * chiplet_num + self.SSDT_YL
        return result

    def wla_hbi_ssdt(self, chiplet_num, hbi_architect, signal_area_hbi):
        if chiplet_num == 0:
            result = 0
        else:
            if hbi_architect == 1:
                result = (1-np.exp(-0.00034*signal_area_hbi)) * 100 * chiplet_num + self.SSDT_YL
            elif hbi_architect == 2:
                # placeholder same as hbi_architect == 1
                result = (1-np.exp(-0.00034*signal_area_hbi)) * 100 * chiplet_num + self.SSDT_YL
            else:
                result = 0
        return result

    def wla_ssdt(self, wla_architect, chiplet_num, dow_architect_input_val, \
        odi_chiplet_size, hbi_architect, signal_area_hbi):
        if wla_architect == 1:
            result = 0
        elif wla_architect == 2:
            result = self.wla_dow_ssdt(chiplet_num, dow_architect_input_val)
        elif wla_architect == 3:
            result = self.wla_odi_ssdt(chiplet_num, odi_chiplet_size)
        else: # wla_architect == 4
            result = self.wla_hbi_ssdt(chiplet_num, hbi_architect, signal_area_hbi)
        return result

    def wla_dow_rtd(self, chiplet_num, wla_architect):
        if chiplet_num == 0 or wla_architect == 1:
            return 0
        else:
            return self.WLA_RTD_DOW

    def wla_odi_rtd(self, chiplet_num, wla_architect):
        if chiplet_num == 0 or wla_architect == 1:
            return 0
        else:
            return self.WLA_RTD_ODI

    def wla_hbi_rtd(self, chiplet_num, wla_architect):
        if chiplet_num == 0 or wla_architect == 1:
            return 0
        else:
            return self.WLA_RTD_HBI

    def wla_rtd(self, chiplet_num, wla_architect):
        if wla_architect == 1:
            return 0
        elif wla_architect == 2:
            return self.WLA_RTD_DOW
        elif wla_architect == 3:
           # odi_rtd = self.WLA_RTD_ODI + 0.1 * (n_topdie - 1) + 0.15 * (n_rdl - 1) - (0.1 if chiplet_num == 0 else 0)
            odi_rtd = self.WLA_RTD_ODI - (0.1 if chiplet_num == 0 else 0)

            return odi_rtd
        else: # wla_architect == 4
            return self.WLA_RTD_HBI

    def wla_dow_ttl(self, chiplet_num, wla_architect, dow_architect_input_val):
        return (1-(100-self.wla_dow_ssdt(chiplet_num, dow_architect_input_val))/ \
            100*(100-self.wla_dow_rtd(chiplet_num, wla_architect))/100)*100

    def wla_odi_ttl(self, chiplet_num, wla_architect, odi_chiplet_size):
        return (1-(100-self.wla_odi_ssdt(chiplet_num, odi_chiplet_size))/ \
            100*(100-self.wla_odi_rtd(chiplet_num, wla_architect))/100)*100

    def wla_hbi_ttl(self, chiplet_num, wla_architect, hbi_architect, signal_area_hbi):
        return (1-(100-self.wla_hbi_ssdt(chiplet_num, hbi_architect, signal_area_hbi))/ \
            100*(100-self.wla_hbi_rtd(chiplet_num, wla_architect))/100)*100

    def wla_ttl(self, chiplet_num, wla_architect, dow_architect_input_val, \
        odi_chiplet_size, hbi_architect, signal_area_hbi):
        if wla_architect == 1:
            return 0
        elif wla_architect == 2:
            return self.wla_dow_ttl(chiplet_num, wla_architect, dow_architect_input_val)
        elif wla_architect == 3:
            return self.wla_odi_ttl(chiplet_num, wla_architect, odi_chiplet_size)
        else: # wla_architect == 4
            return self.wla_hbi_ttl(chiplet_num, wla_architect, hbi_architect, signal_area_hbi)

    #  Package Assembly Yield Loss
    def pkgassy_rtd(self, pkg_type, main_num, exist_emib, point_pkg, exist_hbm_input_val):
        if pkg_type == 1:
            if exist_emib == 1:
                temp_pkgtype1_emib1 = 0.2 + 0.1 * main_num
                if point_pkg == 1:
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype1_emib1 + 0.1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype1_emib1 + 0.1 + 0

                else: # point_pkg == 2
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype1_emib1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype1_emib1 + 0

            else: # exist_emib == 2
                temp_pkgtype1_emib2 = 0.2 + 0 * main_num
                if point_pkg == 1:
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype1_emib2 + 0.1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype1_emib2 + 0.1 + 0

                else: # point_pkg == 2
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype1_emib2 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype1_emib2 + 0

        elif pkg_type == 2:
            if exist_emib == 1:
                temp_pkgtype2_emib1 = 0.3 + 0.1 * main_num
                if point_pkg == 1:
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype2_emib1 + 0.1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype2_emib1 + 0.1 + 0

                else: # point_pkg == 2
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype2_emib1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype2_emib1 + 0
            else: # exist_emib == 2
                temp_pkgtype2_emib2 = 0.3 + 0 * main_num
                if point_pkg == 1:
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype2_emib2 + 0.1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype2_emib2 + 0.1 + 0
                else: # point_pkg == 2
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype2_emib2 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype2_emib2 + 0

        else: # pkg_type == 3
            if exist_emib == 1:
                temp_pkgtype3_emib1 = 0.4 + 0.1 * main_num
                if point_pkg == 1:
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype3_emib1 + 0.1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype3_emib1 + 0.1 + 0

                else: # point_pkg == 2
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype3_emib1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype3_emib1 + 0

            else: # exist_emib == 2
                temp_pkgtype3_emib2 = 0.4 + 0 * main_num
                if point_pkg == 1:
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype3_emib2 + 0.1 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype3_emib2 + 0.1 + 0

                else: # point_pkg == 2
                    if exist_hbm_input_val == 1:
                        result = temp_pkgtype3_emib2 + 0.1
                    elif exist_hbm_input_val == 2:
                        result = temp_pkgtype3_emib2 + 0

        return result

    def pkgassy_finish(self, pkg_type):
        if  pkg_type == 1:
            result = 0.1
        elif pkg_type == 2:
            result = 0.2
        else: # pkg_type == 3
            result = 0.3
        return result

    def pkgassy_test(self, main_num, die_architect_input_val, type_num_satellite_input_val):
        temp = type_num_satellite_input_val * self.SATELLITE_DIE_ATTACH_YL
        if die_architect_input_val == 1:
            result = 0.25 * main_num + temp
        elif die_architect_input_val == 2:
            result = 0.5 * main_num + temp
        elif die_architect_input_val == 3 or \
             die_architect_input_val == 4 or \
             die_architect_input_val == 8:
                result = 0.2 * main_num + temp
        elif die_architect_input_val == 5:
            result = 0.4 * main_num + temp
        elif die_architect_input_val == 6:
            result = 0.1 * main_num + temp
        elif die_architect_input_val == 7:
            result = 0.15 * main_num + temp
        return result

    def pkgassy_ttl(self, pkg_type, main_num, exist_emib, point_pkg, \
                    exist_hbm_input_val, die_architect_input_val, type_num_satellite_input_val):
        return (1-(100-self.pkgassy_rtd(pkg_type, main_num, exist_emib, point_pkg, exist_hbm_input_val))/100* \
                (100-self.pkgassy_finish(pkg_type))/100* \
                (100-self.pkgassy_test(main_num, die_architect_input_val, type_num_satellite_input_val))/100)*100

    def inventory_yield(self, Die_Architecture_Info_val, is_wla, val):
        if Die_Architecture_Info_val == 6: # legacy client
            output = [99.90, 99.95, 99.95, 99.95, 99.95, 99.95]
        elif Die_Architecture_Info_val == 7: # foveros
            if is_wla == 1:
                output = [99.7, 99.8, 99.8, 99.8, 99.9, 99.9] 
            else:
                output = [99.90, 99.95,	99.95, 99.95, 99.95, 99.95]
        
        elif Die_Architecture_Info_val < 4: # emib
            output = [99.7, 99.8, 99.8, 99.8, 99.9, 99.9]
        else: # coemib
            if is_wla == 1:
                output = [99.7, 99.8, 99.8, 99.8, 99.9, 99.9]
            else:
                output = [99.7, 99.8, 99.8, 99.8, 99.9, 99.9]

        return output[val-1]
    
    def get_index(self, pkg_type, exist_emib, point_pkg, lifetime_vol_input_val, \
           wla_architect, dow_architect_input_val, odi_chiplet_size, hbi_architect, \
           exist_hbm_input_val, die_architect_input_val, architecture_maturity_val):
        
        self.pkg_type_input = self.package_type_selection.index(pkg_type) + 1
        self.exist_emib_input = self.exist_emib_selection.index(exist_emib) + 1
        self.point_pkg_input = self.exist_point_selection.index(point_pkg) + 1
        self.lifetime_vol_input = self.lifetime_vol_selection.index(lifetime_vol_input_val) + 1
        self.wla_architect_input = self.wla_architect_selection.index(wla_architect) + 1
        self.dow_architect_input = self.dow_architect_selection.index(dow_architect_input_val) + 1
        self.odi_chiplet_size_input = self.odi_size_chiplet_selection.index(odi_chiplet_size) + 1
        self.hbi_architect_input = self.hbi_architect_selection.index(hbi_architect) + 1
        self.exist_hbm_input = self.exist_hbm_selection.index(exist_hbm_input_val) + 1
        self.die_architect_input = self.die_architect_selection.index(die_architect_input_val) + 1
        self.architecture_maturity_input = self.architecture_maturity_selection.index(architecture_maturity_val) + 1        


    def lrp_prediction(self, product_name, skew_name, chiplet_num, pkg_class, pkg_type, main_num, exist_emib, point_pkg, lifetime_vol_input_val, \
           wla_architect, dow_architect_input_val, odi_chiplet_size, hbi_architect, signal_area_hbi, \
           exist_hbm_input_val, die_architect_input_val, type_num_satellite_input_val, \
           architecture_maturity_val):
        
        self.get_index(pkg_type, exist_emib, point_pkg, lifetime_vol_input_val, 
           wla_architect, dow_architect_input_val, odi_chiplet_size, hbi_architect, \
           exist_hbm_input_val, die_architect_input_val, architecture_maturity_val)
        
        wla_ssdt = self.wla_ssdt(self.wla_architect_input, float(chiplet_num), self.dow_architect_input, \
        self.odi_chiplet_size_input, self.hbi_architect_input, float(signal_area_hbi))
        wla_rtd = self.wla_rtd(float(chiplet_num), self.wla_architect_input)
        pkgassy_rtd = self.pkgassy_rtd(self.pkg_type_input, float(main_num), self.exist_emib_input, \
                                        self.point_pkg_input, self.exist_hbm_input)
        pkgassy_finish_rtd = self.pkgassy_finish(self.pkg_type_input)
        pkgassy_test = self.pkgassy_test(float(main_num), self.die_architect_input, float(type_num_satellite_input_val))

        if self.architecture_maturity_input == 2 or self.architecture_maturity_input == 1:
            multiplier = np.array([4, 2.5, 2, 1.5, 1, 1])
        elif self.architecture_maturity_input == 4 or self.architecture_maturity_input == 3:
            multiplier = np.array([6, 3.5, 2.5, 1.5, 1.25, 1])

        loss = pd.DataFrame(columns = ['PO/ES0', 'ES1', 'ES2', 'QS', 'PRQ', 'PRQ+1Q'])
        if self.wla_architect_input == 1:
            loss.loc[len(loss.index)] = multiplier*pkgassy_rtd
            loss.loc[len(loss.index)] = multiplier*pkgassy_test
            loss.loc[len(loss.index)] = multiplier*pkgassy_finish_rtd
            result = loss.apply(lambda x: 100 - x)
            result.loc[len(result.index)] = [self.inventory_yield(Die_Architecture_Info_val=self.die_architect_input, is_wla=0, val=i) for i in range(1,7)]
            result.index = ["Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]

        else:
            loss.loc[len(loss.index)] = multiplier*wla_rtd
            loss.loc[len(loss.index)] = multiplier*wla_ssdt
            loss.loc[len(loss.index)] = multiplier*pkgassy_rtd
            loss.loc[len(loss.index)] = multiplier*pkgassy_test
            loss.loc[len(loss.index)] = multiplier*pkgassy_finish_rtd
            result = loss.apply(lambda x: 100 - x)
            result.loc[1.5] = [self.inventory_yield(Die_Architecture_Info_val=self.die_architect_input, is_wla=1, val=i) for i in range(1,7)]
            result.loc[len(result.index)] = [self.inventory_yield(Die_Architecture_Info_val=self.die_architect_input, is_wla=0, val=i) for i in range(1,7)]
            result = result.sort_index()
            result.columns = ['PO/ES0', 'ES1', 'ES2', 'QS', 'PRQ', 'PRQ+1Q']
            result.index = ["WLA RtD", "WLA Test PIYL", "WLA Inventory Yield", "Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]
        
        self.lrp_output['Product_Name'] = product_name
        self.lrp_output['Skew_Name'] = skew_name
        self.lrp_output['Package_Type'] = pkg_class
        self.lrp_output['Package_Type_Estimation'] = pkg_type
        self.lrp_output['Number_of_Main_Die'] = main_num
        self.lrp_output['Exist_EMIB'] = exist_emib
        self.lrp_output['Exist_POINT'] = point_pkg
        self.lrp_output['WLA_Architecture'] = wla_architect
        self.lrp_output['Number_of_Chiplet_Base_Die'] = chiplet_num
        self.lrp_output['DoW_Architecture'] = dow_architect_input_val
        self.lrp_output['ODI_Chiplet_Size'] = odi_chiplet_size
        self.lrp_output['HBI_Architecture'] = hbi_architect
        self.lrp_output['Signal_Area'] = signal_area_hbi
        self.lrp_output['Die_Architecture_Summary'] = die_architect_input_val
        self.lrp_output['Number_of_Satellite_Die'] = type_num_satellite_input_val
        self.lrp_output['Exist_HBM'] = exist_hbm_input_val
        self.lrp_output['Lifetime_Volume'] = lifetime_vol_input_val
        self.lrp_output['Architecture_Maturity'] = architecture_maturity_val

        self.lrp_output = self.format_result(result_pred = result)
        
        return result, self.lrp_output
    
    def format_result(self, result_pred):
        for idx, row in result_pred.iterrows():
            for i in range(len(result_pred.columns)):
                milestone_idx = idx + ';' + row.index[i]
                val = row.values[i]
                self.lrp_output[milestone_idx] = "{:.2f}".format(round(val, 2))

        return self.lrp_output


class Manual_Entry_Model:

    def __init__(self):
        self.Die_Architecture_Info_selection = ['Legacy Client','Foveros Client', 'EMIB', 'Co-EMIB']
        self.WLA_Maturity_selection = ['Evolutionary','Revolutionary']
        self.Pkg_Assemb_Maturity_selection = ['Evolutionary','Revolutionary']
        
        self.lrp_output = {}

    def multiplier(self, PRQ, maturity, val): 
        evol_multiplier = [4, 2.5, 2, 1.5, 1, 1]
        rev_multiplier = [6, 3.5, 2.5, 1.5, 1.25, 1]
        if maturity == 1:
            output = 100 - ((100-PRQ)*evol_multiplier[val-1])
        else:
            output = 100 - ((100-PRQ)*rev_multiplier[val-1])

        return output

    def inventory_yield(self, Die_Architecture_Info_val, is_WLA, val):
        if Die_Architecture_Info_val == 1:
            output = [99.90, 99.95, 99.95, 99.95, 99.95, 99.95]
        elif Die_Architecture_Info_val == 2:
            if is_WLA == 0:
                output = [99.7, 99.8, 99.8, 99.8, 99.9, 99.9]
            else:
                output = [99.90, 99.95,	99.95, 99.95, 99.95, 99.95]
        
        elif Die_Architecture_Info_val == 3:
            output = [99.7, 99.8, 99.8, 99.8, 99.9, 99.9]
        else:
            if is_WLA == 0:
                output = [99.7, 99.8, 99.8, 99.8, 99.9, 99.9]
            else:
                output = [99.7, 99.8, 99.8, 99.8, 99.9, 99.9]

        return output[val-1]

    def get_index(self,  Die_Architecture_Info_val, WLA_Maturity, Pkg_Assemb_Maturity):
        
        self.Die_Architecture_Info_val = self.Die_Architecture_Info_selection.index(Die_Architecture_Info_val) + 1
        if WLA_Maturity != None:
            self.WLA_Maturity = self.WLA_Maturity_selection.index(WLA_Maturity) + 1
        self.Pkg_Assemb_Maturity = self.Pkg_Assemb_Maturity_selection.index(Pkg_Assemb_Maturity) + 1


    def lrp_prediction(self, product_name, skew_name, pkg_class, Die_Architecture_Info_val, WLA_Maturity, Pkg_Assemb_Maturity,
                                     PRQ_WLA_RtD, PRQ_WLA_Test_PIYL, PRQ_Pkg_Assemb_RtD,
                                     PRQ_Pkg_Test_PIYL, PRQ_Pkg_Assemb_Finish):
        
        self.get_index(Die_Architecture_Info_val, WLA_Maturity, Pkg_Assemb_Maturity)
        
        if (self.Die_Architecture_Info_val==2) or (self.Die_Architecture_Info_val == 4):
            Milestone = ["WLA RtD", "WLA Test PIYL", "WLA Inventory Yield", "Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]
            PO = [self.multiplier(PRQ_WLA_RtD, self.WLA_Maturity, 1), self.multiplier(PRQ_WLA_Test_PIYL, self.WLA_Maturity, 1), self.inventory_yield(self.Die_Architecture_Info_val, 1, 1), self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 1), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 1), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 1), self.inventory_yield(self.Die_Architecture_Info_val, 0, 1)]
            ES1 = [self.multiplier(PRQ_WLA_RtD, self.WLA_Maturity, 2), self.multiplier(PRQ_WLA_Test_PIYL, self.WLA_Maturity, 2), self.inventory_yield(self.Die_Architecture_Info_val, 1, 2), self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 2), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 2), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 2), self.inventory_yield(self.Die_Architecture_Info_val, 0, 2)]
            ES2 = [self.multiplier(PRQ_WLA_RtD, self.WLA_Maturity, 3), self.multiplier(PRQ_WLA_Test_PIYL, self.WLA_Maturity, 3), self.inventory_yield(self.Die_Architecture_Info_val, 1, 3), self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 3), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 3), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 3), self.inventory_yield(self.Die_Architecture_Info_val, 0, 3)]
            QS = [self.multiplier(PRQ_WLA_RtD, self.WLA_Maturity, 4), self.multiplier(PRQ_WLA_Test_PIYL, self.WLA_Maturity, 4), self.inventory_yield(self.Die_Architecture_Info_val, 1, 4), self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 4), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 4), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 4), self.inventory_yield(self.Die_Architecture_Info_val, 0, 4)]
            PRQ = [self.multiplier(PRQ_WLA_RtD, self.WLA_Maturity, 5), self.multiplier(PRQ_WLA_Test_PIYL, self.WLA_Maturity, 5), self.inventory_yield(self.Die_Architecture_Info_val, 1, 5), self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 5), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 5), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 5), self.inventory_yield(self.Die_Architecture_Info_val, 0, 5)]
            PRQ_1Q = [self.multiplier(PRQ_WLA_RtD, self.WLA_Maturity, 6), self.multiplier(PRQ_WLA_Test_PIYL, self.WLA_Maturity, 6), self.inventory_yield(self.Die_Architecture_Info_val, 1, 6), self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 6), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 6), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 6), self.inventory_yield(self.Die_Architecture_Info_val, 0, 6)]
        else:
            Milestone = ["Pkg Assemb RtD", "Pkg Assemb Test PIYL", "Pkg Assemb Finish", "Pkg Assemb Inventory Yield"]
            PO = [self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 1), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 1), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 1), self.inventory_yield(self.Die_Architecture_Info_val, 0, 1)]
            ES1 = [self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 2), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 2), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 2), self.inventory_yield(self.Die_Architecture_Info_val, 0, 2)]
            ES2 = [self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 3), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 3), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 3), self.inventory_yield(self.Die_Architecture_Info_val, 0, 3)]
            QS = [self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 4), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 4), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 4), self.inventory_yield(self.Die_Architecture_Info_val, 0, 4)]
            PRQ = [self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 5), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 5), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 5), self.inventory_yield(self.Die_Architecture_Info_val, 0, 5)]
            PRQ_1Q = [self.multiplier(PRQ_Pkg_Assemb_RtD, self.Pkg_Assemb_Maturity, 6), self.multiplier(PRQ_Pkg_Test_PIYL, self.Pkg_Assemb_Maturity, 6), self.multiplier(PRQ_Pkg_Assemb_Finish, self.Pkg_Assemb_Maturity, 6), self.inventory_yield(self.Die_Architecture_Info_val, 0, 6)]
        
        output_dict = {'Milestone': Milestone, 'PO/ES0': PO, 'ES1': ES1, 'ES2': ES2, 'QS': QS, 'PRQ': PRQ, 'PRQ+1Q': PRQ_1Q}
        result = pd.DataFrame(output_dict, columns=['Milestone', 'PO/ES0', 'ES1', 'ES2', 'QS', 'PRQ', 'PRQ+1Q'])
        result = result.set_index('Milestone')

        self.lrp_output['Product_Name'] = product_name
        self.lrp_output['Skew_Name'] = skew_name
        self.lrp_output['Package_Type'] = pkg_class
        self.lrp_output['Die_Architecture'] = Die_Architecture_Info_val
        self.lrp_output['WLA_Architecture_Maturity'] = WLA_Maturity
        self.lrp_output['Pkg_Assembly_Architecture_Maturity'] = Pkg_Assemb_Maturity

        self.lrp_output = self.format_result(result_pred = result)
        
        return result, self.lrp_output
        
    def format_result(self, result_pred):
        for idx, row in result_pred.iterrows():
            for i in range(len(result_pred.columns)):
                milestone_idx = idx + ';' + row.index[i]
                val = row.values[i]
                if val is None:
                    val = ''
                self.lrp_output[milestone_idx] = "{:.2f}".format(round(val, 2))

        return self.lrp_output
        
