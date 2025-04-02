"""
RESTful API Backend for Salary Prediction

This Flask application exposes an API endpoint:
    /predict/salary/<board_name>/<postingid>

It reads sample data from a JSON file (sample_data.json) to provide a mocked salary prediction.
If a matching board_name and postingid are found in the sample data, the API returns the
associated role and salary. Otherwise, a JSON formatted 404 error is returned.

Usage:
    Run this script using Python:
        python app.py
    The Flask development server will start on port 5000 by default.
"""

import json
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

def load_sample_data(filepath='sample_data.json'):
    """
    Loads the sample data from a JSON file.

    Args:
        filepath (str): The path to the JSON file containing sample data.

    Returns:
        list: A list of dictionaries representing sample data.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data.get('data', [])
    except Exception as e:
        app.logger.error(f"Error loading sample data: {e}")
        return []

# Load the sample data from the JSON file.
sample_data = load_sample_data()

@app.route('/predict/salary/<board_name>/<postingid>', methods=['GET'])
def predict_salary(board_name, postingid):
    """
    Predicts the salary for a given board and posting ID using sample data from a JSON file.

    Args:
        board_name (str): The name of the job board.
        postingid (str): The unique identifier for the posting.

    Returns:
        JSON: A JSON object containing the role and salary information if found.
              Otherwise, a JSON formatted 404 error is returned.
    """
    # Search for a matching record in the sample data.
    for data in sample_data:
        if data["board_name"] == board_name and data["postingid"] == postingid:
            return jsonify({"role": data["role"], "salary": data["salary"]})

    # If no matching record is found, return a 404 error.
    abort(404, description="Posting not found")

@app.errorhandler(404)
def not_found(error):
    """
    Custom error handler for 404 errors. Returns a JSON response.

    Args:
        error: The error object.

    Returns:
        Response: A JSON response with the error message.
    """
    return make_response(jsonify({"message": error.description}), 404)

if __name__ == '__main__':
    # Run the Flask development server with debug mode enabled.
    app.run(debug=True)
