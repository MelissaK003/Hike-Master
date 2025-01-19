from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import User,Hike, db

# migration initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hike.db'
migrate = Migrate(app, db)
db.init_app(app)

#User CRUD Operations
#  Fetch User
@app.route("/users")
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
@app.route("/users", methods=["POST"])
def add_users():
    data = request.get_json()
    username = data['username']
    first_last_name = data['first_last_name']
    email = data['email']
    password = data['password']

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
@app.route("/users/<int:user_id>", methods=["PATCH"])
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
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "Deleted successfully"}), 200
    else:
        return jsonify({"error": "User you are trying to delete doesn't exist!"}), 404

#Hike Details
#Fetch Hike details
@app.route("/hikes")
def fetch_hikes():
    hikes = Hike.query.all()
    hike_list = []

    for hike in hikes:
        hike_list.append({
            'id':hike.id,
            'hike_name':hike.hike_name,
            'location':hike.location,
            'rating':hike.rating
    
        })

    return jsonify(hike_list)

#Add Hike
@app.route("/hike", methods=["POST"])
def add_hike():
    data = request.get_json()
    hike_name = data.get('hike_name')  
    location = data.get('location')
    rating = data.get('rating')
    user_id = data['user_id']

    check_hikename = Hike.query.filter_by(hike_name=hike_name).first()
    check_user_id =User.query.get(user_id)
  

    if check_hikename:
        return jsonify({"error": "The hike title already exists"}), 409
    elif not check_user_id:
        return jsonify({"error":"User doesn't exists"}),409
    else:
        new_hike = Hike(hike_name=hike_name, location=location, rating=rating, user_id=user_id)
        db.session.add(new_hike)
        db.session.commit()
        return jsonify({"success": "Hike added successfully"}), 201
    
#Update Hike
@app.route("/hike/<int:hike_id>", methods=["PATCH"])
def update_hike(hike_id):
    hike = Hike.query.get(hike_id)

    if hike:
        data = request.get_json()

        hike_name = data.get('hike_name', hike.hike_name)  
        location = data.get('location', hike.location)     
        rating = data.get('rating', hike.rating)            
        user_id = data.get('user_id', hike.user_id)         

        check_hikename = Hike.query.filter_by(hike_name=hike_name).first()

        if check_hikename and check_hikename.id != hike.id:
            return jsonify({"error": "The hike title already exists"}), 409
        check_user_id = User.query.get(user_id)
        if not check_user_id:
            return jsonify({"error": "User doesn't exist"}), 409

        hike.hike_name = hike_name
        hike.location = location
        hike.rating = rating
        hike.user_id = user_id

        db.session.commit()
        return jsonify({"success": "Hike updated successfully"}), 200

    else:
        return jsonify({"error": "Hike not found!"}), 404
    
#Delete Hike 
@app.route("/hike/<int:hike_id>", methods=["DELETE"])
def delete_hike(hike_id):
    hike = Hike.query.get(hike_id)

    if hike:
        db.session.delete(hike)
        db.session.commit()
        return jsonify({"success": "Deleted successfully"}), 200
    else:
        return jsonify({"error": "Hike Destination you are trying to delete doesn't exist!"}), 404   




if __name__ == "__main__":
    app.run()
