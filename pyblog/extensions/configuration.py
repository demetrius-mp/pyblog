from dynaconf import FlaskDynaconf

flask_dynaconf = FlaskDynaconf(ENVVAR_PREFIX='', ENVVAR_PREFIX_FOR_DYNACONF='')


def init_app(app, **config):
    flask_dynaconf.init_app(app, **config)
    app.config.load_extensions()
