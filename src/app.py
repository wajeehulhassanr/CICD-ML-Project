import os
import joblib
import logging
from flask import render_template
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd

from utils import load_data, preprocess_data, evaluate_model
from model import train, test, predict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Default model path
MODEL_PATH = os.environ.get('MODEL_PATH', 'models/iris_model.joblib')
VERSION = os.environ.get('VERSION', 'v1.0.0')

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Iris Classification API',
        'version': VERSION
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

@app.route('/train', methods=['POST'])
def train_model():
    """Endpoint to train the model"""
    try:
        # Get parameters from request or use defaults
        params = request.get_json() or {}
        
        url = params.get('data_url', "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data")
        test_size = float(params.get('test_size', 0.2))
        model_params = params.get('model_params', None)
        
        # Load and preprocess data
        data = load_data(url)
        X_train, X_test, y_train, y_test = preprocess_data(data, test_size=test_size)
        
        # Train model
        model = train(X_train, y_train, model_params, model_path=MODEL_PATH)
        
        # Evaluate model
        accuracy = test(model, X_test, y_test)
        
        return jsonify({
            'status': 'success',
            'message': 'Model trained successfully',
            'model_path': MODEL_PATH,
            'accuracy': accuracy,
            'train_samples': X_train.shape[0],
            'test_samples': X_test.shape[0]
        })
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """Endpoint to make predictions"""
    try:
        # Check if model exists
        if not os.path.exists(MODEL_PATH):
            return jsonify({
                'status': 'error',
                'message': f'Model not found at {MODEL_PATH}. Train the model first.'
            }), 404
        
        # Load the model
        model = joblib.load(MODEL_PATH)
        
        # Get features from request
        features = request.get_json()
        
        if not features:
            return jsonify({
                'status': 'error',
                'message': 'No features provided'
            }), 400
        
        # Convert to numpy array
        if isinstance(features, list):
            # Single or multiple samples
            X = np.array(features)
            if X.ndim == 1:
                X = X.reshape(1, -1)  # Reshape single sample
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid input format. Expected list of features.'
            }), 400
        
        # Make predictions
        predictions = predict(model, X)
        
        return jsonify({
            'status': 'success',
            'predictions': predictions.tolist()
        })
    except Exception as e:
        logger.error(f"Error making predictions: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/info', methods=['GET'])
def model_info():
    """Endpoint to get model information"""
    try:
        if not os.path.exists(MODEL_PATH):
            return jsonify({
                'status': 'error',
                'message': f'Model not found at {MODEL_PATH}. Train the model first.'
            }), 404
        
        # Load the model
        model = joblib.load(MODEL_PATH)
        
        # Get model information
        model_info = {
            'model_type': type(model).__name__,
            'parameters': model.get_params(),
            'features_count': model.n_features_in_,
            'classes': model.classes_.tolist(),
            'model_path': MODEL_PATH,
            'version': VERSION
        }
        
        return jsonify({
            'status': 'success',
            'model_info': model_info
        })
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
        
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


