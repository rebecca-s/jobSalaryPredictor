"""
Unit Tests for the Salary Prediction API

This script uses Python's built-in unittest framework to test the Flask API.
It tests both a valid request (where sample data is found) and an invalid request
(where no matching record exists). After running the tests, it prints a summary
of the number of tests passed out of the total.
"""

import unittest
from app import app

class SalaryAPITestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app for testing and set up a test client.
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_valid_salary_prediction(self):
        """
        Test that a valid board_name and postingid return the expected salary data.
        """
        response = self.client.get('/predict/salary/cohere/e3cb621a-75b8-467c-803c-4325fb0c1301')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['role'], "Software Engineer")
        self.assertEqual(data['salary'], "$100,000")

    def test_invalid_salary_prediction(self):
        """
        Test that an invalid board_name or postingid returns a 404 error.
        """
        response = self.client.get('/predict/salary/invalid/unknown')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("Posting not found", data.get("message", ""))

if __name__ == '__main__':
    # Create a test suite from the test case.
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SalaryAPITestCase)
    # Run the test suite.
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    # Calculate the number of tests passed.
    total_tests = result.testsRun
    # Passed tests: total tests minus failures and errors.
    passed_tests = total_tests - len(result.failures) - len(result.errors)
    print(f"\nSuccess: {passed_tests}/{total_tests}")
