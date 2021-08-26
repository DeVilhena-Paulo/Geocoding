from flask import Flask
from api.rest import api_rest


app = Flask(
    __name__,
    template_folder="../site/templates",
    static_folder="../site/static",
)

app.register_blueprint(api_rest)


def get_app():
    return app
