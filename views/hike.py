from flask import jsonify,request,Blueprint
from models import Hike,User,db

hike_bp = Blueprint("hike_bp", __name__)

#Hike Details
#Fetch Hike details
@hike_bp.route("/hikes")
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
@hike_bp.route("/hike", methods=["POST"])
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
@hike_bp.route("/hike/<int:hike_id>", methods=["PATCH"])
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
@hike_bp.route("/hike/<int:hike_id>", methods=["DELETE"])
def delete_hike(hike_id):
    hike = Hike.query.get(hike_id)

    if hike:
        db.session.delete(hike)
        db.session.commit()
        return jsonify({"success": "Deleted successfully"}), 200
    else:
        return jsonify({"error": "Hike Destination you are trying to delete doesn't exist!"}), 404   