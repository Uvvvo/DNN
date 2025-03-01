import unittest
from data_processing import load_data, preprocess_data

class TestPreprocessing(unittest.TestCase):
    def test_preprocess_data(self):
        data = load_data('historical_data.csv')
        X, y, scaler, le = preprocess_data(data)
        self.assertGreater(len(X), 0)  # التأكد من وجود بيانات

if __name__ == "__main__":
    unittest.main()