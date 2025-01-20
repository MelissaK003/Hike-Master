from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import User,Hike, db
from flask_jwt_extended import JWTManager
from datetime import timedelta


# migration initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hike.db'
migrate = Migrate(app, db)
db.init_app(app)

# importing functions from  views
from views import *

app.register_blueprint(user_bp)
app.register_blueprint(hike_bp)
app.register_blueprint(auth_bp)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "HIKE101" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] =  timedelta(minutes=15) 
jwt = JWTManager(app)
jwt.init_app(app)


if __name__ == "__main__":
    app.run()
