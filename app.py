import dotenv
import os
import importlib

import sqlalchemy

import flask
from flask import Blueprint,send_from_directory,render_template,url_for
from imports import mimetypes

from flask_wtf.csrf import CSRFProtect

from imports.bootstrap import bootstrap
from imports.database import db
dotenv.load_dotenv(dotenv.find_dotenv(),override=True)

def get_app(**kwargs):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config[
        'SECRET_KEY'] = os.getenv(kwargs.get('key_flask_secret_key'))




    # Get the path of the 'modules' folder
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')

    import sys
    # Iterate over the folders in the 'extensions' directory
    databases = []
    blueprint_names = []
    blueprint_display_names = {}
    schemas_list = []
    for module_folder in os.listdir(modules_dir):

        # Construct the full path of the plugin folder
        module_path = os.path.join(modules_dir, module_folder)



        # Check if the item is a directory
        if os.path.isdir(module_path) and module_path != '__pycache__':

            if os.path.isfile(os.path.join(module_path, 'base_settings.py')) and \
                    os.path.isfile(os.path.join(module_path, 'view.py')):

                print('\nLoading Modules Folder:', module_folder)
                module = importlib.import_module(f'modules.{module_folder}.base_settings', f'.modules.{module_folder}.base_settings')

                importlib.import_module(f'modules.{module_folder}.view',f'.modules.{module_folder}.view') #Loads the view.

                # Use the imported module as needed
                if hasattr(module, 'blueprints'):
                    blueprints = getattr(module, 'blueprints')
                    for blueprint in blueprints:
                        app.register_blueprint(blueprint)
                        blueprint_names.append(blueprint.name)
                        try:
                            blueprint_display_names[blueprint.name] = blueprint.display_name
                        except:
                            blueprint_display_names[blueprint.name] = blueprint.name
                if hasattr(module,'Schema'):
                    db_schema = getattr(module,'Schema')
                    schemas_list.append(db_schema)
                if hasattr(module,'database_binding'):
                    database_binding = getattr(module, 'database_binding')
                    databases.append(database_binding)
                else:
                    databases.append(module_folder)
            else:
                databases.append(module_folder)







    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=os.getenv(kwargs.get('key_postgres_login_user')),
                                                                                                  pw=os.getenv(kwargs.get('key_postgres_login_password')),
                                                                                                  port=os.getenv(kwargs.get('key_postgres_port')),
                                                                                                  host=os.getenv(kwargs.get('key_postgres_host')),
                                                                                                  db=os.getenv(kwargs.get('key_postgres_database')))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['CACHE_TYPE'] = 'simple'
    app.config['SESSION_COOKIE_SAMESITE'] = "Strict"
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config['SQLALCHEMY_BINDS'] = {
        db_name: f'{app.config["SQLALCHEMY_DATABASE_URI"]}' for xy, db_name in enumerate(databases)
    }
    print('Databases:',app.config['SQLALCHEMY_BINDS'].keys())

    CSRFProtect(app)
    db.init_app(app)
    bootstrap.init_app(app)
    try:
        from imports.login_manager import login_manager
        login_manager.init_app(app)
        app.config['LOGIN_MANAGER_LOADED'] = True
    except Exception as e:
        app.config['LOGIN_MANAGER_LOADED'] = False
        app.config['LOGIN_DISABLED'] = True
        print("\n[ERROR] Unable to load login manager due to the following reason:",e)
        print("\tLogin has been disabled and is no longer required. If this is not desired, please correct the issue and restart the server.\n")

    # limiter.init_app(app)



    with app.app_context():
        # get all the tables defined in your models
        db.create_all()
        tables = db.Model.metadata.tables.values()

        # group the tables by schema
        schemas = []
        for table in tables:
            schema_name = table.schema
            if schema_name not in schemas:
                schemas.append(schema_name)
        for schema in schemas_list:
            if schema not in schemas:
                schemas.append(schema)

        # create the schemas
        if len(schemas) > 0:
            print("Schemas to create:",schemas)
        with db.engine.connect() as conn:
            for schema_name in schemas:
                if not conn.dialect.has_schema(conn, schema_name):
                    conn.execute(sqlalchemy.schema.CreateSchema(schema_name))
            db.session.commit()



    FileServer = Blueprint('FileServer', __name__, static_folder='static')

    @FileServer.route('/static/<filename>', methods=["GET"])
    def load_files(filename):
        try:
            return send_from_directory(FileServer.static_folder, filename)
        except:
            return 'File Not Found.'

    @FileServer.route('/static/<folder>/<filename>', methods=['GET'])
    def load_file_from_folder(folder, filename):
        # print(FileServer.static_folder)
        try:
            try:
                return send_from_directory('{}/{}'.format(FileServer.static_folder, folder), filename,
                                           mimetype=mimetypes.MimeTypes['.{}'.format(filename.split('.')[-1])][-1])
            except:
                return send_from_directory('{}/{}'.format(FileServer.static_folder, folder), filename)
        except:
            return 'File Not Found.'

    app.register_blueprint(FileServer)

    General = Blueprint('General', __name__,static_folder='static')
    General.blueprint_names = blueprint_names

    @General.route('/', methods=['GET'])
    def main():
        landing_pages = []
        for blueprint_name in General.blueprint_names:

            try:
                landing_pages.append([url_for(f'{blueprint_name}.landing_page'),blueprint_display_names[blueprint_name]])
            except Exception as e:
                pass
                # print('Unable to load landing page:',blueprint_name)
                # print('\t',e)

        landing_page_wallpaper = None
        for ext in ['png','jpg','webp']:
            full_path = f'{General.static_folder}/landing_page_wallpaper.{ext}'
            if os.path.exists(full_path):
                landing_page_wallpaper = url_for("FileServer.load_files",filename=f"landing_page_wallpaper.{ext}")
        return render_template('/main/landing_page.html',available_landing_pages=landing_pages,landing_page_wallpaper=landing_page_wallpaper)
    app.register_blueprint(General)
    return app



