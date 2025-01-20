from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import User,Hike, db

# migration initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hike.db'
migrate = Migrate(app, db)
db.init_app(app)

# importing functions from  views
from views import *

app.register_blueprint(user_bp)
app.register_blueprint(hike_bp)


if __name__ == "__main__":
    app.run()
