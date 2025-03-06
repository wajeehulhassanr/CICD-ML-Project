import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import logging
import requests
from io import StringIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_data(url="https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"):
    """
    Load the Iris dataset from UCI repository
    
    Args:
        url: URL to the dataset
        
    Returns:
        pandas DataFrame with the dataset
    """
    try:
        logger.info(f"Downloading data from {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # The Iris dataset doesn't have column names in the file
        column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
        data = pd.read_csv(StringIO(response.text), header=None, names=column_names)
        
        logger.info(f"Successfully loaded dataset with shape {data.shape}")
        return data
    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        raise

def preprocess_data(data, test_size=0.2, random_state=42):
    """
    Preprocess the dataset and split into training and testing sets
    
    Args:
        data: pandas DataFrame with the dataset
        test_size: proportion of the dataset to include in the test split
        random_state: random seed for reproducibility
        
    Returns:
        X_train, X_test, y_train, y_test: split data
    """
    try:
        logger.info("Preprocessing data and splitting into train/test sets")
        
        # Separate features and target
        X = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(f"Error preprocessing data: {str(e)}")
        raise

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model on test data
    
    Args:
        model: trained model
        X_test: test features
        y_test: test labels
        
    Returns:
        accuracy: model accuracy
    """
    try:
        accuracy = model.score(X_test, y_test)
        logger.info(f"Model accuracy: {accuracy:.4f}")
        return accuracy
    except Exception as e:
        logger.error(f"Error evaluating model: {str(e)}")
        raise
