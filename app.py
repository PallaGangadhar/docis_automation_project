from flask import Flask, render_template, request, Response, redirect
from flask_socketio import SocketIO, emit
from flask_mail import Mail, Message
import os
import datetime
from test_code import *
from utlity import genearate_list_of_dict,convert_date_to_str,convert_str_to_date
from db import *
from send_mail import send_mail_to


async_mode = None

app = Flask(__name__)
app.secret_key = 'super secret key'

socketio = SocketIO(app, async_mode=async_mode)


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
def index():
    total_regression_count = i_cmts_count = harmony_count=0
    graph_data={}
    harmony_graph_data={}
    cmts_graph_data={}
    data1=[]
    data2=[]
    data3=[]
    dates=[]
    h_date=[]
    c_date=[]
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    flag=False

    if from_date != "" and to_date != "" and from_date != None and to_date != None:
        if from_date > to_date:
            flag=True

    if from_date != "" and to_date == "":
        to_date = from_date
    elif from_date == "" and to_date != "":
        from_date = to_date
    print("flag===>",flag)
    if flag == False:

        curr, conn=db_connection()
        curr.execute('SELECT * FROM regression')
        sample_data=curr.fetchone()
        curr.execute('SELECT count(*) FROM regression')
        total_regression_count=curr.fetchone()
        total_regression_count=total_regression_count[0]

        curr.execute('SELECT count(regression_logs_details.*) from regression_logs_details, regression WHERE regression_logs_details.regression_id=regression.regression_id and regression.cmts_type='"'Arris'"'')
        i_cmts_count = curr.fetchone()
        i_cmts_count = i_cmts_count[0]


        curr.execute('SELECT count(regression_logs_details.*) from regression_logs_details, regression WHERE regression_logs_details.regression_id=regression.regression_id and regression.cmts_type='"'Harmony'"'')
        harmony_count = curr.fetchone()
        harmony_count = harmony_count[0]

        if from_date == None and to_date == None or from_date == "" and to_date == "":
            curr.execute('SELECT count(*),DATE(date_added) as reg_date FROM regression GROUP BY DATE(date_added) ORDER BY reg_date DESC')
            regression_graph=curr.fetchall()
            
            curr.execute('SELECT count(regression_logs_details.regression_id),DATE(regression.date_added) as reg_date from regression_logs_details, regression WHERE regression_logs_details.regression_id=regression.regression_id and regression.cmts_type='"'Harmony'"' GROUP BY DATE(regression.date_added) ORDER BY reg_date DESC')
            harmony_graph=curr.fetchall()
            

            curr.execute('SELECT count(regression_logs_details.regression_id),DATE(regression.date_added) as reg_date from regression_logs_details, regression WHERE regression_logs_details.regression_id=regression.regression_id and regression.cmts_type='"'Arris'"' GROUP BY DATE(regression.date_added) ORDER BY reg_date DESC')
            cmts_graph=curr.fetchall()
        
        elif from_date != None and to_date != None  and from_date != "" and to_date != "":
            to_date=convert_str_to_date(to_date,"%Y-%m-%d")+datetime.timedelta(days=1)
            to_date=convert_date_to_str(to_date,"%Y-%m-%d")
            curr.execute(f"SELECT count(*),DATE(date_added) as reg_date FROM regression WHERE date_added BETWEEN '{from_date}' AND '{to_date}' GROUP BY DATE(date_added) ORDER BY reg_date DESC")
            regression_graph=curr.fetchall()
            
            curr.execute(f"SELECT count(regression_logs_details.regression_id),DATE(regression.date_added) as reg_date from regression_logs_details, regression WHERE regression_logs_details.regression_id=regression.regression_id and regression.cmts_type='Harmony' AND regression.date_added BETWEEN '{from_date}' AND '{to_date}' GROUP BY DATE(regression.date_added) ORDER BY reg_date DESC")
            harmony_graph=curr.fetchall()
            
            curr.execute(f"SELECT count(regression_logs_details.regression_id),DATE(regression.date_added) as reg_date from regression_logs_details, regression WHERE regression_logs_details.regression_id=regression.regression_id and regression.cmts_type='Arris' AND regression.date_added BETWEEN '{from_date}' AND '{to_date}' GROUP BY DATE(regression.date_added) ORDER BY reg_date DESC")
            cmts_graph=curr.fetchall()
        
        
        
        for i in regression_graph:   
            # date=i[1].strftime("%d-%m-%Y")
            date=i[1].strftime("%Y-%m-%d")
            data1.append({'date':date,'count':i[0]})
            dates.append(date)
        graph_data['data']=data1

        for i in harmony_graph:  
            date=i[1].strftime("%Y-%m-%d")
            h_date.append(date) 
            data2.append({'date':date,'count':i[0]})
        
    
        data2=genearate_list_of_dict(dates,h_date,data2)
        harmony_graph_data['data']=data2
    
        for i in cmts_graph:    
            date=i[1].strftime("%Y-%m-%d")
            c_date.append(date)
            data3.append({'date':date,'count':i[0]})
        

        data3=genearate_list_of_dict(dates,c_date,data3)
        cmts_graph_data['data']=data3

        conn.commit()
        curr.close()
        conn.close()
        return render_template('index.html',total_regression_count=total_regression_count,i_cmts_count=i_cmts_count,harmony_count=harmony_count,regression_date_graph=graph_data,harmony_graph_data=harmony_graph_data,cmts_graph_data=cmts_graph_data)

    else:
        return render_template('index.html',total_regression_count=total_regression_count,i_cmts_count=i_cmts_count,harmony_count=harmony_count,regression_date_graph=graph_data,harmony_graph_data=harmony_graph_data,cmts_graph_data=cmts_graph_data,error_message=True)



@app.route('/logs', methods=['GET','POST'])
def logs():
    if request.method == "POST":
        global reg_id
        reg_id=add_regression(request)
        tc = request.form.get('data')
        for tc_name in tc.split(','):
            eval(tc_name + "()")
           
        call_after_execution(reg_id)
    return render_template('logs.html')

@app.route('/i_cmts', methods=['GET','POST'])
def i_cmts():
    return render_template('i_cmts.html')

@app.route('/harmony', methods=['GET','POST'])
def harmony():
    return render_template('harmony.html')

@app.route('/ganga', methods=['GET','POST'])
def ganga():
    return render_template('ganga.html')


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



@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    emit('client disconnected','a client disconnected but I dont know who',broadcast = True)


@app.route("/stop", methods=['GET','POST'])
def stop():
    if request.method == "POST":
        socketio.stop()
        os.system("python -m flask run --reload")
    return Response({'msg':''})


@app.route("/add_regression_logs", methods=['GET','POST'])
def add_regression_logs():
    if request.method == "POST":
        response=request.json
        response['r_id']=reg_id
        add_regression_details(response)
    return Response({'msg':''})


@app.route("/view_regression_details", methods=['GET','POST'])
def view_regression_details():
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
    
    return render_template('regression_details.html',regression_details=regression_details,c_type=c_type,status=status)

@app.route("/view_tc_logs_details/<int:reg_id>", methods=['GET','POST'])
def view_tc_logs_details(reg_id):
    curr,conn=db_connection()
    # curr.execute(f'SELECT regression_logs_details.*,regression.summary_path FROM regression_logs_details,regression WHERE regression_logs_details.regression_id={reg_id} and regression.regression_id=regression_logs_details.regression_id')
    curr.execute(f'SELECT * FROM regression_logs_details WHERE regression_id={reg_id}')
    tc_logs_details=curr.fetchall()
    curr.execute(f"SELECT summary_path FROM regression WHERE regression_id={reg_id}")
    summary_path=curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('view_tc_logs_details.html',tc_logs_details=tc_logs_details,summary_path=summary_path,reg_id=reg_id)


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
    print("dd===",len(tc_ids))
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

if __name__ == '__main__':
    socketio.run(app, debug=True)


