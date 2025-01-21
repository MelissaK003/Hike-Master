from flask import Flask
from flask_migrate import Migrate
from models import TokenBlocklist, db, User
from datetime import timedelta
from flask_jwt_extended import JWTManager


app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hike.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Setup JWT
app.config["JWT_SECRET_KEY"] = "HIKE101"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
jwt = JWTManager(app)

# Token blocklist 
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

# lueprints
from views import user_bp, hike_bp, auth_bp
app.register_blueprint(user_bp)
app.register_blueprint(hike_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)

