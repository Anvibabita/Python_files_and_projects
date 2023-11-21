#pip install mysql-connector-python
""" Store website user activity in MySQL db """
from mysql.connector import connect
from flask import request, session, current_app as ca, Response
from datetime import datetime
from db import MYQL

def user_audit(request: request, session: session, current_app: ca, response: Response):
 try:
    request_object = {}
    #creating keys and values
    request_object['system_name'] = current_app.name
    request_object['username'] = session.get('uname')
    request_object["url"] = request.url
    request_object["method"] = request.method 
    request_object["ip_address"] = request.remote_addr
#    if request.method.lower() != 'get':
    request_object.update({"body": request.get_json(silent=True)})
    if request.args:
        request_object["arguments"] = request.args
    if request.form:
        request_object["form_data"] = request.form.to_dict()                                    
    request_object.update({
        "action_result": any([request_object.get('body'),
            request_object.get('arguments'),
            request_object.get('form_data')])
        })
    request_object.update({"return_value": response.get_json(silent=True)})
    # js = request.json  
    if request.method == 'POST':
        request_object["body_req"] = request.json
    
    #creating dynamic query
    query = f"""INSERT INTO USER_AUDIT (
        user_name, api_name, time_of_action,
        ip_address, action_result, action_name, return_value, system_name, method, body_request
        )
        VALUES
        ("{request_object['username']}", "{request_object['url']}", "{datetime.now()}",
        "{request_object['ip_address']}", "{request_object['action_result']}", "{request_object['url'][17:]}",
        "{request_object['return_value']}", "{request_object['system_name']}","{request_object['method']}","{request_object['body_req']}");
    """
    MYQL().insert(query)
    #return request_object

 except Exception as er:
    print(er)
   

