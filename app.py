"""Flask app for Cupcakes"""

import os

from flask import Flask, jsonify, request

from models import connect_db, db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")

connect_db(app)

@app.get("/api/cupcakes")
def get_cupcakes():
    """Retrieve data about all cupcakes and respond with JSON"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """
    Retrieve data about a single cupcake
    Respond with JSON like: {cupcake: {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post("/api/cupcakes")
def create_cupcake():
    """
    Create a cupcake
    Respond with JSON like: {cupcake: {id, flavor, size, rating, image_url}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json["image_url"] or None

    cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image_url = image_url
    )

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)