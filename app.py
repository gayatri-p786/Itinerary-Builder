import os
import json
import base64
from urllib.parse import quote_plus
from bson import ObjectId
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Load configuration from config.json
with open('config.json') as f:
    config = json.load(f)

# Generate a random secret key
secret_key = base64.b64encode(os.urandom(24)).decode('utf-8')

# MongoDB credentials
mongodb_username = config['mongodb']['username']
mongodb_password = config['mongodb']['password']

# Escape the username and password using quote_plus
escaped_username = quote_plus(mongodb_username)
escaped_password = quote_plus(mongodb_password)

# Construct the MongoDB URI connection string with escaped credentials
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.grxcm5a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(uri)
db = client.get_database("travel_itinerary_db")
itineraries_collection = db["itineraries"]

@app.route('/')
def index():
    # Fetch itineraries from MongoDB
    itineraries = itineraries_collection.find()
    return render_template('index.html', itineraries=itineraries)

@app.route('/add_itinerary')
def add_itinerary():
    return render_template('add_itinerary.html')

@app.route('/itinerary/<itinerary_id>', methods=['GET'])
def view_itinerary(itinerary_id):
    try:
        itinerary = itineraries_collection.find_one({'_id': ObjectId(itinerary_id)})
        if itinerary:
            return render_template('itinerary.html', itinerary=itinerary)
        else:
            return "Itinerary not found", 404
    except Exception as e:
        return str(e), 500

@app.route('/create_itinerary', methods=['POST'])
def create_itinerary():
    name = request.json.get('name')
    destinations = request.json.get('destinations')
    # Insert itinerary into MongoDB
    itinerary_data = {"name": name, "destinations": destinations}
    itineraries_collection.insert_one(itinerary_data)
    
    return redirect(url_for('index'))

@app.route('/edit_itinerary/<itinerary_id>', methods=['GET'])
def edit_itinerary(itinerary_id):
    itinerary = itineraries_collection.find_one({'_id': ObjectId(itinerary_id)})
    return render_template('edit_itinerary.html', itinerary=itinerary)

@app.route('/edit_itinerary/<itinerary_id>', methods=['PUT'])
def update_itinerary(itinerary_id):
    data = request.json
    name = data.get('name')
    destinations = data.get('destinations')
    itineraries_collection.update_one(
        {'_id': ObjectId(itinerary_id)},
        {'$set': {
            'name': name,
            'destinations': destinations
        }}
    )
    return jsonify({'status': 'success'}), 200

@app.route('/delete_itinerary/<itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    result = itineraries_collection.delete_one({'_id': ObjectId(itinerary_id)})
    if result.deleted_count == 1:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure'}), 404


if __name__ == '__main__':
    app.run(debug=True)
