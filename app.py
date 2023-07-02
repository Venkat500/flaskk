from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['people']
energy_consumption = db['energyConsumption']

@app.route('/')
def hello():
    return 'Hello, World!'

# Get all energy consumption records
@app.route('/energy', methods=['GET'])
def get_energy_consumption():
    records = []
    for record in energy_consumption.find():
        records.append({
            'id': str(record['_id']),
            'consumption': record['consumption'],
            'time': record['time'],
            'cost': record['cost']
        })
    return render_template('energy.html', records=records)

# Get a specific energy consumption record by ID
@app.route('/energy/<record_id>', methods=['GET'])
def get_energy_record(record_id):
    record = energy_consumption.find_one({'_id': ObjectId(record_id)})
    if record:
        return jsonify({
            'id': str(record['_id']),
            'consumption': record['consumption'],
            'time': record['time'],
            'cost': record['cost']
        })
    else:
        return jsonify({'error': 'Record not found'}), 404

# Create a new energy consumption record
@app.route('/energy', methods=['POST'])
def create_energy_record():
    data = request.get_json()
    record = {
        'consumption': data['consumption'],
        'time': data['time'],
        'cost': data['cost']
    }
    result = energy_consumption.insert_one(record)
    return jsonify({'id': str(result.inserted_id)}), 201

# Update an energy consumption record
@app.route('/energy/<record_id>', methods=['PUT'])
def update_energy_record(record_id):
    data = request.get_json()
    updated_record = {
        'consumption': data['consumption'],
        'time': data['time'],
        'cost': data['cost']
    }
    result = energy_consumption.update_one({'_id': ObjectId(record_id)}, {'$set': updated_record})
    if result.modified_count == 1:
        return jsonify({'message': 'Record updated successfully'})
    else:
        return jsonify({'error': 'Record not found'}), 404

# Delete an energy consumption record
@app.route('/energy/<record_id>', methods=['DELETE'])
def delete_energy_record(record_id):
    result = energy_consumption.delete_one({'_id': ObjectId(record_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Record deleted successfully'})
    else:
        return jsonify({'error': 'Record not found'}), 404

# Process an energy consumption record
@app.route('/process', methods=['POST'])
def process_data():
    # Get the request data
    data = request.get_json()

    # Retrieve data from the 'energyConsumption' collection
    record_id = data.get('record_id')  # Assuming the client sends the record ID

    record = energy_consumption.find_one({'_id': ObjectId(record_id)})
    if record:
        # Modify the retrieved data as needed
        modified_cost = record['cost'] * 10  # Multiply the cost by 10

        # Add the modified data to a new collection (e.g., 'processedData')
        processed_collection = db['processedData']
        result = processed_collection.insert_one({'cost': modified_cost})

        # Return the result of the insertion
        return jsonify({'id': str(result.inserted_id)}), 201

    else:
        return jsonify({'error': 'Record not found'}), 404


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
