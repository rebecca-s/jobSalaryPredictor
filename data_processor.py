import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import zipfile
import re
import traceback

class DataProcessor:
    def __init__(self):
        self.label_encoders = {}
        
    def load_data(self, filepath):
        """Load and preprocess the salary prediction dataset."""
        try:
            # Handle zip files
            if filepath.endswith('.zip'):
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    # Extract the first CSV file from the zip
                    csv_file = [f for f in zip_ref.namelist() if f.endswith('.csv')][0]
                    df = pd.read_csv(zip_ref.open(csv_file))
            else:
                df = pd.read_csv(filepath)
            
            # Print dataset information for debugging
            print("\nDataset Info:")
            print("Shape:", df.shape)
            print("\nColumns:", df.columns.tolist())
            print("\nSample of data:")
            print(df.head())
            
            # Extract years of experience from job description
            df['experience'] = df['FullDescription'].str.extract(r'(\d+)\+?\s*(?:year|yr)s?\s*(?:of\s*)?experience', flags=re.IGNORECASE)
            df['experience'] = pd.to_numeric(df['experience'], errors='coerce').fillna(0)
            
            # Use Title as the job title
            df['title'] = df['Title'].fillna('Unknown')
            
            # Use LocationNormalized as the location
            df['location'] = df['LocationNormalized'].fillna('Unknown')
            
            # Extract education level from description
            education_keywords = {
                'Bachelor': 'Bachelor\'s Degree',
                'Master': 'Master\'s Degree',
                'PhD': 'PhD',
                'Doctorate': 'PhD',
                'High School': 'High School',
                'Associate': 'Associate\'s Degree'
            }
            
            def extract_education(desc):
                if pd.isna(desc):
                    return 'Unknown'
                desc = desc.lower()
                for keyword, level in education_keywords.items():
                    if keyword.lower() in desc:
                        return level
                return 'Unknown'
            
            df['education'] = df['FullDescription'].apply(extract_education)
            
            # Use SalaryNormalized as the salary
            df['salary'] = df['SalaryNormalized'].fillna(0)
            
            return df
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            print("Traceback:", traceback.format_exc())
            raise
    
    def preprocess_features(self, df):
        """Preprocess features for model training."""
        try:
            # Create feature matrix
            features = ['experience', 'education', 'location', 'title']
            X = df[features].copy()
            
            # Encode categorical variables
            for col in ['education', 'location', 'title']:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
            
            return X
            
        except Exception as e:
            print(f"Error preprocessing features: {str(e)}")
            print("Traceback:", traceback.format_exc())
            raise
    
    def prepare_data(self, filepath):
        """Prepare data for model training."""
        try:
            # Load data
            df = self.load_data(filepath)
            
            # Preprocess features
            X = self.preprocess_features(df)
            y = df['salary']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            print(f"Error preparing data: {str(e)}")
            print("Traceback:", traceback.format_exc())
            raise
    
    def transform_single_posting(self, posting_data):
        """Transform a single job posting for prediction."""
        try:
            # Create a DataFrame with the posting data
            df = pd.DataFrame([posting_data])
            
            # Preprocess features
            X = self.preprocess_features(df)
            
            return X
            
        except Exception as e:
            print(f"Error transforming posting: {str(e)}")
            print("Traceback:", traceback.format_exc())
            raise 