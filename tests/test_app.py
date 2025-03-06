import os
import sys
import unittest
import numpy as np
import tempfile
from unittest.mock import patch, MagicMock

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_data, preprocess_data
from src.model import train, evaluate_model, predict

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    @patch('src.utils.requests.get')
    def test_load_data(self, mock_get):
        """Test data loading"""
        # Mock response
        mock_response = MagicMock()
        mock_response.text = "5.1,3.5,1.4,0.2,Iris-setosa\n" \
                             "4.9,3.0,1.4,0.2,Iris-setosa\n" \
                             "6.3,3.3,6.0,2.5,Iris-virginica"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        data = load_data()
        
        self.assertEqual(data.shape, (3, 5))
        self.assertEqual(list(data.columns), ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class'])
    
    def test_preprocess_data(self):
        """Test data preprocessing"""
        # Create sample data with at least 2 of each class
        import pandas as pd
        data = pd.DataFrame({
            'sepal_length': [5.1, 4.9, 6.3, 5.8, 7.1, 5.7],
            'sepal_width': [3.5, 3.0, 3.3, 2.7, 3.0, 2.8],
            'petal_length': [1.4, 1.4, 6.0, 5.1, 5.9, 4.1],
            'petal_width': [0.2, 0.2, 2.5, 1.9, 2.1, 1.3],
            'class': ['Iris-setosa', 'Iris-setosa', 'Iris-virginica', 'Iris-versicolor', 'Iris-virginica', 'Iris-versicolor']
        })
        
        X_train, X_test, y_train, y_test = preprocess_data(data, test_size=0.4, random_state=42)
        
        # Check total number of samples
        self.assertEqual(X_train.shape[0] + X_test.shape[0], 6)
        self.assertEqual(len(y_train) + len(y_test), 6)
        
        # Check approximate split
        self.assertTrue(2 <= X_test.shape[0] <= 3)
        self.assertTrue(3 <= X_train.shape[0] <= 4)

class TestModel(unittest.TestCase):
    """Test model functions"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for model
        self.temp_dir = tempfile.TemporaryDirectory()
        self.model_path = os.path.join(self.temp_dir.name, 'test_model.joblib')
        
        # Create sample data
        np.random.seed(42)
        self.X_train = np.random.random((20, 4))
        self.y_train = np.array(['Iris-setosa'] * 10 + ['Iris-versicolor'] * 10)
        self.X_test = np.random.random((10, 4))
        self.y_test = np.array(['Iris-setosa'] * 5 + ['Iris-versicolor'] * 5)
    
    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()
    
    def test_train_and_test(self):
        """Test model training and testing"""
        # Train model
        model = train(self.X_train, self.y_train, model_path=self.model_path)
        
        # Check if model file exists
        self.assertTrue(os.path.exists(self.model_path))
        
        # Test model
        accuracy = evaluate_model(model, self.X_test, self.y_test)
        
        # Check if accuracy is a float between 0 and 1
        self.assertIsInstance(accuracy, float)
        self.assertTrue(0 <= accuracy <= 1)
    
    def test_predict(self):
        """Test model prediction"""
        # Train model
        model = train(self.X_train, self.y_train, model_path=self.model_path)
        
        # Make predictions
        predictions = predict(model, self.X_test[:3])
        
        # Check predictions
        self.assertEqual(len(predictions), 3)
        self.assertTrue(all(pred in ['Iris-setosa', 'Iris-versicolor'] for pred in predictions))
        
        # Test prediction with model path
        predictions2 = predict(None, self.X_test[:3], model_path=self.model_path)
        self.assertEqual(len(predictions2), 3)

if __name__ == '__main__':
    unittest.main()
