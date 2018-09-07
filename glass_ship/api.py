from flask import Flask
from flask import jsonify, request
from glass_ship.ship import vesseltrackerservice
from glass_ship.storage.models import Seafarer
from glass_ship.storage.db import init_db, engine
from sqlalchemy.orm import sessionmaker
from glass_ship.storage import models


app = Flask("glass-ship")
app.debug = True
init_db()
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/get_ships_names')
def get_ship_names():
    vessels = models.Vessel.query.all()
    vessel_list = []
    for vessel in vessels:
        vessel_list.append(vessel.name)

    return jsonify({"name": vessel_list}), 200


@app.route('/register', methods=['POST'])
def store_user():
    """
    Store user into db
    :return: json response
    """
    data = request.get_json()
    user = Seafarer(name=data['name'], sailor_id=data['sailorID'],
                    phone=data['phone'], emergency_contact=data['emergencyContact'])
    if not session.query(Seafarer).filter(Seafarer.name == data['name'],
                                            Seafarer.sailor_id == data['sailor_id']).first():
        session.add(user)
        session.commit()
    else:
        return jsonify({"Message": "User already exists"}), 200
    return jsonify({"Message": "Saved user!"}), 200


@app.route('/insert_ships', methods=['GET'])
def insert_ships():
    vesseltrackerservice.store_vessels_in_database(session)
    return jsonify({"message": "I inserted all the ships, if you refresh this I will insert them again.. and again.. so don't do this"})
