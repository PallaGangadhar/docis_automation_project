import psycopg2
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_NAME=os.environ.get('DB_NAME')
POSTGRES_USERNAME=os.environ.get('POSTGRES_USERNAME')
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOSTNAME=os.environ.get('POSTGRES_HOSTNAME')
POSTGRES_PORT=os.environ.get('POSTGRES_PORT')


def db_connection():
    conn = psycopg2.connect(f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{DB_NAME}")
    curr = conn.cursor()
    return curr, conn


def add_regression(request):
    curr, conn=db_connection()
    regression_name = request.form.get('regression_name')
    total_tc_selected = request.form.get('total_tc_selected')
    cmts_type = request.form.get('cmts_type')
    device_id = request.form.get('device_id')
    regression_string = request.form.get('random_string')
    tab = request.form.get('tab')
    r_id=0
    curr.execute('''INSERT INTO regression(regression_name, pass_count, fail_count, no_run_count, total_count,status,cmts_type,device_id, regression_string, tab_info) VALUES (%s, %s, %s, %s,%s,%s,%s,%s, %s, %s) RETURNING regression_id''',
                  (regression_name, 0, 0, 0,int(total_tc_selected),"In Progress", cmts_type,device_id,regression_string, tab))


    r_id = curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    r_id=str(r_id[0])
    return r_id
        

def update_regression(**kwargs):
    pass_tc = kwargs.get('pass_tc')
    fail_tc = kwargs.get('fail_tc')
    r_id = kwargs.get('r_id')
    log_id = kwargs.get('log_id', None)
    status = kwargs.get('status', None)
    curr, conn=db_connection()
    curr.execute(f'SELECT * FROM regression WHERE regression_id={r_id}')
    query_data=curr.fetchone()
    pass_count=query_data[3]
    fail_count=query_data[4]
    no_run_count=query_data[5]
    total_count=query_data[6]

    
    if log_id is not None:
        pass_count, fail_count, total_count,no_run = select_query_to_get_count_details(r_id)
        if status == "PASS":
            pass_count += 1
            fail_count -= 1
        else:
            pass_count -= 1
            fail_count += 1 
        curr.execute('''UPDATE regression_logs_details SET status=%s WHERE log_id=%s''',(status, log_id))
    else:
        pass_count+=pass_tc
        fail_count+=fail_tc

    curr.execute(f'UPDATE regression SET pass_count={pass_count}, fail_count={fail_count} WHERE regression_id={r_id}')
        
    if int(total_count) == int(pass_count)+int(fail_count)+int(no_run_count):
        curr.execute('''UPDATE regression SET status=%s WHERE regression_id=%s''',( "Completed", r_id))

    conn.commit()
    curr.close()
    conn.close()


def add_regression_details(response):
    try:
        r_id=response.get('r_id')
        status=response.get('status')
        fail_in=response.get('fail_in')
        execution_time=response.get('execution_time')
        tc_logs_path=response.get('tc_logs_path')
        tc_id=response.get('tc_id')
        log_id=response.get('log_id')
        status=status.upper()
        curr, conn=db_connection()
        if log_id:
            curr.execute('''UPDATE regression_logs_details SET  failed_in=%s, execution_time=%s, tc_logs_path=%s WHERE log_id=%s''',( fail_in, execution_time, tc_logs_path, log_id))
        else:
            curr.execute('''INSERT INTO regression_logs_details(regression_id,status, failed_in,execution_time,tc_logs_path, testcase_id) VALUES (%s,%s,%s,%s,%s,%s)''',(r_id, status, fail_in, execution_time, tc_logs_path, tc_id) )
        
        conn.commit()
        curr.close()
        conn.close()
    except Exception as e:
        print('Regression Logs error ====> ', e)

        
def update_regression_summary_path(r_id, file_name):
    curr, conn=db_connection()
    curr.execute('''UPDATE regression SET summary_path=%s WHERE regression_id=%s''',( str(file_name), r_id))
    conn.commit()
    curr.close()
    conn.close()
    

def select_query_to_get_count_details(reg_id):
    curr,conn=db_connection()
    curr.execute(f"SELECT * FROM regression WHERE regression_id={reg_id}")
    query_data=curr.fetchone()
    pass_count=query_data[3]
    fail_count=query_data[4]
    no_run=query_data[5]
    total_count=query_data[6]
    conn.commit()
    curr.close()
    conn.close()
    return pass_count, fail_count, total_count,no_run


def add_regression_session(session_id, regression_string):
    curr,conn=db_connection()
    curr.execute('''INSERT INTO regression_session (session_id, regression_string) VALUES (%s, %s)''', (session_id,regression_string))
    conn.commit()
    curr.close()
    conn.close()


def get_sesson_id(regression_string):
    session_id = None
    curr,conn=db_connection()
    curr.execute(f"SELECT CASE WHEN EXISTS ("+\
            "SELECT 1 "+\
            "FROM regression_session "+\
            "WHERE regression_string = %s"+\
        ") THEN 'True'"+\
        "ELSE 'False'"+\
    "END AS result;", (regression_string,))
    is_exists = curr.fetchone()[0]
    
    if is_exists == 'True':
        curr.execute("SELECT session_id FROM public.regression_session WHERE regression_string = %s", (regression_string,))
        session_id = curr.fetchone()[0]

    curr.close()
    conn.close()
    return session_id

def get_resgression_id(regression_string):
    print("Regression string === ", regression_string)
    try:
        curr,conn=db_connection()
        curr.execute("SELECT regression_id FROM public.regression WHERE regression_string = %s", (regression_string,))
        regression_id = curr.fetchone()[0]
        conn.commit()
        curr.close()
        conn.close()
        return regression_id
    except Exception as e:
        print("Session error Arris ===", e)

def get_resgression_id_by_log_id(log_id):
    curr,conn=db_connection()
    curr.execute("SELECT regression_id FROM public.regression_logs_details WHERE log_id = %s", (log_id,))
    regression_id = curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()
    return regression_id

def get_regressions_logs_testcase_details(tc_id):
    curr,conn=db_connection()
    curr.execute("SELECT  testcase_number, testcase_name, testcase_reference FROM testcase_details WHERE testcase_id = %s", (tc_id,))
    query_data = curr.fetchone()
    testcase_number = query_data[0]
    testcase_name = query_data[1]
    testcase_reference = query_data[2]
    curr.close()
    conn.close()
    return testcase_number, testcase_name, testcase_reference

def get_testcase_function(tc_id):
    curr,conn=db_connection()
    curr.execute("SELECT testcase_function FROM testcase_details  WHERE testcase_id = %s", (tc_id,))
    query_data = curr.fetchone()
    testcase_function = query_data[0]
    curr.close()
    conn.close()
    return testcase_function

def get_tab_info(random_string):
    curr,conn=db_connection()
    curr.execute("SELECT tab_info from regression WHERE regression_string = %s", (random_string,))
    query_data = curr.fetchone()
    if query_data is None:
        tab_info = None
    else:
        tab_info = query_data[0]
    
    curr.close()
    conn.close()
    return tab_info

def get_regression_random_string(r_id):
    curr,conn=db_connection()
    curr.execute("SELECT regression_string from regression WHERE regression_id = %s", (r_id,))
    query_data = curr.fetchone()
    regression_string = query_data[11]
    curr.close()
    conn.close()
    return regression_string     


def get_tc_executed_count(rid):
    curr, conn = db_connection()
    curr.execute(f"SELECT count(log_id) FROM public.regression_logs_details where regression_id = {rid};")
    query_data = curr.fetchone()
    curr.close()
    conn.close()
    return query_data[0]

def get_executed_tc_status(log_id):
    curr, conn = db_connection()
    curr.execute(f"SELECT status FROM public.regression_logs_details where log_id = {log_id};")
    query_data = curr.fetchone()
    curr.close()
    conn.close()
    print("Executed status DB === ", query_data[0])
    return query_data[0]


def update_track_rerun_count(r_id, pass_count, fail_count):
    curr, conn = db_connection()
    curr.execute('''UPDATE track_rerun_count SET pass_count = %s, fail_count = %s WHERE reg_id = %s''', (pass_count, fail_count, r_id))
    conn.commit()
    curr.close()
    conn.close()

def get_rerun_pass_fail_count_status(r_id):
    curr, conn = db_connection()
    curr.execute(f"SELECT pass_count, fail_count, total_rerun_count FROM public.track_rerun_count where reg_id = {r_id};")
    query_data = curr.fetchone()
    curr.close()
    conn.close()
    if query_data:
        return query_data[0], query_data[1], query_data[2]
    else:
        return 0, 0, 0
    
def delete_track_rerun_tc(r_id):
    curr, conn = db_connection()
    curr.execute(f"DELETE FROM track_rerun_count where reg_id = {r_id};")
    conn.commit()
    curr.close()
    conn.close()

# create table track_rerun_count(
# 	reg_id serial NOT NULL,
# 	pass_count INT NOT NULL DEFAULT 0,
# 	fail_count INT NOT NULL DEFAULT 0,
# 	total_rerun_count INT NOT NULL DEFAULT 0,
#     testcase_details TEXT NOT NULL
    
# )

# ALTER TABLE public.track_rerun_count
# ADD COLUMN testcase_details TEXT NOT NULL;


# 1. create table track_rerun_count
# 2. rerun_tc api
# 3. rereun_mutltiple_tc in script.js
# 4. re_run_tc.html
# 5. def send_chart_details(data), def rerun_tc(log_id=None), def track_rerun_tc():app.py 
# 6. send_req in utils.py
# 7.   socket.on('charts_details', function (msg)  and chart_container(new) changes in tab script
# 8. changes related to log_id in each tc function
