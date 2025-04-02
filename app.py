"""
RESTful API Backend for Salary Prediction

This Flask application exposes an API endpoint:
    /predict/salary/<board_name>/<postingid>

It uses a trained machine learning model to predict salaries based on job posting features.
The model takes into account experience, education, location, and job title to make predictions.

Usage:
    Run this script using Python:
        python app.py
    The Flask development server will start on port 5000 by default.
"""

import json
import traceback
from flask import Flask, jsonify, abort, make_response, request
from data_processor import DataProcessor
from model_trainer import SalaryPredictor

app = Flask(__name__)

# Initialize the data processor and model
data_processor = DataProcessor()
salary_predictor = SalaryPredictor()

# Load the trained model
if not salary_predictor.load_model():
    app.logger.warning("No trained model found. Please train the model first.")

@app.route('/predict/salary/<board_name>/<postingid>', methods=['POST'])
def predict_salary(board_name, postingid):
    """
    Predicts the salary for a given job posting using the trained model.

    Args:
        board_name (str): The name of the job board.
        postingid (str): The unique identifier for the posting.
        JSON body: Contains job posting features (experience, education, location, title)

    Returns:
        JSON: A JSON object containing the predicted salary and confidence metrics.
    """
    if not request.is_json:
        abort(400, description="Request must be JSON")
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['experience', 'education', 'location', 'title']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields")
    
    try:
        # Transform the input data
        X = data_processor.transform_single_posting(data)
        
        # Make prediction
        predicted_salary = salary_predictor.predict(X)[0]
        
        return jsonify({
            "board_name": board_name,
            "postingid": postingid,
            "predicted_salary": f"${predicted_salary:,.2f}",
            "features": data
        })
    
    except Exception as e:
        app.logger.error(f"Error making prediction: {e}")
        app.logger.error(traceback.format_exc())
        abort(500, description=f"Error making prediction: {str(e)}")

@app.route('/train', methods=['POST'])
def train_model():
    """
    Endpoint to train the salary prediction model using provided data.
    
    Returns:
        JSON: Training results including model performance metrics.
    """
    if not request.is_json:
        abort(400, description="Request must be JSON")
    
    data = request.get_json()
    
    if 'data_file' not in data:
        abort(400, description="Missing data_file in request")
    
    try:
        app.logger.info(f"Starting model training with data file: {data['data_file']}")
        
        # Prepare data for training
        app.logger.info("Preparing data...")
        X_train, X_test, y_train, y_test = data_processor.prepare_data(data['data_file'])
        app.logger.info(f"Data prepared. Training set size: {len(X_train)}, Test set size: {len(X_test)}")
        
        # Train the model
        app.logger.info("Training model...")
        salary_predictor.train(X_train, y_train)
        
        # Evaluate the model
        app.logger.info("Evaluating model...")
        metrics = salary_predictor.evaluate(X_test, y_test)
        
        return jsonify({
            "message": "Model trained successfully",
            "metrics": metrics
        })
    
    except Exception as e:
        app.logger.error(f"Error training model: {e}")
        app.logger.error(traceback.format_exc())
        abort(500, description=f"Error training model: {str(e)}")

@app.errorhandler(404)
def not_found(error):
    """Custom error handler for 404 errors."""
    return make_response(jsonify({"message": error.description}), 404)

@app.errorhandler(400)
def bad_request(error):
    """Custom error handler for 400 errors."""
    return make_response(jsonify({"message": error.description}), 400)

@app.errorhandler(500)
def internal_error(error):
    """Custom error handler for 500 errors."""
    return make_response(jsonify({"message": error.description}), 500)

if __name__ == '__main__':
    app.run(debug=True)
