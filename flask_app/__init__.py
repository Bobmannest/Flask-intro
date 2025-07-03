import os
from flask import Flask

#Use 'flask --app flask_app:instantiate_app run --debug' to run in the Terminal
#go to http://127.0.0.1:5000/hello to see output
def instantiate_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY='epic',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #Loads instance/custom config only if not testing
        app.config.from_pyfile('config.py', silent = True)
    else:
        #Loads test config
        app.config.from_mapping(test_config)

    #flask DOESN'T auto make instance folders so it must be done manually
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():  # put application's code here
        return 'Hello World!'

    return app
