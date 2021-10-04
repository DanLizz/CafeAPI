import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import json

app = Flask(__name__)

API_KEY = "MyToPsECRETapiKeyisThis"

# To disable sorting in jsonify
app.config['JSON_SORT_KEYS'] = False

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record

# Get Random Cafe
@app.route("/random", methods=["GET"])
def get_random_cafe():
    random_cafe = db.session.query(Cafe).order_by(func.random()).first()
    a_cafe = jsonify(
        cafe=jsonify
        (name=random_cafe.name,
         map_url=random_cafe.map_url,
         img_url=random_cafe.img_url,
         location=random_cafe.location,
         has_sockets=random_cafe.has_sockets,
         has_toilet=random_cafe.has_toilet,
         has_wifi=random_cafe.has_wifi,
         can_take_calls=random_cafe.can_take_calls,
         seats=random_cafe.seats,
         coffee_price=random_cafe.coffee_price,
         id=random_cafe.id,
         ).json
    )
    return a_cafe


# Get all Cafes
@app.route("/all", methods=["GET"])
def get_all_cafes():
    cafe_list = []
    all_cafe = db.session.query(Cafe).all()
    for cafe in all_cafe:
        each_cafe = {
            'id': cafe.id,
            'name': cafe.name,
            'location': cafe.location,
            'coffee_price': cafe.coffee_price,
            'seats': cafe.seats,
            'img_url': cafe.img_url,
            'map_url': cafe.map_url,
            'has_wifi': cafe.has_wifi,
            'has_sockets': cafe.has_sockets,
            'can_take_calls': cafe.can_take_calls,
            'has_toilet': cafe.has_toilet,
        }
        cafe_list.append(each_cafe)
    return jsonify(cafes=cafe_list)


# Find Cafes in a location
@app.route("/search")
def search_cafe():
    search_location = request.args.get('location', type=str)
    cafes = db.session.query(Cafe).filter_by(location=search_location).all()
    if not cafes:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe at that location."
        })
    else:
        cafe_list = []
        for cafe in cafes:
            cafe_dict = {"id": cafe.id,
                         "name": cafe.name,
                         "map_url": cafe.map_url,
                         "img_url": cafe.img_url,
                         "location": cafe.location,
                         "has_sockets": cafe.has_sockets,
                         "has_toilet": cafe.has_toilet,
                         "has_wifi": cafe.has_wifi,
                         "can_take_calls": cafe.can_take_calls,
                         "seats": cafe.seats,
                         "coffee_price": cafe.coffee_price}
            cafe_list.append(cafe_dict)
        all_cafes = {"cafes": cafe_list}
        all_cafes_json = jsonify(cafes=all_cafes["cafes"])
        return all_cafes_json


# HTTP POST - Create Record
# Add New Cafe
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def modify_price(cafe_id):
    cafe = db.session.query(Cafe).filter_by(id=cafe_id).first()
    updated_price = request.args.get('new_price', type=str)
    if cafe:
        cafe.coffee_price = updated_price
        db.session.commit()
        return jsonify(response={"success": "Successfully patched the data for cafe."}), 200
    else:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe with the given id in the database."
        }), 404


# HTTP DELETE - Delete Record
@app.route("/report_closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get('api_key')
    if api_key == API_KEY:
        closed_cafe = db.session.query(Cafe).filter_by(id=cafe_id).first()
        if closed_cafe:
            db.session.delete(closed_cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the data for closed cafe."}), 200
        else:
            return jsonify(error={
                "Not Found": "Sorry, we don't have a cafe with the given id in the database."
            }), 404
    else:
        return jsonify(error={
            "Key Error": "Sorry, you have no admin access. Make sure your api_key is correct."
        }), 403


if __name__ == '__main__':
    app.run(debug=True)
