from utlity import send_req
import requests
import texttable as tt
from db import update_regression_summary_path, db_connection
import os
from datetime import datetime

tab = tt.Texttable()
row=None
l=[]

directory = "Logs"
parent_dir = "C:\\Users\\GANGADHAR PALLA\\Documents\\CMTS_Automation_Project\\CMTS_New_UI_dev\\static"
path = os.path.join(parent_dir, directory)

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



def table_summary(tc_no,tc_name,status,fail_in,execution_time,tc_logs_path):
    r=requests.post("http://localhost:5000/add_regression_logs", json={"tc_no":tc_no,"testcase_name":tc_name, "status":status,'fail_in':fail_in,'execution_time':execution_time,'tc_logs_path':tc_logs_path},headers = {'Content-type': 'application/json'})
    print(r.status_code)

def TC_1():
    test1()
    test2()
    print("\n\nTC_1 Called===")
    send_req("\n\n########### Test Case 2 #################\n\n")
    output = """
 PRIM    1ST TIME     TIMES  %                             ONLINE TIME                  OFFLINE TIME
 SID     ONLINE       ONLINE  ONLINE  MIN         AVG         MAX         MIN         AVG         MAX
 ------  -----------  ------  ------  ----------  ----------  ----------  ----------  ----------  ----------
Md17:0/0.0
      1  Apr 18 2024       2  100     0d0h0m      2d10h6m     4d20h12m    0d0h0m      0d0h0m      0d0h0m    
      8  Apr 18 2024       1  100     0d0h0m      8d18h54m    8d18h54m    0d0h0m      0d0h0m      0d0h0m    
      2  Apr 18 2024       5  100     0d0h0m      0d19h57m    4d3h49m     0d0h0m      0d0h0m      0d0h0m    
      7  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      6  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      3  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      4  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      5  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
Md62:0/0.0
     41  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     37  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     63  Apr 24 2024       1  100     0d0h0m      2d22h20m    2d22h20m    0d0h0m      0d0h0m      0d0h0m    
     61  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     52  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     58  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     51  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     59  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     36  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     46  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     38  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     44  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     34  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     57  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     56  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     50  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     54  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     49  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     48  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     55  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     60  Apr 24 2024       1  100     0d0h0m      2d22h26m    2d22h26m    0d0h0m      0d0h0m      0d0h0m    
     53  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     35  Apr 24 2024       2  100     0d0h0m      0d9h44m     0d19h28m    0d0h0m      0d0h0m      0d0h0m    
     40  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     39  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     42  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     62  Apr 24 2024       1  100     0d0h0m      2d22h23m    2d22h23m    0d0h0m      0d0h0m      0d0h0m    
     43  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     45  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     47  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
 ===========================================================================================================
 PRIM    1ST TIME     TIMES  %                             ONLINE TIME                  OFFLINE TIME
 SID     ONLINE       ONLINE  ONLINE  MIN         AVG         MAX         MIN         AVG         MAX
 ------  -----------  ------  ------  ----------  ----------  ----------  ----------  ----------  ----------
Md17:0/0.0
      1  Apr 18 2024       2  100     0d0h0m      2d10h6m     4d20h12m    0d0h0m      0d0h0m      0d0h0m    
      8  Apr 18 2024       1  100     0d0h0m      8d18h54m    8d18h54m    0d0h0m      0d0h0m      0d0h0m    
      2  Apr 18 2024       5  100     0d0h0m      0d19h57m    4d3h49m     0d0h0m      0d0h0m      0d0h0m    
      7  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      6  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      3  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      4  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      5  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
Md62:0/0.0
     41  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     37  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     63  Apr 24 2024       1  100     0d0h0m      2d22h20m    2d22h20m    0d0h0m      0d0h0m      0d0h0m    
     61  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     52  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     58  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     51  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     59  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     36  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     46  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     38  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     44  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     34  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     57  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     56  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     50  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     54  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     49  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     48  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     PRIM    1ST TIME     TIMES  %                             ONLINE TIME                  OFFLINE TIME
 SID     ONLINE       ONLINE  ONLINE  MIN         AVG         MAX         MIN         AVG         MAX
 ------  -----------  ------  ------  ----------  ----------  ----------  ----------  ----------  ----------
Md17:0/0.0
      1  Apr 18 2024       2  100     0d0h0m      2d10h6m     4d20h12m    0d0h0m      0d0h0m      0d0h0m    
      8  Apr 18 2024       1  100     0d0h0m      8d18h54m    8d18h54m    0d0h0m      0d0h0m      0d0h0m    
      2  Apr 18 2024       5  100     0d0h0m      0d19h57m    4d3h49m     0d0h0m      0d0h0m      0d0h0m    
      7  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      6  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      3  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      4  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      5  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
Md62:0/0.0
     41  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     37  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     63  Apr 24 2024       1  100     0d0h0m      2d22h20m    2d22h20m    0d0h0m      0d0h0m      0d0h0m    
     61  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     52  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     58  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     51  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     59  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     36  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     46  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     38  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     44  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     34  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     57  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     56  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     50  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     54  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     49  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     48  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     55  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     60  Apr 24 2024       1  100     0d0h0m      2d22h26m    2d22h26m    0d0h0m      0d0h0m      0d0h0m    
     53  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     35  Apr 24 2024       2  100     0d0h0m      0d9h44m     0d19h28m    0d0h0m      0d0h0m      0d0h0m    
     40  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     39  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     42  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     62  Apr 24 2024       1  100     0d0h0m      2d22h23m    2d22h23m    0d0h0m      0d0h0m      0d0h0m    
     43  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     45  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     47  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
 ===========================================================================================================
 PRIM    1ST TIME     TIMES  %                             ONLINE TIME                  OFFLINE TIME
 SID     ONLINE       ONLINE  ONLINE  MIN         AVG         MAX         MIN         AVG         MAX
 ------  -----------  ------  ------  ----------  ----------  ----------  ----------  ----------  ----------
Md17:0/0.0
      1  Apr 18 2024       2  100     0d0h0m      2d10h6m     4d20h12m    0d0h0m      0d0h0m      0d0h0m    
      8  Apr 18 2024       1  100     0d0h0m      8d18h54m    8d18h54m    0d0h0m      0d0h0m      0d0h0m    
      2  Apr 18 2024       5  100     0d0h0m      0d19h57m    4d3h49m     0d0h0m      0d0h0m      0d0h0m    
      7  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      6  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      3  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      4  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      5  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
Md62:0/0.0
     41  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     37  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     63  Apr 24 2024       1  100     0d0h0m      2d22h20m    2d22h20m    0d0h0m      0d0h0m      0d0h0m    
     61  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     52  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     58  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     51  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     59  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     36  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     46  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     38  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     44  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     34  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     57  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     56  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     50  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     54  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     49  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     48  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     55  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     60  Apr 24 2024       1  100     0d0h0m      2d22h26m    2d22h26m    0d0h0m      0d0h0m      0d0h0m    
     53  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     35  Apr 24 2024       2  100     0d0h0m      0d9h44m     0d19h28m    0d0h0m      0d0h0m      0d0h0m    
     40  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     39  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     42  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     62  Apr 24 2024       1  100     0d0h0m      2d22h23m    2d22h23m    0d0h0m      0d0h0m      0d0h0m    
     43  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     45  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     47  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
 ===========================================================================================================
 PRIM    1ST TIME     TIMES  %                             ONLINE TIME                  OFFLINE TIME
 SID     ONLINE       ONLINE  ONLINE  MIN         AVG         MAX         MIN         AVG         MAX
 ------  -----------  ------  ------  ----------  ----------  ----------  ----------  ----------  ----------
Md17:0/0.0
      1  Apr 18 2024       2  100     0d0h0m      2d10h6m     4d20h12m    0d0h0m      0d0h0m      0d0h0m    
      8  Apr 18 2024       1  100     0d0h0m      8d18h54m    8d18h54m    0d0h0m      0d0h0m      0d0h0m    
      2  Apr 18 2024       5  100     0d0h0m      0d19h57m    4d3h49m     0d0h0m      0d0h0m      0d0h0m    
      7  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      6  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      3  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      4  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
      5  Apr 18 2024       1  100     0d0h0m      8d18h53m    8d18h53m    0d0h0m      0d0h0m      0d0h0m    
Md62:0/0.0
     41  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     37  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     63  Apr 24 2024       1  100     0d0h0m      2d22h20m    2d22h20m    0d0h0m      0d0h0m      0d0h0m    
     61  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     52  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     58  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     51  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     59  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     36  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     46  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     38  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     44  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     34  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     57  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     56  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     50  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     54  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     49  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     48  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     55  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     60  Apr 24 2024       1  100     0d0h0m      2d22h26m    2d22h26m    0d0h0m      0d0h0m      0d0h0m    
     53  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     35  Apr 24 2024       2  100     0d0h0m      0d9h44m     0d19h28m    0d0h0m      0d0h0m      0d0h0m    
     40  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     39  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     42  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     62  Apr 24 2024       1  100     0d0h0m      2d22h23m    2d22h23m    0d0h0m      0d0h0m      0d0h0m    
     43  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     45  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     47  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
 ===========================================================================================================
     55  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
     60  Apr 24 2024       1  100     0d0h0m      2d22h26m    2d22h26m    0d0h0m      0d0h0m      0d0h0m    
     53  Apr 24 2024       1  100     0d0h0m      2d22h27m    2d22h27m    0d0h0m      0d0h0m      0d0h0m    
     35  Apr 24 2024       2  100     0d0h0m      0d9h44m     0d19h28m    0d0h0m      0d0h0m      0d0h0m    
     40  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     39  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     42  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     62  Apr 24 2024       1  100     0d0h0m      2d22h23m    2d22h23m    0d0h0m      0d0h0m      0d0h0m    
     43  Apr 24 2024       1  100     0d0h0m      2d22h30m    2d22h30m    0d0h0m      0d0h0m      0d0h0m    
     45  Apr 24 2024       1  100     0d0h0m      2d22h29m    2d22h29m    0d0h0m      0d0h0m      0d0h0m    
     47  Apr 24 2024       1  100     0d0h0m      2d22h28m    2d22h28m    0d0h0m      0d0h0m      0d0h0m    
 ==========================================================================================================="""
    # tab.add_row(['Ottmar Hitzfeld', 'Borussia Dortmund, Bayern Munich','1997 and 2001'])
    tab.add_row(['Ottmar Hitzfeld', 'Borussia Dortmund, Bayern Munich','1997 and 2001'])

    send_req("\n\n########### Executed command: show clock #################\n\n")

    # for i in output.splitlines():
    #     print(i)
    send_req(output)

    send_req("====== TABLE ====================")
    
    send_req("TestStep:Pass")
    table_summary("001","TC 1","FAiL","N/A","12.5 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0},headers = {'Content-type': 'application/json'})

def TC_2():
    print("\n\nTC_2 Called===")
    output = """ 
  ASD-GT0003-CCAP001# TC 2 called
    Fine!!!!
    """
    # row = ['Ernst Happel', 'Feyenoord, Hamburg', '1970 and 1983']
    tab.add_row(['Ernst Happel', 'Feyenoord, Hamburg', '1970 and 1983'])

    send_req("\n\n########### Test Case 2 #################\n\n")
    send_req(output)
    table_summary("012","TC 2","PASS","N/A","5.5 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0},headers = {'Content-type': 'application/json'})

def TC_3():
    
    output = """ 
        Hello GPA........
        show clock 

    """
    # row = ['Jose Mourinho', 'Porto, Inter Milan', '2004 and 2010']
    tab.add_row(['Jose Mourinho', 'Porto, Inter Milan', '2004 and 2010'])
    
    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
    send_req("Teststep:Fail")
    table_summary("03_022","TC 3","PASS","N/A","6 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0},headers = {'Content-type': 'application/json'})
    
def TC_4():
    
    output = """ 
        Hello Arjun........
        show clock 

    
    """
    tab.add_row(['Gangadhar', 'Gpalla, Inter Milan', '000 and 000'])

    send_req("\n\n########### Test Case 2 #################\n\n")
    send_req(output)
    table_summary("4","Tc 4","PASS","N/A","1 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0},headers = {'Content-type': 'application/json'})

def TC_5():
    
    output = """ 
        Hello Arjun........
    """
    tab.add_row(['Gangadhar', 'Gpalla, Inter Milan', '000 and 000'])

    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
    table_summary("5","TC 5","PASS","N/A","1 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0},headers = {'Content-type': 'application/json'})

def TC_6():
    
    output = """ 
        Hello Gangadhar........
        
    
    """
    tab.add_row(['Gangadhar', 'Gpalla, Inter Milan', '000 and 000'])

    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
    table_summary("6","Tc 6","PASS","N/A","1 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0},headers = {'Content-type': 'application/json'})



def call_after_execution(r_id):
    # folder_name = 
    curr, conn=db_connection()
    curr.execute(f"select regression_name, regression_id from regression where regression_id={r_id}")
    data = curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    regression_name = data[0].replace(' ','_')
    regression_id = str(data[1])
    # print("regression_name[0] ===", data[1])
    # current_datetime = datetime.now()
    # datetime_string = current_datetime.strftime("%Y-%m-%d %H-%M-%S")
    # print("Current Date and Time:", datetime_string.replace(' ','_'))
    # folder_name=f"static\\files\\{regression_name}_{datetime_string}"
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
    

