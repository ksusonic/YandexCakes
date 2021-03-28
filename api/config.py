from flask import Flask

# TODO: https://flask.palletsprojects.com/en/1.1.x/config/

SECRET_KEY = "hello_Alice"
SQLALCHEMY_DATABASE_URI = 'sqlite:db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLAlCHEMY_ECHO = False
DEBUG = True


def configure_app(app: Flask) -> Flask:
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=SQLALCHEMY_TRACK_MODIFICATIONS,
        SQLAlCHEMY_ECHO=SQLAlCHEMY_ECHO,
        DEBUG=DEBUG,
    )
    return app
