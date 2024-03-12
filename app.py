from flask import Flask, jsonify, request
import psycopg2
import queries
from flask_cors import CORS
# import mysql.connector

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Allow requests from the React frontend

try:
    connection = psycopg2.connect(
        dbname="alleventsdb",
        user="root",
        password="VIFDIcP2e3VxrZ4ZhLOMCcFdGTQDDbI8",
        host="dpg-cno4m7tjm4es73cf7a50-a.oregon-postgres.render.com",
        port="5432",
    )
    print("Connected successfully!")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")


@app.after_request
def add_headers(response):
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    return response

@app.route('/api/data', methods=['GET'])
def get_data():
    print("inside method call.......")
    cursor = connection.cursor()
    cursor.execute(queries.FETCH_EVENT_DETAILS)
    data = cursor.fetchall()
    cursor.close()
    print("featched...",data)
    return jsonify(data)

@app.route('/api/create/event', methods=['POST'])
def create_event():
    try:
        event_data = request.json
        # Check if an event with the same name already exists
        cursor = connection.cursor()
        cursor.execute(queries.CHECK_EVENT_BY_NAME, (event_data['name'],))
        existing_event = cursor.fetchone()
        cursor.close()
        if existing_event:
            return jsonify({'error': 'Event with the same name already exists'}), 400
        
        # If event with the same name does not exist, proceed with creating the new event
        cursor = connection.cursor()
        cursor.execute(queries.CREATE_NEW_EVENT, (
            event_data['name'],
            event_data['starttime'],
            event_data['endtime'],
            event_data['location'],
            event_data['description'],
            event_data['category'],
            event_data['bannerImage']
        ))
        connection.commit()
        cursor.close()
        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        print(e)  # Print the caught exception for debugging
        return jsonify({'error': 'Failed to create event', 'details': str(e)}), 500



@app.route('/api/events/delete/<string:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        cursor = connection.cursor()
        cursor.execute(queries.FETCH_EVENT_BY_ID, (event_id,))
        event = cursor.fetchone()
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        cursor.execute(queries.DELETE_EVENT_BY_ID, (event_id,))
        connection.commit()
        cursor.close()
        return jsonify({'message': 'Event deleted successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to delete event', 'details': str(e)}), 500

@app.route('/api/events/update/<string:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        event_data = request.json
        cursor = connection.cursor()
        cursor.execute(queries.FETCH_EVENT_BY_ID, (event_id,))
        existing_event = cursor.fetchone()
        if not existing_event:
            return jsonify({'error': 'Event not found'}), 404
        cursor.execute(queries.UPDATE_EVENT, (
            event_data['name'],
            event_data['starttime'],
            event_data['endtime'],
            event_data['location'],
            event_data['description'],
            event_data['category'],
            event_data['bannerImage'],
            event_id
        ))
        connection.commit()
        cursor.close()
        return jsonify({'message': 'Event updated successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to update event', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
