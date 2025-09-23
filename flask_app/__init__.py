import os
from flask import Flask


#'flask --app flask_app:instantiate_app run' to run in the Terminal
#'flask --app flask_app:instantiate_app init-db' to initialise database
#Go to http://127.0.0.1:5000/works to see output
def instantiate_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='epic',
        DATABASE=os.path.join(app.instance_path, 'flask_app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    #flask DOESN'T auto make instance folders so it must be done manually
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/works')
    def hello():
        return 'Working!'

    #You can use '.' instead of 'flask_app' to import from root directory!
    from . import db_init
    db_init.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
