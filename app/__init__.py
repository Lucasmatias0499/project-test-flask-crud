from flask import Flask
from app.routes import user_bp
from app.database import init_db
import logging

logging.basicConfig(
    level=logging.INFO,  # Ou logging.DEBUG para mais detalhes
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)


def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(user_bp)
    return app