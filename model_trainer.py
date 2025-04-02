from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class SalaryPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model_path = 'models/salary_predictor.joblib'
        
    def train(self, X_train, y_train):
        """Train the salary prediction model."""
        self.model.fit(X_train, y_train)
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save the trained model
        joblib.dump(self.model, self.model_path)
        
    def evaluate(self, X_test, y_test):
        """Evaluate the model's performance."""
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        return {
            'mse': mse,
            'rmse': mse ** 0.5,
            'r2': r2
        }
    
    def load_model(self):
        """Load a trained model from disk."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False
    
    def predict(self, X):
        """Make salary predictions for new job postings."""
        return self.model.predict(X) 