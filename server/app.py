# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here


@app.route("/earthquakes/<int:id>")
def Earthquakes(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        earthquake_dict = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year

        }

        return make_response(earthquake_dict, 200)
    else:
        error_message = {'message': f'Earthquake {id} not found.'}
        return make_response(error_message, 404)


@ app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude).all()
    if earthquakes:
        earthquakes_list = [{
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year

        } for earthquake in earthquakes]
        response = {
            'count': len(earthquakes),
            'quakes': earthquakes_list
        }

        return make_response(response, 200)
    else:
        
        response = {
            'count': 0,
            'quakes': []
        }
             
    return make_response(response, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)