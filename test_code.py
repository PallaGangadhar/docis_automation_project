from utlis import send_req
import requests
import texttable as tt
from db import update_regression_summary_path

tab = tt.Texttable()
row=None
l=[]

def table_summary(tc_no,tc_name,status,fail_in,execution_time,tc_logs_path):
    r=requests.post("http://localhost:5000/add_regression_logs", json={"tc_no":tc_no,"testcase_name":tc_name, "status":status,'fail_in':fail_in,'execution_time':execution_time,'tc_logs_path':tc_logs_path},headers = {'Content-type': 'application/json'})
    print(r.status_code)

def TC_1():
    print("\n\nTC_1 Called===")
    output = """ASD-GT0003-CCAP001# show clock 

    """
    tab.add_row(['Ottmar Hitzfeld', 'Borussia Dortmund, Bayern Munich','1997 and 2001'])

    send_req("\n\n########### Executed command: show clock #################\n\n")

    for i in output.splitlines():
        # print(i)
        send_req(i)

    send_req("====== TABLE ====================")
    
    send_req("TestStep:Pass")
    table_summary("1","TC 1","FAiL","N/A","12 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":0, "fail":1},headers = {'Content-type': 'application/json'})

def TC_2():
    print("\n\nTC_2 Called===")
    output = """ 
  ASD-GT0003-CCAP001# show clock 
    2023 June 1 07:00:46 
    """
    # row = ['Ernst Happel', 'Feyenoord, Hamburg', '1970 and 1983']
    tab.add_row(['Ernst Happel', 'Feyenoord, Hamburg', '1970 and 1983'])

    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
    table_summary("2","TC 2","PASS","N/A","5 seconds","a.txt")
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
    table_summary("3","TC 3","PASS","N/A","6 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0},headers = {'Content-type': 'application/json'})
    
def TC_4():
    
    output = """ 
        Hello Arjun........
        show clock 

    
    """
    tab.add_row(['Gangadhar', 'Gpalla, Inter Milan', '000 and 000'])

    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
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
        Hello Arjun........
        ASD-GT0003-CCAP001# 
    show clock 
    
    """
    tab.add_row(['Gangadhar', 'Gpalla, Inter Milan', '000 and 000'])

    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
    table_summary("6","Tc 6","PASS","N/A","1 seconds","a.txt")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0},headers = {'Content-type': 'application/json'})



def call_after_execution(r_id):
    file = open("static\\files\\abc.txt", "w")
    file.truncate(0)
    file.write("\n********** SUMMARY **********")
    print(tab.draw())
    file.write(tab.draw())
    update_regression_summary_path(r_id,"abc.txt")
    tab.reset()
    file.close()

