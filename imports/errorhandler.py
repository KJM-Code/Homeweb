
from flask import jsonify
from flask import session
from flask import request
from flask import url_for,redirect,render_template
from flask_login import current_user

def make_error(status_code, message,Include_Schema=False,extra_message=None):
    print(__name__,request.url_rule,'\n^__ERROR: ',message)
    response_dict = {
        'status': status_code,
        'message': message,
    }
    response = jsonify(response_dict)
    response.status_code = status_code
    session['error_log'] = 'Message: {}'.format(message)
    if extra_message is not None:
        session['error_log']+= ' || Extra:'+extra_message
    session['error_log']+='\n'
    return response