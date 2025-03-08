import requests
import secrets
import datetime
from flask import request
from db import db_connection

per_page = 5

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

def filter_regression(cmts_type,search_reg,query):
    params = []
    # Apply Filters
    if cmts_type:
        query += " AND cmts_type = %s"
        params.append(cmts_type)

    if search_reg:
        query += " AND LOWER(regression_name) LIKE LOWER(%s)"
        params.append(f"%{search_reg}%")
    return query, params

def filter_testcase(tc_name,module_type,device_type,query):
    params = []
    # Apply Filters
    if tc_name:
        query += " AND LOWER(testcase_name) LIKE LOWER(%s)"
        params.append(f"%{tc_name}%")

    if device_type:
        query += " AND devices_details.device_id = %s"
        params.append(device_type)

    if module_type:
        query += " AND modules_details.modules_id = %s"
        params.append(module_type)
    return query, params

def filter_devices(search_device,query):
    params = []
    # Apply Filters
    if search_device:
        query += " AND LOWER(device_name) LIKE LOWER(%s)"
        params.append(f"%{search_device}%")
    return query, params

def filter_modules(search_module, device_type,query):
    params = []
    # Apply Filters
    if device_type:
        query += " AND devices_details.device_id= %s"
        params.append(device_type)

    if search_module:
        query += " AND LOWER(module_name) LIKE LOWER(%s)"
        params.append(f"%{search_module}%")
    return query, params

def get_offset_details(**kwargs):
    curr, conn = db_connection()
    # Base Query
    table_name = kwargs.get('table_name')
    offset =  kwargs.get('offset')
    per_page = kwargs.get('per_page')
    order_by_field = None
    query = f"SELECT * FROM {table_name} WHERE 1=1"

    if table_name == "regression":
        cmts_type = kwargs.get('cmts_type')
        search_reg = kwargs.get('search_reg')
        query, params = filter_regression(cmts_type, search_reg, query)
        order_by_field = "date_added"
    
    elif table_name == "testcase_details":
        tc_name = kwargs.get('tc_name')
        module_type = kwargs.get('module_type')
        device_type = kwargs.get('device_type')
        query = f"SELECT {table_name}.*,modules_details.module_name,devices_details.device_name\
        FROM {table_name},modules_details,devices_details where {table_name}.modules_id = \
        modules_details.modules_id and modules_details.device_id=devices_details.device_id\
         and 1=1"
        query, params = filter_testcase(tc_name,module_type,device_type,query)
        order_by_field = "testcase_id"

    elif table_name == "devices_details":
        search_device = kwargs.get('search_devices')
        query, params = filter_devices(search_device, query)
        order_by_field = "device_id"
    
    elif table_name == "modules_details":
        search_module = kwargs.get('search_module')
        device_type = kwargs.get('device_type')
        query = "SELECT devices_details.device_name,modules_id, module_name FROM public.modules_details, \
                devices_details where devices_details.device_id=modules_details.device_id and 1=1"
        query, params = filter_modules(search_module, device_type, query)
        order_by_field = "modules_id"

    query += f" ORDER BY {order_by_field} DESC LIMIT %s OFFSET %s"
    params.extend([per_page, offset])
    curr.execute(query, tuple(params))
    offset_details = curr.fetchall()
    curr.close()
    conn.close()
    return offset_details

# Function to count total regression details with filters
def get_table_total_details(**kwargs):
    curr, conn = db_connection()
    table_name = kwargs.get('table_name')
    print("Table name===", table_name)
    # Base Query
    query = f"SELECT * FROM {table_name} WHERE 1=1"
    
    if table_name == "regression":
        cmts_type = kwargs.get('cmts_type')
        search_reg = kwargs.get('search_reg')
        query, params = filter_regression(cmts_type, search_reg,query)
    
    elif table_name == "testcase_details":
        tc_name = kwargs.get('tc_name')
        module_type = kwargs.get('module_type')
        device_type = kwargs.get('device_type')
        query = f"SELECT {table_name}.*,modules_details.module_name,devices_details.device_name\
        FROM {table_name},modules_details,devices_details where {table_name}.modules_id = \
        modules_details.modules_id and modules_details.device_id=devices_details.device_id"
        query, params = filter_testcase(tc_name, module_type, device_type, query)
        
    elif table_name == "devices_details":
        search_device = kwargs.get('search_devices')
        query, params = filter_devices(search_device, query)

    elif table_name == "modules_details":
        search_module = kwargs.get('search_module')
        device_type = kwargs.get('device_type')
        query = "SELECT devices_details.device_name,modules_id, module_name FROM public.modules_details, \
                devices_details where devices_details.device_id=modules_details.device_id "
        query, params = filter_modules(search_module, device_type, query)
        print("Query===", query)

    curr.execute(query, tuple(params))
    total = len(curr.fetchall())
    curr.close()
    conn.close()
    return total
