"""
Unit Tests for the Salary Prediction API

This script uses Python's built-in unittest framework to test the Flask API.
It tests both the model training endpoint and the salary prediction endpoint.
"""

import unittest
import json
import os
from app import app

class TestResult(unittest.TextTestResult):
    def printSummary(self):
        """Print a summary of the test results."""
        print(f"\nRan {self.testsRun} tests in {self.timeTaken:.3f}s")
        if self.wasSuccessful():
            print(f"OK - {self.testsRun}/{self.testsRun} tests passed")
        else:
            print(f"FAILED - {len(self.failures) + len(self.errors)}/{self.testsRun} tests failed")

class SalaryAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and test data."""
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Sample job posting data
        self.test_posting = {
            "experience": 5,
            "education": "Bachelor's Degree",
            "location": "San Francisco, CA",
            "title": "Senior Software Engineer"
        }
        
        # Sample training data file path
        self.test_data_file = "test_data.csv"
        
    def test_train_model(self):
        """Test the model training endpoint."""
        # Create a test data file with all required columns
        with open(self.test_data_file, 'w') as f:
            f.write("Id,Title,FullDescription,LocationRaw,LocationNormalized,ContractType,ContractTime,Company,Category,SalaryRaw,SalaryNormalized,SourceName\n")
            f.write("1,Senior Software Engineer,Looking for a Senior Software Engineer with 5+ years of experience in Python and web development.,San Francisco,CA,permanent,full_time,Test Company,IT Jobs,120000,120000,Test Source\n")
            f.write("2,Data Scientist,Seeking a Data Scientist with 3 years of experience in machine learning and data analysis.,New York,NY,permanent,full_time,Test Company,Data Science Jobs,100000,100000,Test Source\n")
            f.write("3,Frontend Developer,Frontend Developer with 2 years of experience in React and TypeScript.,Chicago,IL,permanent,full_time,Test Company,IT Jobs,90000,90000,Test Source\n")
            f.write("4,Backend Engineer,Backend Engineer with 4 years of experience in Java and Spring.,Boston,MA,permanent,full_time,Test Company,IT Jobs,110000,110000,Test Source\n")
            f.write("5,ML Engineer,Machine Learning Engineer with 6 years of experience in deep learning.,Seattle,WA,permanent,full_time,Test Company,Data Science Jobs,130000,130000,Test Source\n")
        
        # Test the training endpoint
        response = self.client.post('/train',
                                  json={"data_file": self.test_data_file},
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertIn("metrics", data)
        
        # Clean up test data file
        os.remove(self.test_data_file)
    
    def test_predict_salary(self):
        """Test the salary prediction endpoint."""
        # Test with valid data
        response = self.client.post('/predict/salary/testboard/123',
                                  json=self.test_posting,
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("predicted_salary", data)
        self.assertIn("features", data)
        
        # Test with missing fields
        invalid_posting = {
            "experience": 5,
            "education": "Bachelor's Degree"
        }
        
        response = self.client.post('/predict/salary/testboard/123',
                                  json=invalid_posting,
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Missing required fields", data.get("message", ""))
    
    def test_invalid_json(self):
        """Test handling of invalid JSON data."""
        response = self.client.post('/predict/salary/testboard/123',
                                  data="invalid json",
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("The browser (or proxy) sent a request that this server could not understand", data.get("message", ""))

if __name__ == '__main__':
    unittest.main(testResultClass=TestResult)
