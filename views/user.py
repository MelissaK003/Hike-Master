from flask import jsonify,request,Blueprint
from models import User,db
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user_bp", __name__)

#User CRUD Operations
#  Fetch User
@user_bp.route("/users")
def fetch_users():
    users = User.query.all()
    user_list = []

    for user in users:
        user_list.append({
            'id':user.id,
            'username':user.username,
            'first_last_name':user.first_last_name,
            'email':user.email
              
        })

    return jsonify(user_list)

#Add User
@user_bp.route("/users", methods=["POST"])
def add_users():
    data = request.get_json()
    username = data['username']
    first_last_name = data['first_last_name']
    email = data['email']
    password = generate_password_hash( data['password'])

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    print("Email ",check_email)
    print("Username",check_username)
    if check_username or check_email:
        return jsonify({"error": "Username or email already exists"}),409

    else:
        new_user = User(username=username, email=email, password=password, first_last_name = first_last_name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success":"User added successfully"}), 201

#Update User
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        username = data['username']
        first_last_name = data['first_last_name']
        email = data['email']
        password = data['password']

        check_username = User.query.filter_by(username=username and id!=user.id).first()
        check_email = User.query.filter_by(email=email and id!=user.id).first()

    
        if check_username or check_email:
            return jsonify({"error":"Username/email exists"}),406

        else:
            user.username=username
            user.first_last_name=first_last_name
            user.email=email
            user.password=password
          
            db.session.commit()
            return jsonify({"success":"Updated successfully"}), 201

    else:
        return jsonify({"error":"User doesn't exist!"}),406

#Delete User
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "Deleted successfully"}), 200
    else:
        return jsonify({"error": "User you are trying to delete doesn't exist!"}), 404