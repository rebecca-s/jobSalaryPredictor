# jobSalaryPredictor
## Installation
### Repo Clone
```commandline
git clone https://github.com/rebecca-s/jobSalaryPredictor.git
```


### Install Dependencies
Use pip to install Flask:
```commandline
pip install flask
```

## API Endpoint

The API exposes the following endpoint:
```commandline
/predict/salary/<board_name>/<postingid>
```

### Example API Call

```commandline
GET /predict/salary/cohere/e3cb621a-75b8-467c-803c-4325fb0c1301
```


**Example Response:**

```json
{
  "role": "Software Engineer",
  "salary": "$100,000"
}
```

If no matching record is found, the API returns a 404 error with a JSON message:
```json
{
  "message": "Posting not found"
}

```

## Running the Flask App
To start the Flask development server, run:

```commandline
python app.py
```
The server will start on port 5000 by default. You can access the API by navigating to:
```commandline
http://127.0.0.1:5000/predict/salary/cohere/e3cb621a-75b8-467c-803c-4325fb0c1301
```
### Running the Unit Tests
Unit tests are provided in the test_app.py file. To run the tests and see the success summary, execute:
```commandline
python test_app.py
```
