from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(
        app,
        origins="*",
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Credentials",
        ],
        supports_credentials=True
    )

    from app.errors import blueprint as errors_bp
    app.register_blueprint(errors_bp)

    from app.views import blueprint as views_bp
    app.register_blueprint(views_bp)

    return app