from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY = 'dev')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    app.register_blueprint(db.bp)

    from . import cache
    app.register_blueprint(cache.bp)
    
    from . import views
    app.register_blueprint(views.bp)

    return app