# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# #Create database object globally
# db=SQLAlchemy()

# def create_app():
#     app=Flask(__name__)

#     app.config['SECRET_KEY']='your-secret-key'
#     app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#     db.__init__(app)

#     from app import models

#     from app.routes.auth import auth_bp
#     from app.routes.tasks import tasks_bp
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(tasks_bp)

#     return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database object globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # ✅ Use init_app, not db.__init__

    # ✅ Import models inside the app context so they register with SQLAlchemy
    with app.app_context():
        from app import models

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app
