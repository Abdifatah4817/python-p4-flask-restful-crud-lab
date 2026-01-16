#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant  # Make sure Plant model exists in models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# ----------------- Routes -----------------

class Plants(Resource):
    def get(self):
        plants = [p.to_dict() for p in Plant.query.all()]
        return make_response(plants, 200)

    def post(self):
        new_plant = Plant(
            name=request.form['name'],
            image=request.form['image'],
            price=float(request.form['price']),
            is_in_stock=request.form.get('is_in_stock', 'true') == 'true'
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        return make_response(plant.to_dict(), 200)

    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        data = request.get_json()
        for key, value in data.items():
            setattr(plant, key, value)
        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        db.session.delete(plant)
        db.session.commit()
        return '', 204  # No Content

api.add_resource(PlantByID, '/plants/<int:id>')

# ----------------- Run Server -----------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)
