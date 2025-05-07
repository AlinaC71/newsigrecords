import os

from flask import Flask, render_template
from .models import db
# from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) 

    app.secret_key ='138b977ff08ed968ccf472dd3ae2dbbf'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Andr66a1995@localhost/signall'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    db.init_app(app)

# Test connection
    with app.app_context():
        try:
            db.engine.connect()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

        db.create_all()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



     
    from sr.general.general import gen    
    app.register_blueprint(gen)

    from sr.reccontrol.reccontrol import rec_con    
    app.register_blueprint(rec_con)


        

    return app


