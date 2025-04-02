# Salary Prediction API

A machine learning-based API for predicting salaries based on job posting features. The API uses a Random Forest model trained on job posting data to make salary predictions.

## Features

- Salary prediction based on job posting features
- Model training endpoint
- RESTful API design
- Comprehensive test suite

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rebecca-s/jobSalaryPredictor.git
cd <your-repo-folder>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Download the training data:
    - Visit [Kaggle Job Salary Prediction Dataset](https://www.kaggle.com/c/job-salary-prediction/data)
    - Download the `Train_rev1.zip` file
    - Extract the `Train_rev1.csv` file to the project root directory
    - Note: You'll need to create a Kaggle account and accept the competition rules to download the data

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Train the model:
```bash
curl -X POST http://localhost:5000/train \
     -H "Content-Type: application/json" \
     -d '{"data_file": "job-salary-prediction-training-data/Train_rev1.zip"}'
```
if you are on windows:
```bash
Invoke-RestMethod -Uri "http://localhost:5000/train" -Method Post -ContentType "application/json" -Body '{"data_file":"job-salary-prediction-training-data/Train_rev1.zip"}'
```
3. Make salary predictions:
```bash
curl -X POST http://localhost:5000/predict/salary/board_name/posting_id \
     -H "Content-Type: application/json" \
     -d '{
           "experience": 5,
           "education": "Bachelor'\''s Degree",
           "location": "San Francisco, CA",
           "title": "Senior Software Engineer"
         }'
```
if you are on windows:
```
$body = @{
    experience = 5
    education = "Bachelor's Degree"
    location = "London"
    title = "Software Engineer"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/predict/salary/testboard/123" -Method Post -ContentType "application/json" -Body $body
```

## API Endpoints

### POST /train
Trains the salary prediction model using provided data.

Request body:
```json
{
    "data_file": "path/to/your/data.csv"
}
```

### POST /predict/salary/<board_name>/<postingid>
Predicts salary for a job posting.

Request body:
```json
{
    "experience": 5,
    "education": "Bachelor's Degree",
    "location": "San Francisco, CA",
    "title": "Senior Software Engineer"
}
```

## Testing

Run the test suite:
```bash
python -m unittest test_app.py
```

## Data Format

### Training Data Format
The training data should be in CSV format with the following columns:
- `Id`: Unique identifier for the job posting
- `Title`: Job title
- `FullDescription`: Complete job description
- `LocationRaw`: Raw location text
- `LocationNormalized`: Standardized location name
- `ContractType`: Type of contract (e.g., permanent, contract)
- `ContractTime`: Time basis (e.g., full-time, part-time)
- `Company`: Company name
- `Category`: Job category
- `SalaryRaw`: Raw salary text
- `SalaryNormalized`: Standardized salary value
- `SourceName`: Source of the job posting

### Prediction Input Format
When making predictions, provide the following fields:
- `experience`: Number of years of experience (integer)
- `education`: Education level (must be one of):
    - "Bachelor's Degree"
    - "Master's Degree"
    - "PhD"
    - "High School"
    - "Associate's Degree"
    - "Unknown"
- `location`: Job location (city or region)
- `title`: Job title

## License

MIT License
