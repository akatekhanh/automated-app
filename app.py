import ast
import os
from flask import Flask, jsonify, render_template, request
import redis
from rq import Queue, Worker
from db import create_connection, create_table

from negotiation import process_data
from new_negotiation import process

app = Flask(__name__)
redis_connection = redis.Redis(host=os.getenv('REDIS'), port=6379)
queue = Queue(connection=redis_connection, default_timeout=3600)


# Create the SQLite table within the app context
with app.app_context():
    # Connect to SQLite3 database
    conn = create_connection()
    create_table(conn)


@app.route('/old', methods=['GET', 'POST'])
def home():
    conn = create_connection()
    cursor = conn.cursor()
    # Retrieve data from the table
    cursor.execute('SELECT * FROM negotiation_results ORDER BY id DESC LIMIT 1')

    data = cursor.fetchone()

    processed_data = None
    if data:
        zipped_data = zip(ast.literal_eval((data[3])), ast.literal_eval(data[4]))
        processed_data = {
            "id": data[0],
            "a1_utility": data[1],
            "a2_utility": data[2],
            "data": [item for item in zipped_data],
            "winner": data[6],
            "result": data[5],
            "a1_steps": data[7],
            "a2_steps": data[8]
        }
    # Close the connection
    conn.close()
    return render_template('home.html', result=processed_data)



@app.route('/process', methods=['POST'])
def process_app():
    data = request.json
    try:
        queue.enqueue(process_data, int(data['agent_1']), int(data['agent_2']))
    except Exception as e:
        raise EnvironmentError(f"Error when processing the queue {e}")
    return jsonify({'status': True})


@app.route('/', methods=['GET'])
def run():
    return render_template('new_negotiator.html', result=None)


@app.route('/process_new', methods=['POST'])
def process_new():
    data = request.json
    try:
       processed_data = process(int(data['n_steps'])) 
    except Exception as e:
        raise EnvironmentError(f"Error when processing the queue {e}")
    return jsonify(processed_data)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
