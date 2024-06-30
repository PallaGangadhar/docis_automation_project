from flask import Flask, render_template, request, Response, redirect, session, url_for
from flask_socketio import SocketIO, emit
from flask_mail import Mail, Message
import os
import datetime
from test_code import *
from utlity import genearate_list_of_dict,convert_date_to_str,convert_str_to_date
from db import *
from send_mail import send_mail_to
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import re
from decorators import login_required,devices_details_render
import bcrypt
import threading
from cryptography.fernet import Fernet


async_mode = None

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SECRET_KEY'] = "testkey"


socketio = SocketIO(app, async_mode=async_mode)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def background_thread(data):
    socketio.emit('my_response',
                    {'data': str(data)})


def send_chart_details(data):
    pass_tc = data.get('pass')
    fail_tc = data.get('fail')
    p=0
    f=0
    pass_count, fail_count, total_count,no_run = select_query_to_get_count_details(reg_id)
    p=int(pass_count)+pass_tc
    f=int(fail_count)+fail_tc
    update_regression(pass_tc, fail_tc, reg_id)
    socketio.emit('charts_details',{'pass_tc':p, 'fail_tc':f,'r_id':reg_id,'total_count':total_count})


@app.route('/', methods=['GET','POST'])
@login_required
def index():
    total_regression_count = 0
    graph_data={}
    data1=[]
    dates=[]
  
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    if from_date != "" and to_date == "":to_date = from_date
    elif from_date == "" and to_date != "":from_date = to_date
    
    curr, conn=db_connection()
    curr.execute('SELECT count(regression_logs_details.log_id) from  regression_logs_details')
    total_regression_count=curr.fetchone()
    total_regression_count=total_regression_count[0]
    curr.execute(f"SELECT * FROM devices_details ORDER BY device_id DESC")
    devices_details=curr.fetchall()

    
    curr.execute('SELECT devices_details.device_name, count(regression_logs_details.*) FROM regression_logs_details inner JOIN regression ON regression.regression_id = regression_logs_details.regression_id RIGHT JOIN devices_details ON regression.device_id = devices_details.device_id GROUP BY devices_details.device_name')
    devices_regression_count = curr.fetchall()
    total_regression_devices = len(devices_regression_count)+1
    if from_date == None and to_date == None or from_date == "" and to_date == "":
        curr.execute('SELECT count(*),DATE(date_added) as reg_date FROM regression GROUP BY DATE(date_added) ORDER BY reg_date DESC')
        regression_graph=curr.fetchall()
        
        curr.execute('SELECT devices_details.device_name, count(regression_logs_details.regression_id),DATE(regression.date_added)  as reg_date from  regression INNER JOIN regression_logs_details ON regression_logs_details.regression_id = regression.regression_id INNER JOIN devices_details ON regression.device_id = devices_details.device_id GROUP BY DATE(regression.date_added), devices_details.device_id ORDER BY reg_date DESC')
        graph_details = curr.fetchall()

        curr.execute('SELECT devices_details.device_name, count(regression_logs_details.regression_id) from  regression INNER JOIN regression_logs_details ON regression_logs_details.regression_id = regression.regression_id INNER JOIN devices_details ON regression.device_id = devices_details.device_id GROUP BY  devices_details.device_name')
        pie_chart_details = curr.fetchall()

    
    elif from_date != None and to_date != None  and from_date != "" and to_date != "":
        to_date=convert_str_to_date(to_date,"%Y-%m-%d")+datetime.timedelta(days=1)
        to_date=convert_date_to_str(to_date,"%Y-%m-%d")
        curr.execute(f"SELECT count(*),DATE(date_added) as reg_date FROM regression WHERE date_added BETWEEN '{from_date}' AND '{to_date}' GROUP BY DATE(date_added) ORDER BY reg_date DESC")
        regression_graph=curr.fetchall()

        curr.execute(f"SELECT devices_details.device_name, count(regression_logs_details.regression_id),DATE(regression.date_added)  as reg_date from  regression INNER JOIN regression_logs_details ON regression_logs_details.regression_id = regression.regression_id INNER JOIN devices_details ON regression.device_id = devices_details.device_id AND regression.date_added BETWEEN '{from_date}' AND '{to_date}' GROUP BY DATE(regression.date_added), devices_details.device_id ORDER BY reg_date DESC")
        graph_details = curr.fetchall()

        curr.execute(f"SELECT devices_details.device_name, count(regression_logs_details.regression_id) from  regression INNER JOIN regression_logs_details ON regression_logs_details.regression_id = regression.regression_id INNER JOIN devices_details ON regression.device_id = devices_details.device_id AND regression.date_added BETWEEN '{from_date}' AND '{to_date}' GROUP BY  devices_details.device_name")
        pie_chart_details = curr.fetchall()
        
        
    
    for i in regression_graph:   
        date=i[1].strftime("%Y-%m-%d")
        data1.append({'date':date,'count':i[0]})
        dates.append(date)
    graph_data['data']=data1
    
    new_data =[]
    
    for graph_detail in graph_details:
        dt=convert_date_to_str(graph_detail[2],"%Y-%m-%d")
        new_data.append({'date':dt, 'data':[graph_detail[1]],'name':graph_detail[0]})

    for dt in range(0, len(new_data),1):
        for ct in range(0, len(dates),1):
            if dates[ct] not in new_data[dt]['date']:
                new_data[dt]['data'].insert(ct,0)

    new_graph_data={}
    new_graph_list_data=[]
    
    for i in range(0,len(new_data),1):
        if new_data[i]['name'] in new_graph_data.keys():
            new_graph_data[new_data[i]['name']].append(new_data[i]['data'])
        else:
            new_graph_data[new_data[i]['name']] = [new_data[i]['data']]
    
    new_data_2 ={}
    new_graph_data = [new_graph_data]
    for k in range(0,len([new_graph_data]),1):
        for i in new_graph_data[0].keys():
            output_list = [sum(pair) for pair in zip(*new_graph_data[k][i])]
            new_graph_list_data.append({'name':i,'data':output_list})
        

    new_data_2['data'] = new_graph_list_data

    pie_chart = []
    for pie in pie_chart_details:
        per = (pie[1]/total_regression_count)*100
        pie_chart.append({'name':pie[0], 'y':round(per,2)})


    conn.commit()
    curr.close()
    conn.close()
    is_data_present=len(regression_graph)
    return render_template('index.html',total_regression_count=total_regression_count,regression_date_graph=graph_data,devices_details=devices_details,devices_regression_count=devices_regression_count,new_data_2=new_data_2,pie_chart=pie_chart,total_regression_devices=total_regression_devices,is_data_present=is_data_present)



@app.route('/logs', methods=['GET','POST'])
@login_required
def logs():
    if request.method == "POST":
        global reg_id
        reg_id=add_regression(request)
        tc = request.form.get('data')
        for tc_name in tc.split(','):
            eval(tc_name + "()")
        call_after_execution(reg_id)
    return render_template('logs.html')

@app.route('/tc_execution/<int:device_id>', methods=['GET','POST'])
@login_required
def tc_execution(device_id):
    devices_details=header()
    curr, conn=db_connection()
    curr.execute(f"SELECT * FROM modules_details where device_id={device_id}")
    modules_details=curr.fetchall()
    curr.execute(f"SELECT * FROM testcase_details WHERE modules_id in (SELECT modules_id FROM modules_details where device_id={device_id} )")
    testcase_details = curr.fetchall()
    curr.execute(f"SELECT * FROM devices_details where device_id={device_id}")
    device_details = curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('tc_execution.html',modules_details=modules_details,testcase_details=testcase_details,device_details=device_details,devices_details=devices_details)


@app.route('/modules', methods=['GET','POST'])
@login_required
def modules():
    devices_details=header()
    curr, conn=db_connection()
    # curr.execute(f"SELECT * FROM modules_details ORDER BY modules_id DESC")
    curr.execute("SELECT devices_details.device_name,modules_id, module_name FROM public.modules_details, devices_details where devices_details.device_id=modules_details.device_id ORDER BY modules_id DESC;")
    modules_details=curr.fetchall()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('modules.html',modules_details=modules_details,devices_details=devices_details)

@app.route('/devices', methods=['GET','POST'])
@login_required
def devices():
    
    curr, conn=db_connection()
    curr.execute(f"SELECT * FROM devices_details ORDER BY device_id DESC")
    devices_details=curr.fetchall()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('device_details.html',devices_details=devices_details)

@app.route('/testcase_details', methods=['GET','POST'])
@login_required
def testcase_details():
    devices_details=header()
    curr, conn=db_connection()
    # curr.execute(f"SELECT * FROM testcase_details ORDER BY testcase_id DESC")
    curr.execute('SELECT testcase_details.*,modules_details.module_name,devices_details.device_name FROM public.testcase_details,modules_details,devices_details where testcase_details.modules_id = modules_details.modules_id and modules_details.device_id=devices_details.device_id ORDER BY testcase_id DESC;')
    # curr.execute('SELECT testcase_details.*,devices_details.device_name, modules_details.module_name FROM testcase_details,modules_details, devices_details where devices_details.device_id=modules_details.device_id ORder by testcase_details.testcase_id desc;')
    testcase_details=curr.fetchall()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('testcase_details.html',testcase_details=testcase_details,devices_details=devices_details)

@app.route('/add_modules_details', methods=['GET','POST'])
@login_required
def add_modules():
    devices_details=header()
    curr, conn=db_connection()
    if request.method == "POST":
        module = str(request.form.get('module'))
        device_id = str(request.form.get('device_id'))
        curr.execute('''INSERT INTO modules_details(device_id,module_name) VALUES (%s,%s)''',(device_id,module) )
    curr.execute(f"SELECT * FROM devices_details ORDER BY device_id DESC")
    devices_details=curr.fetchall()
    conn.commit()
    curr.close()
    conn.close()
    
    return render_template('add_modules.html',devices_details=devices_details)

@app.route('/add_device_details', methods=['GET','POST'])
@login_required
def add_device_details():
    devices_details=header()
    error_message=None
    if request.method == "POST":
        device_name = str(request.form.get('device_name'))
        device_ip = str(request.form.get('device_ip'))
        model = str(request.form.get('model'))
        vendor = str(request.form.get('vendor'))
        curr, conn=db_connection()
        
        try:
            curr.execute('''INSERT INTO devices_details(device_name,ip,model, vendor) VALUES (%s,%s,%s,%s)''',(device_name,device_ip, model, vendor) )
        except Exception as e:
            pat = re.search("DETAIL:.*", str(e))
            if pat!= None:
                error_message=pat.group(0)
            else:
                error_message = str(e)
            
        conn.commit()
        curr.close()
        conn.close()
    return render_template('add_device_details.html',error_message=error_message,devices_details=devices_details)


@app.route('/add_testcase_details', methods=['GET','POST'])
@login_required
def add_testcase_details():
    devices_details=header()
    curr, conn=db_connection()
    if request.method == "POST":
        module_id = str(request.form.get('module_id'))
        testcase_number = str(request.form.get('testcase_number'))
        testcase_name = str(request.form.get('testcase_name'))
        testcase_function = str(request.form.get('testcase_function'))
        testcase_reference=str(request.form.get('testcase_reference'))
        curr.execute('''INSERT INTO testcase_details(modules_id,testcase_number,testcase_name,testcase_function,testcase_reference) VALUES (%s,%s,%s,%s,%s)''',(module_id,testcase_number,testcase_name,testcase_function,testcase_reference) )
    curr.execute(f"SELECT * FROM modules_details ORDER BY modules_id DESC")
    modules_details=curr.fetchall()
    conn.commit()
    curr.close()
    conn.close()
    
    return render_template('add_testcase_details.html',modules_details=modules_details,devices_details=devices_details)


@app.route("/connect", methods=['GET','POST'])
@socketio.event
def connect():
    if request.method == "POST":
        data=request.json.get('data')
        socketio.start_background_task(background_thread, data)
        return Response({'msg':"Hi"})
    else:
        emit('my_response', {'data': ''})

@app.route("/charts", methods=['GET','POST'])
@socketio.event
def charts():    
    if request.method == "POST":
        data=request.json
        send_chart_details(data)
        return Response({'msg':"Hi"})
    else:
        return render_template('charts.html')

@app.route("/disconnect", methods=['GET','POST'])
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    emit('client disconnected','a client disconnected but I dont know who')


@app.route("/stop", methods=['GET','POST'])
@socketio.on('disconnect')
def stop():
    if request.method == "POST":
        shutdown_server()
    return Response({'msg':''})


@app.route("/add_regression_logs", methods=['GET','POST'])
def add_regression_logs():
    if request.method == "POST":
        response=request.json
        response['r_id']=reg_id
        add_regression_details(response)
    return Response({'msg':''})


@app.route("/view_regression_details", methods=['GET','POST'])
@login_required
def view_regression_details():
    devices_details=header()
    curr,conn=db_connection()
    cmts_type = request.args.get('cmts_type_dropdown')
    search_reg = request.args.get('search_reg')
    if cmts_type != None and cmts_type != "" and (search_reg == None or search_reg == ""):
        cmts_type="'"+cmts_type+"'"
        curr.execute(f"SELECT * FROM regression WHERE cmts_type="+cmts_type+"ORDER BY date_added DESC")

    elif search_reg != None and search_reg != "" and (cmts_type == None or cmts_type == ""):
        search_reg="'%"+search_reg+"%'"
        curr.execute(f"SELECT * FROM regression WHERE LOWER(regression_name) LIKE LOWER("+search_reg+")ORDER BY date_added DESC")
        
    elif search_reg != None and search_reg != "" and cmts_type != None and cmts_type != "" :
        search_reg="'%"+search_reg+"%'"
        cmts_type="'"+cmts_type+"'"
        curr.execute(f"SELECT * FROM regression WHERE LOWER(regression_name) LIKE LOWER("+search_reg+") and cmts_type="+cmts_type+" ORDER BY date_added DESC")

    else:
        curr.execute('SELECT * FROM regression ORDER BY date_added DESC')

    regression_details=curr.fetchall()
    
    curr.execute('SELECT cmts_type,status FROM regression')
    c_type_curr=curr.fetchall()
    
    c_type=[]
    status=[]
    for i in c_type_curr:
        [c_type.append(i[0]) if i[0] not in c_type else None]
        [status.append(i[1]) if i[1] not in status else None]

    conn.commit()
    curr.close()
    conn.close()
    
    return render_template('regression_details.html',regression_details=regression_details,c_type=c_type,status=status,devices_details=devices_details)

@login_required
@app.route("/view_tc_logs_details/<int:reg_id>", methods=['GET','POST'])
def view_tc_logs_details(reg_id):
    devices_details=header()
    curr,conn=db_connection()
    curr.execute(f'SELECT * FROM regression_logs_details WHERE regression_id={reg_id}')
    tc_logs_details=curr.fetchall()
    curr.execute(f"SELECT summary_path FROM regression WHERE regression_id={reg_id}")
    summary_path=curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('view_tc_logs_details.html',tc_logs_details=tc_logs_details,summary_path=summary_path,reg_id=reg_id,devices_details=devices_details)


@app.route('/delete_regression/<int:id>', methods=['GET','POST'])
def delete_regression(id):
    if request.method == "POST":
        curr,conn=db_connection()
        curr.execute(f'DELETE FROM regression_logs_details WHERE regression_id={id}')
        curr.execute(f'DELETE FROM regression WHERE regression_id={id}')
        conn.commit()
        curr.close()
        conn.close()
        return redirect("/view_regression_details")


@app.route('/send_mail/<int:reg_id>', methods=['GET','POST'])
def send_mail(reg_id):
    if request.method == "POST":
        email= request.form.get('emails')
        print("Email===>",email)
        curr,conn=db_connection()
        curr.execute(f'SELECT summary_path FROM regression WHERE regression_id={reg_id}')
        summary_path = curr.fetchone()
        send_mail_to(summary_path[0])
        conn.commit()
        curr.close()
        conn.close()
        return redirect("/view_regression_details")

@app.route('/delete_selected_regression', methods=['GET','POST'])
def delete_selected_regression():
    tc_ids = request.form.get('data')
    tc_ids=tc_ids.split(',')
    curr,conn=db_connection()
    for ids in tc_ids:
        curr.execute(f'DELETE FROM regression_logs_details WHERE regression_id={ids}')
        curr.execute(f'DELETE FROM regression WHERE regression_id={ids}')
    conn.commit()
    curr.close()
    conn.close()
    
    return redirect("/view_regression_details")

@app.route('/delete_all_regressions', methods=['GET','POST'])
def delete_all_regressions():
    curr,conn=db_connection()
    curr.execute(f'DELETE FROM regression_logs_details')
    curr.execute(f'DELETE FROM regression ')
    conn.commit()
    curr.close()
    conn.close()
    
    return redirect("/view_regression_details")

@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        curr,conn=db_connection()
        curr.execute('SELECT * FROM user_info WHERE username = %s', (username, ))
        account = curr.fetchone()
        if account != None:
            password = password.encode('utf-8') 
            account_password = account[1].encode('utf-8')
            if password == account_password:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                msg = 'Logged in successfully !'
                return redirect(url_for('index'))
            else:
                msg = 'Incorrect username / password !'
        else:
            msg = 'Incorrect username / password !'

    return render_template('login.html',msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']
        curr,conn=db_connection()
        curr.execute('SELECT * FROM user_info WHERE username = %s', (username, ))
        account = curr.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Usernamconverted_to_bytese must contain only characters and numbers !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else:
            converted_to_bytes = password.encode('utf-8') 
            salt = bcrypt.gensalt() 
            encrypted_password = bcrypt.hashpw(converted_to_bytes, salt)
            curr.execute('''INSERT INTO user_info(username, password) VALUES (%s, %s)''', (username, encrypted_password, ))

            conn.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/edit_device_details/<int:device_id>', methods=['GET','POST'])
@login_required
def edit_device_details(device_id):
    devices_details=header()
    curr, conn=db_connection()
    error_message = None
    update_device_details=curr.execute(f"SELECT * FROM devices_details WHERE device_id={device_id}")
    update_device_details=curr.fetchone()
    if request.method == "POST":
        device_name = str(request.form.get('device_name'))
        device_ip = str(request.form.get('device_ip'))
        model = str(request.form.get('model'))
        vendor = str(request.form.get('vendor'))
        try:
            curr.execute(f'UPDATE devices_details SET device_name=%s,ip=%s,model=%s,vendor=%s WHERE device_id = %s',(device_name,device_ip, model, vendor,device_id) )
            conn.commit()
            curr.close()
            conn.close()
        except Exception as e:
            pat = re.search("DETAIL:.*", str(e))
            if pat!= None:
                error_message=pat.group(0)
            else:
                error_message = str(e)
        if error_message != None:
            return render_template('edit_device_details.html',update_device_details = update_device_details,error_message=error_message,devices_details=devices_details)
        else:
            return redirect(url_for('devices'))
      
    conn.commit()
    curr.close()
    conn.close()
        
    return render_template('edit_device_details.html',update_device_details = update_device_details,error_message=error_message,devices_details=devices_details)

@app.route('/edit_testcase_details/<int:testcase_id>', methods=['GET','POST'])
@login_required
def edit_testcase_details(testcase_id):
    devices_details=header()
    curr, conn=db_connection()
    error_message = None
    update_testcase_details=curr.execute(f"SELECT * FROM testcase_details WHERE testcase_id={testcase_id}")
    update_testcase_details=curr.fetchone()
    if request.method == "POST":
        testcase_number = str(request.form.get('testcase_number'))
        testcase_name = str(request.form.get('testcase_name'))
        testcase_function = str(request.form.get('testcase_function'))
        testcase_reference = str(request.form.get('testcase_reference'))
        try:
            curr.execute(f'UPDATE testcase_details SET testcase_number=%s,testcase_name=%s,testcase_function=%s,testcase_reference=%s WHERE testcase_id = %s',(testcase_number,testcase_name, testcase_function,testcase_reference,testcase_id) )
            conn.commit()
            curr.close()
            conn.close()
        except Exception as e:
            pat = re.search("DETAIL:.*", str(e))
            if pat!= None:
                error_message=pat.group(0)
            else:
                error_message = str(e)
        if error_message != None:
            return render_template('edit_testcase_details.html',update_testcase_details = update_testcase_details,error_message=error_message,devices_details=devices_details)
        else:
            return redirect(url_for('testcase_details'))
      
    conn.commit()
    curr.close()
    conn.close()
        
    return render_template('edit_testcase_details.html',update_testcase_details = update_testcase_details,error_message=error_message,devices_details=devices_details)

@app.route('/edit_modules_details/<int:module_id>', methods=['GET','POST'])
@login_required
def edit_module_details(module_id):
    devices_details=header()
    curr, conn=db_connection()
    update_module_details=curr.execute(f"SELECT * FROM modules_details WHERE modules_id={module_id}")
    update_module_details=curr.fetchone()
    error_message = None
    if request.method == "POST":
        module_name = str(request.form.get('module'))
        print("Moduke name====", module_name)
        print("Moduke name====", module_id)
       
        try:
            curr.execute(f'UPDATE modules_details SET module_name=%s WHERE modules_id = %s',(module_name,module_id) )
            conn.commit()
            curr.close()
            conn.close()
        except Exception as e:
            pat = re.search("DETAIL:.*", str(e))
            if pat!= None:
                error_message=pat.group(0)
            else:
                error_message = str(e)
        print("Error message===", error_message)
        
        return redirect(url_for('modules'))
      
    conn.commit()
    curr.close()
    conn.close()
        
    return render_template('edit_modules_details.html',update_module_details = update_module_details,error_message=error_message,devices_details=devices_details)



@app.route('/get_device_details_from_modules',  methods=['GET','POST'])
def get_device_details_from_modules():
    if request.method == 'POST':
        device_id = request.form.get('data')
        curr, conn=db_connection()
        curr.execute(f"SELECT * FROM devices_details WHERE device_id={device_id}")
        module_device_details=curr.fetchone()
        print("====", module_device_details)
        conn.commit()
        curr.close()
        conn.close()
        return render_template('get_device_details_from_modules.html',module_device_details=module_device_details)

@app.route('/delete_testcase/<int:id>', methods=['GET','POST'])
def delete_testcase(id):
    if request.method == "POST":
        curr,conn=db_connection()
        curr.execute(f'DELETE FROM testcase_details WHERE testcase_id={id}')
        conn.commit()
        curr.close()
        conn.close()
        return redirect("/testcase_details")



def header():
    curr, conn=db_connection()
    curr.execute(f"SELECT * FROM devices_details ORDER BY device_id DESC")
    devices_details=curr.fetchall()
    conn.commit()
    curr.close()
    conn.close()
    return devices_details


if __name__ == '__main__':
    socketio.run(app, debug=True)

