import joblib
import logging
from sklearn.ensemble import RandomForestClassifier
import os
import pytest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@pytest.mark.skip(reason="Not a test function")
def test(model, X_test, y_test):
    """
    Test the model and return accuracy
    
    Args:
        model: trained model
        X_test: test features
        y_test: test labels
        
    Returns:
        accuracy score
    """
    try:
        logger.info("Testing model...")
        accuracy = model.score(X_test, y_test)
        logger.info(f"Test accuracy: {accuracy:.4f}")
        return accuracy
    except Exception as e:
        logger.error(f"Error testing model: {str(e)}")
        raise

def train(X_train, y_train, model_params=None, model_path='model.joblib'):
    """
    Train a RandomForest classifier
    
    Args:
        X_train: training features
        y_train: training labels
        model_params: parameters for RandomForestClassifier
        model_path: path to save the model
        
    Returns:
        trained model
    """
    try:
        logger.info("Training RandomForest classifier...")
        
        if model_params is None:
            model_params = {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': 42
            }
        
        model = RandomForestClassifier(**model_params)
        model.fit(X_train, y_train)
        
        # Save the model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
        
        return model
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise

def evaluate_model(model, X_test, y_test):
    """
    Test the model and return accuracy
    
    Args:
        model: trained model
        X_test: test features
        y_test: test labels
        
    Returns:
        accuracy score
    """
    try:
        logger.info("Testing model...")
        accuracy = model.score(X_test, y_test)
        logger.info(f"Test accuracy: {accuracy:.4f}")
        return accuracy
    except Exception as e:
        logger.error(f"Error testing model: {str(e)}")
        raise

def predict(model, X, model_path=None):
    """
    Make predictions using the model
    
    Args:
        model: trained model or None if model_path is provided
        X: features to predict
        model_path: path to load the model from (if model is None)
        
    Returns:
        predicted classes
    """
    try:
        logger.info("Making predictions...")
        
        # Load model if not provided
        if model is None and model_path is not None:
            logger.info(f"Loading model from {model_path}")
            model = joblib.load(model_path)
        
        if model is None:
            raise ValueError("Either model or model_path must be provided")
        
        predictions = model.predict(X)
        logger.info(f"Generated {len(predictions)} predictions")
        return predictions
    except Exception as e:
        logger.error(f"Error making predictions: {str(e)}")
        raise

def get_feature_importance(model, feature_names):
    """
    Get feature importance from the model
    
    Args:
        model: trained model
        feature_names: list of feature names
        
    Returns:
        dictionary of feature importances
    """
    try:
        importances = model.feature_importances_
        feature_importance = dict(zip(feature_names, importances))
        logger.info("Feature importance calculated")
        return feature_importance
    except Exception as e:
        logger.error(f"Error getting feature importance: {str(e)}")
        raise
