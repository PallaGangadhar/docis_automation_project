import requests
import time
import secrets
import datetime
from flask import request

def send_req(message):
    query_string = request.url.split('?')[1]
    requests.post("http://localhost:5000/send_message", json={"data": message, 'query_string':query_string},headers = {'Content-type': 'application/json'})
    
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


def convert_str_to_date(date,d_format):
    datetime_str = datetime.datetime.strptime(date, d_format)
    return datetime_str

def convert_date_to_str(date,d_format):
    return date.strftime(d_format)
   