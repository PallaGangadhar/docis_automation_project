from utlity import send_req
import requests
import texttable as tt
from db import update_regression_summary_path, db_connection, get_resgression_id, get_resgression_id_by_log_id, get_tab_info
import os
from datetime import datetime
from flask import request
from utlity import table_summary


tab = tt.Texttable()
row=None
l=[]

directory = "Logs"
parent_dir = "C:\\Users\\GANGADHAR PALLA\\Documents\\CMTS_Automation_Project\\CMTS_New_UI_dev\\static"
path = os.path.join(parent_dir, directory)

def get_query_string():
    query_string = request.url.split('?')[1]
    return query_string

def create_dir():
    try:
        if not os.path.isdir('Logs'):
            os.mkdir(path)
    except:
        pass

create_dir()
def create_regression_folder():
    directory = "Logs"
    parent_dir = "C:\\Users\\GANGADHAR PALLA\\Documents\\CMTS_Automation_Project\\CMTS_New_UI_dev\\static"
    path = os.path.join(parent_dir, directory)
    curr, conn=db_connection()
    curr.execute(f"select regression_name,date_added from regression order by regression_id desc limit 1")
    data = curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    regression_name = data[0].replace(' ','_')
    date_time = data[1]
    dt_obj = date_time
    dt_obj = date_time.replace(microsecond=0)
    formatted_date = dt_obj.strftime("%Y-%m-%d_%H-%M-%S")
    path=f"{path}\\{regression_name}_{formatted_date}"
    if not os.path.isdir(path):
        os.mkdir(path)
    # os.makedirs(new_path, exist_ok=True)
    return path

def test1():
    new_path = create_regression_folder()
    start_create = open(f"{new_path}/file1.txt", "w")
    start_create.write("Hi" + '\n')
    start_create.close()


def test2():
    new_path = create_regression_folder()
    start_create = open(f"{new_path}/file2.txt", "w")
    start_create.write("Hello" + '\n')
    start_create.close()




def TC_1(**kwargs):
    print("kwargs yes === ", kwargs)
    tc_id = kwargs.get('tc_id')
    log_id = kwargs.get('log_id', None)
    total_rerun_count = kwargs.get('total_rerun_tc',0)
    random_string = kwargs.get('random_string',None)
    print("Arris TC 1 ====>", tc_id, log_id, total_rerun_count, random_string)
    
    # print("Arris TC 1 ====>", total_rerun_count)
    # send_req("\n\n########### Test Case 1 #################\n\n")
    output = """
 PRIM    1ST TIME     TIMES  %                             ONLINE TIME                  OFFLINE TIME
 SID     ONLINE       ONLINE  ONLINE  MIN         AVG         MAX         MIN         AVG         MAX
 ------  -----------  ------  ------  ----------  ----------  ----------  ----------  ----------  ----------
Md17:0/0.0
      1  Apr 18 2024       2  100     0d0h0m      2d10h6m     4d20h12m    0d0h0m      0d0h0m      0d0h0m 
     TestStep:FAIL
    """
    if log_id is None:
        query_string = get_tab_info(random_string)
    kwargs_data = {
        'output': output,
        'random_string': random_string
    }
    send_req(**kwargs_data)
    # kwargs_data = {
    #     'output': output,
    #     'random_string': random_string
    # }
    # send_req({'output':f'##Test Case Number: {test_case_number}##', 'random_string': random_string})

    # tab.add_row(['Ottmar Hitzfeld', 'Borussia Dortmund, Bayern Munich','1997 and 2001'])
    # tab.add_row(['Ottmar Hitzfeld', 'Borussia Dortmund, Bayern Munich','1997 and 2001'])

    # send_req("\n\n########### Executed command: show clock #################\n\n")

    # # for i in output.splitlines():
    # #     print(i)
    # send_req(output)

    # send_req("====== TABLE ====================")
    
    # send_req("TestStep:Pass")
    # query_string = get_query_string()
    table_summary("FAIL","N/A","5.5 seconds","a.txt",tc_id, log_id, random_string)
    requests.post("http://localhost:5000/charts", json={"pass":0, "fail":1,'query_string':random_string,'log_id':log_id, 'total_rerun_count':total_rerun_count},headers = {'Content-type': 'application/json'})
    # eval(result_summary("' + reg_id + '", "'+random_string+'")')

def TC_2(**kwargs):
    tc_id = kwargs.get('tc_id')
    log_id = kwargs.get('log_id')
    total_rerun_count = kwargs.get('total_rerun_tc')
    random_string = kwargs.get('random_string')
    output = """ 
  ASD-GT0003-CCAP001# 
  TC 2 called
    Fine!!!!
    Fine!!!!
    Fine!!!!
    Fine!!!!

    Fine!!!!
    Fine!!!!
    TestStep:FAIL
    """
    # query_string = get_tab_info(random_string)
    kwargs_data = {
        'output': output,
        'random_string': random_string
    }
    send_req(**kwargs_data)
    # row = ['Ernst Happel', 'Feyenoord, Hamburg', '1970 and 1983']
    # tab.add_row(['Ernst Happel', 'Feyenoord, Hamburg', '1970 and 1983'])

    # send_req("\n\n########### Test Case 2 #################\n\n")
    # send_req(output)
    # # testcase_number, testcase_name, testcase_reference = get_regressions_logs_testcase_details(tc_id)
    # query_string = get_query_string()
    # print("Arris query string ==", query_string)
    table_summary("FAIL","N/A","5.5 seconds","a.txt",tc_id, log_id, random_string)
    requests.post("http://localhost:5000/charts", json={"pass": 0, "fail":1,'query_string':random_string,'log_id':log_id, 'total_rerun_count':total_rerun_count},headers = {'Content-type': 'application/json'})

def TC_3(**kwargs):
    tc_id = kwargs.get('tc_id')
    log_id = kwargs.get('log_id')
    total_rerun_count = kwargs.get('total_rerun_tc')
    random_string = kwargs.get('random_string')
    output = """ Hello GPA........
        show clock 
        show clock 
    """
    query_string = get_tab_info(random_string)
    kwargs_data = {
        'output': output,
        'random_string': random_string
    }
    send_req(**kwargs_data)

    # row = ['Jose Mourinho', 'Porto, Inter Milan', '2004 and 2010']
    # tab.add_row(['Jose Mourinho', 'Porto, Inter Milan', '2004 and 2010'])
    # print(output)
    # send_req("\n\n########### Test Case 3 #################\n\n")
    # send_req(output)
    # send_req("Teststep:Fail")
    # query_string = get_query_string()
    # print("Arris query string ==", query_string)
    table_summary("FAIL","N/A","5.5 seconds","a.txt",tc_id, log_id, random_string)
    requests.post("http://localhost:5000/charts", json={"pass":0, "fail":1,'query_string':random_string,'log_id':log_id, 'total_rerun_count':total_rerun_count},headers = {'Content-type': 'application/json'})
    
def TC_4(**kwargs):
    tc_id = kwargs.get('tc_id')
    log_id = kwargs.get('log_id')
    total_rerun_count = kwargs.get('total_rerun_tc')
    random_string = kwargs.get('random_string')
    
    output = """ 
        Hello Arjun........
        show clock 
        show clock 
        show clock 
        none of the above
        none of the above
        none of the above
        none of the above
        none of the above
        TestStep:PASS
    """

    # tab.add_row(['Gangadhar', 'Gpalla, Inter Milan', '000 and 000'])
    # print(output)
    # send_req("\n\n########### Test Case 4 #################\n\n")
    kwargs_data = {
        'output': output,
        'random_string': random_string
    }
    # send_req(**kwargs_data)
    send_req(**kwargs_data)
    # query_string = get_tab_info(random_string)
    
    table_summary("PASS","N/A","5.5 seconds","a.txt",tc_id, log_id, random_string)
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0,'query_string':random_string,'log_id':log_id, 'total_rerun_count':total_rerun_count},headers = {'Content-type': 'application/json'})


def RPD_call_after_execution():
    print("=======Parallel_RPD_call_after_execution=====")
    query_string = get_query_string()
    r_id = get_resgression_id(query_string)
    curr, conn=db_connection()
    curr.execute(f"select regression_name, regression_id from regression where regression_id={r_id}")
    data = curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    regression_name = data[0].replace(' ','_')
    regression_id = str(data[1])
    print("regression_name[0] ===", data[1])
    current_datetime = datetime.now()
    datetime_string = current_datetime.strftime("%Y-%m-%d %H-%M-%S")
    print("Current Date and Time:", datetime_string.replace(' ','_'))
    folder_name=f"static\\files\\{regression_name}_{datetime_string}"
    folder_name=f"static\\files\\{regression_name}_{regression_id}"
    print(f"Folder name=== {folder_name}")
    os.makedirs(folder_name, exist_ok=True)
    file = open(f"{folder_name}\\abc.txt", "w")
    file.truncate(0)
    file.write("\n********** SUMMARY **********")
    print(tab.draw())
    file.write(tab.draw())
    update_regression_summary_path(r_id,"abc.txt")
    tab.reset()
    file.close()
    # pass
    
