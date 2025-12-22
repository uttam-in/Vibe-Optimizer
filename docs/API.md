# API Documentation

## Base URL
`http://localhost:8000/api/v1`

## Endpoints

### Sentiment

#### GET /sentiment/trends
Get sentiment trends over time.

**Query Parameters:**
- `start_date` (optional): ISO datetime
- `end_date` (optional): ISO datetime
- `source_type` (optional): twitter, reddit, reviews

**Response:**
```json
{
  "trends": [
    {
      "period_start": "2024-01-01T00:00:00",
      "period_end": "2024-01-02T00:00:00",
      "sentiment_distribution": {
        "positive": 120,
        "neutral": 45,
        "negative": 35
      },
      "average_intensity": 0.72
    }
  ]
}
```

#### GET /sentiment/distribution
Get current sentiment distribution.

### Insights

#### GET /insights/
Get generated insights.

**Query Parameters:**
- `insight_type` (optional): trend, risk, opportunity, complaint
- `severity` (optional): low, medium, high, critical
- `limit` (optional): default 10

#### GET /insights/{insight_id}
Get detailed insight information.

### Reports

#### POST /reports/generate
Generate a new report.

**Body:**
```json
{
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-01-07T23:59:59",
  "format": "html"
}
```

#### GET /reports/latest
Get the most recent report.
