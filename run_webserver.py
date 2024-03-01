import datetime as dt
import argparse
import logging
from app import get_app

parser = argparse.ArgumentParser(description="Local Webserver.")
parser.add_argument("--disable_login", nargs='?', const=True, type=bool, default=False, help="Disables login requirement for the server.")
parser.add_argument("--disable_user_registration", nargs='?', const=True, type=bool, default=False, help="Disables user registration for the server.")
parser.add_argument('--port', default='7075', help="Port the server will run on.", required=False)
parser.add_argument("--host", default=None, help="Address that the server is hosted on. Default is localhost.", required=False)
parser.add_argument("--ssl_key", default="", help="[optional] location of your ssl key. full path required. ex: C:/Path/filename.key. Needs ssl_cert in conjunction with ssl_key.", required=False)
parser.add_argument("--ssl_cert", default="", help="[optional] location of your ssl cert. full path required. ex: C:/Path/filename.cert. Needs ssl_key in conjunction with ssl_cert.", required=False)
parser.add_argument("--enable_csrf_protection", nargs='?', const=True, type=bool, default=True, help="Enables CSRF Protection for the server.", required=False)
parser.add_argument("--csrf_time_limit", nargs='?', const=True, type=int, default=86400, help="If CSRF Protection is enabled, sets the timeout for CSRF protected pages.", required=False)
parser.add_argument("--enable_info_logging", nargs='?', const=True, type=bool, default=False, help="If enabled, displays routes and any accompanying information in the terminal.", required=False)


parser.add_argument("--key_flask_secret_key", type=str, default='FLASK_SECRET_KEY', help="Key used to get the flask_secret_key value from the system variables or .env file.", required=False)
parser.add_argument("--key_postgres_login_user", type=str, default='POSTGRES_USER', help="Key used to get the postgres_login_user value from the system variables or .env file.", required=False)
parser.add_argument("--key_postgres_login_password", type=str, default='POSTGRES_PASSWORD', help="Key used to get the postgres_login_password value from the system variables or .env file.", required=False)
parser.add_argument("--key_postgres_host", type=str, default='POSTGRES_HOST', help="Key used to get the postgres_host value from the system variables or .env file.", required=False)
parser.add_argument("--key_postgres_port", type=str, default='POSTGRES_PORT', help="Key used to get the postgres_port value from the system variables or .env file.", required=False)
parser.add_argument("--key_postgres_database", type=str, default='POSTGRES_DATABASE', help="Key used to get the postgres_database value from the system variables or .env file.", required=False)


args = vars(parser.parse_args())

if __name__ == '__main__':
    app = get_app(**args)
    log = logging.getLogger('werkzeug')
    if args.get('enable_info_logging',False) is False:
        log.setLevel(logging.ERROR)

    ## On imagesorter, ending the request for an image would create an SSLEOFError, but only on the python-mamba installation...and I'm not sure how to fix it.
    ## So I'm filtering it out. Please let me know if there's a solution to this that doesn't involve suppressing all SSLEOFErrors.
    ## Doesn't seem to cause any actual issues other than clog up the command prompt.
    class SSLEOFErrorFilter(logging.Filter):
        def filter(self, record):
            # Return False to filter out log records with SSLEOFError
            return "SSLEOFError" not in record.getMessage()
    log.addFilter(SSLEOFErrorFilter())

    @app.template_filter('convert_datetime')
    def convert_datetime(text, strptime='%Y-%m-%d %H:%M:%S.%f', strftime='%x'):
        try:
            results = dt.datetime.strptime(text, strptime).strftime(strftime)
            return results
        except:
            return text


    if app.config['LOGIN_MANAGER_LOADED'] is False:
        app.config['LOGIN_DISABLED'] = True
    else:
        app.config['LOGIN_DISABLED'] = args.get('disable_login',False)

    if args.get('disable_user_registration',False) == True:
        app.config['USER_REGISTRATION_DISABLED'] = True
    else:
        app.config['USER_REGISTRATION_DISABLED'] = False

    app.config['parsed_args'] = args
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    if CSRF_PROTECTION_STATUS:= args.get('enable_csrf_protection',False) == True:
        print("\tCSRF Protection Enabled.")
        app.config['WTF_CSRF_TIME_LIMIT'] = int(args.get('csrf_time_limit',86400)) #1 Day
    else:
        pass


    app.config['WTF_CSRF_CHECK_DEFAULT'] = CSRF_PROTECTION_STATUS
    PORT = args.get('port', 7070)
    HOST = args.get('host', None)



    print("PORT:",PORT,'HOST:','localhost' if HOST is None else HOST)
    if (ssl_cert:=args.get("ssl_cert",None)) and (ssl_key:=args.get('ssl_key',None)):
        # if os.path.isfile(ssl_cert) and os.path.isfile(ssl_key):
        app.run(debug=False, port=PORT, threaded=True, host=HOST,
                ssl_context=(ssl_cert, ssl_key))

    else:
        app.run(debug=False, port=args.get('port',7070), threaded=True, host=HOST)

