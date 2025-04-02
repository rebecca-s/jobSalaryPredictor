# jobSalaryPredictor


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
