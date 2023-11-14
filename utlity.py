import requests
import time
import secrets

def send_req(message):
    # time.sleep(0.3)
    requests.post("http://localhost:5000/connect", json={"data": message},headers = {'Content-type': 'application/json'})
    
def generate_key():
    ''' genearate key '''
    return secrets.token_hex(6)


def genearate_list_of_dict(r_dates,type_dates,graph_data):
    new_list=[]
    for r_date in r_dates:
        if r_date not in type_dates:
            graph_data.append({'date':r_date,'count':0}) 
    graph_data.sort(key = lambda x:x['date'],reverse=True)
    [new_list.append(i) for i in graph_data]
    return new_list

# import re
# output="D:\Ganga\Arjun_Project\static\\files\\abc.txt"
# pat=re.search("[a-zA-z0-9]+[.]txt$", output)
# print(pat.group(0))