from dynaconf import FlaskDynaconf

flask_dynaconf = FlaskDynaconf()


def init_app(app, **config):
    flask_dynaconf.init_app(app, **config)
    app.config.load_extensions()
