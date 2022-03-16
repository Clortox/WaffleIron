from app import app
from app.routes.front import front
app.app.register_blueprint(front)

def create_app():
    return app.app
