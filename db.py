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
    r_id=0
    curr.execute('''INSERT INTO regression(regression_name, pass_count, fail_count, no_run_count, total_count,status,cmts_type,device_id, regression_string) VALUES (%s, %s, %s, %s,%s,%s,%s,%s, %s) RETURNING regression_id''',
                  (regression_name, 0, 0, 0,int(total_tc_selected),"In Progress", cmts_type,device_id,regression_string))


    r_id = curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    r_id=str(r_id[0])
    return r_id
        

def update_regression(pass_tc,fail_tc,r_id):
    curr, conn=db_connection()
    curr.execute(f'SELECT * FROM regression WHERE regression_id={r_id}')
    query_data=curr.fetchone()
    pass_count=query_data[3]
    fail_count=query_data[4]
    no_run_count=query_data[5]
    total_count=query_data[6]

    pass_count+=pass_tc
    fail_count+=fail_tc
    curr.execute(f'UPDATE regression SET pass_count={pass_count}, fail_count={fail_count} WHERE regression_id={r_id}')
    
    if int(total_count) == int(pass_count)+int(fail_count)+int(no_run_count):

        curr.execute('''UPDATE regression SET status=%s WHERE regression_id=%s''',( "Completed", r_id))
    
    conn.commit()
    curr.close()
    conn.close()


def add_regression_details(response):
    r_id=response.get('r_id')
    status=response.get('status')
    fail_in=response.get('fail_in')
    tc_no=str(response.get('tc_no'))
    execution_time=response.get('execution_time')
    testcase_name=response.get('testcase_name')
    tc_logs_path=response.get('tc_logs_path')
    
    status=status.upper()
    curr, conn=db_connection()
    curr.execute('''INSERT INTO regression_logs_details(regression_id,testcase_number,testcase_name,status, failed_in,execution_time,tc_logs_path) VALUES (%s,%s,%s,%s,%s,%s,%s)''',(r_id,tc_no,testcase_name,status, fail_in, execution_time,tc_logs_path) )
    
    conn.commit()
    curr.close()
    conn.close()

    
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
    # curr.execute('''INSERT INTO regression_session(session_id,) VALUES (%s,) ''',
    #               (session_id))
    curr.execute('''INSERT INTO regression_session (session_id, regression_string) VALUES (%s, %s)''', (session_id,regression_string))
    conn.commit()
    curr.close()
    conn.close()


def get_sesson_id(regression_string):
    curr,conn=db_connection()
    curr.execute(f"SELECT CASE WHEN EXISTS ("+\
            "SELECT 1 "+\
            "FROM regression_session "+\
            "WHERE regression_string = %s"+\
        ") THEN 'True'"+\
        "ELSE 'False'"+\
    "END AS result;", (regression_string,))
    is_exists = curr.fetchone()[0]
    print("is exists===", is_exists)
    if is_exists == 'True':
        curr.execute("SELECT session_id FROM public.regression_session WHERE regression_string = %s", (regression_string,))
        session_id = curr.fetchone()[0]
        conn.commit()
    curr.close()
    conn.close()
    return session_id

def get_resgression_id(regression_string):
    curr,conn=db_connection()
    curr.execute("SELECT regression_id FROM public.regression WHERE regression_string = %s", (regression_string,))
    regression_id = curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()
    return regression_id

# CREATE TABLE IF NOT EXISTS user_info(
#     user_id serial,
#     username text NOT NULL, 
#     password text NOT NULL
   
# );
# CREATE TABLE IF NOT EXISTS user_access(
#     access_id serial,
#     user_id serial,
#     password text NOT NULL,
#     CONSTRAINT fk_user FOREIGN KEY(user_id)
#         REFERENCES user_info(user_id)
   
# );
# CREATE TABLE IF NOT EXISTS modules_details(
#     device_id serial ,
#     modules_id serial PRIMARY KEY,
#     module_name text NOT NULL,
# CONSTRAINT fk_device FOREIGN KEY(device_id)
#         REFERENCES devices_details(device_id)
# );
# CREATE TABLE IF NOT EXISTS devices_details(
#     device_id serial PRIMARY KEY,
#     device_name text NOT NULL,
#     ip text NOT NULL,
#     model text NOT NULL,
#     vendor text not null

# );
# CREATE TABLE IF NOT EXISTS testcase_details(
#     testcase_id serial PRIMARY KEY,
# modules_id serial,
#     testcase_number text not null,
#     testcase_name text not null,
#     testcase_function text not null,
# CONSTRAINT fk_module FOREIGN KEY(modules_id)
#         REFERENCES modules_details(modules_id)
# );

# def insert()
# curr.execute('CREATE TABLE IF NOT EXISTS regression (regression_id INT,'
#                                  'regression_name varchar (1000) NOT NULL,'
#                                  'pass_count integer NOT NULL,'
#                                  'fail_count integer NOT NULL,'
#                                  'total_count integer NOT NULL,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP),'
#                                 'PRIMARY KEY(regression_id)'
#                                  )


# curr.execute('CREATE TABLE IF NOT EXISTS logs (logs_id serial,'
#                                  'regression_id INT,'
#                                  'status varchar(1000) NOT NULL,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP,'
#                                  'CONSTRAINT fk_regression FOREIGN KEY(regression_id) REFERENCES regression(regression_id)'
#                                  )
# CREATE TABLE IF NOT EXISTS logs(
#     logs_id INT,
#     regression_id INT,
#     status varchar(1000) NOT NULL,
#     date_added date DEFAULT CURRENT_TIMESTAMP,

#     CONSTRAINT fk_regression FOREIGN KEY(regression_id)
#         REFERENCES regression(regression_id)
# );

# regression_name='ABC',
# pass_count=1
# fail_count=1
# total_count=0
# curr.execute(
#         '''INSERT INTO regression \
#         (regression_name, pass_count, fail_count,total_count) VALUES (%s, %s, %s, %s) RETURNING regression_id''',
#         (regression_name, pass_count, fail_count, total_count))

# data = curr.fetchone()
# print("User ID of latest entry:", type(data[0]))

# curr.execute(
#         '''INSERT INTO logs \
#         (regression_id,testcase_name, status) VALUES (%s,%s, %s)''',
#         (1,"TC_1","PASS"))

# CREATE TABLE IF NOT EXISTS regression_logs_details(
#     log_id serial,
#     regression_id serial,
#     testcase_number text,
#     testcase_name text,
#     status varchar(1000),
#     failed_in text,
#     execution_time text,
#     tc_logs_path text,
#     date_added timestamp DEFAULT CURRENT_TIMESTAMP,
#     CONSTRAINT fk_regression FOREIGN KEY(regression_id)
#         REFERENCES regression(regression_id)
# );

# CREATE TABLE IF NOT EXISTS regression(
#     regression_id serial,
#     device_id serial,
#     regression_name text NOT NULL, 
#     pass_count integer NOT NULL,
#     fail_count integer NOT NULL,
#     no_run_count integer NOT NULL,
#     total_count integer NOT NULL,
#     summary_path text,
#     status varchar(1000),
#     cmts_type varchar(1000),
#     date_added timestamp DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY(regression_id)
# CONSTRAINT fk_device FOREIGN KEY(device_id)
#         REFERENCES devices_details(device_id)

# );

# ikpD10@gpa002
# SELECT testcase_details.testcase_name FROM public.testcase_details,modules_details where testcase_details.modules_id = modules_details.modules_id and modules_details.modules_id=5;


# ALTER TABLE modules_details DROP CONSTRAINT fk_device;
# ALTER TABLE modules_details
# ADD CONSTRAINT fk_device FOREIGN KEY (device_id)
# REFERENCES devices_details (device_id) ON DELETE CASCADE;


# ALTER TABLE testcase_details DROP CONSTRAINT fk_module;
# ALTER TABLE testcase_details
# ADD CONSTRAINT fk_module FOREIGN KEY (modules_id)
# REFERENCES modules_details (modules_id) ON DELETE CASCADE;

# ALTER TABLE regression DROP CONSTRAINT fk_device;
# ALTER TABLE regression
# ADD CONSTRAINT fk_device FOREIGN KEY (device_id)
# REFERENCES devices_details (device_id) ON DELETE CASCADE;


# ALTER TABLE regression_logs_details DROP CONSTRAINT fk_regression;
# ALTER TABLE regression
# ADD CONSTRAINT fk_regression FOREIGN KEY (regression_id)
# REFERENCES regression (regression_id) ON DELETE CASCADE;



# WITH extracted_digits AS (
#     SELECT 
#         REGEXP_REPLACE(execution_time, '\D', '', 'g') AS digits_string
#     FROM 
#         regression_logs_details where regression_id=9
# )
# SELECT 
#     SUM(CAST(SUBSTRING(digits_string, 1) AS INTEGER)) AS sum_of_digits
# FROM 
#     extracted_digits;