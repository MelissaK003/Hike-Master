from flask import jsonify, request, Blueprint
from models import User, db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint("auth_bp", __name__)

# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    else:
        return jsonify({"error": "Either email or password is incorrect"}), 401
    
 # current user
@auth_bp.route("/current_user", methods=["GET"])
@jwt_required()
def current_user():
    current_user_id  = get_jwt_identity()
    return jsonify({'current_user_id':current_user_id})   

#Logout