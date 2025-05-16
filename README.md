# currency-converter-project

## Description

This is a currency converter project that uses the Frankfurter API to convert currencies.

## Technologies

- Python 3.13
- FastAPI
- Aiohttp
- Limits
- Pydantic
- Uvicorn

## Setup

1. Fork and Clone the repository `git clone https://github.com/your-username/currency-converter-project.git`
2. Navigate to the project directory `cd currency-converter-project`
3. Install dependencies `uv sync`
4. Run the application `uv run uvicorn app.main:app --reload`



## Authentication

The API uses an API key for authentication. The API key should be passed in the header as `X-API-Key`. The API key is generated when a user is created. The API key is unique to each user.

## Rate Limiting

The API has a rate limit of 10 requests per minute per user. If the rate limit is exceeded, the API will return a 429 status code.

## Credits

The API has a subscription credit system. Each user starts with 10 credits. Each request costs 1 credit. If the user runs out of credits, the API will return a 403 status code.

## Usage

1. Create a user with a username and password endpoint `/users/`
2. Get currencies endpoint `/currencies/`
3. Get currency rates endpoint `/conversions/`. The base currency should be in the format `USD` and the target currency should be in the format `EUR`.
4. Get historical currency rates endpoint `/historical-rates/{date}`
5. Get historical currency rates endpoint with base currency and target currency `/historical-rates/{date}?base_currency={base_currency}&target_currency={target_currency}`. If no base currency or target currency is provided, the default is USD to EUR. The date should be in the format `YYYY-MM-DD`.
6. Get all users endpoint `/users/`


## Example Requests

```bash
# Create a user
POST http://localhost:8000/users/
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpassword"
}

# Get currencies
GET http://localhost:8000/currencies/

# Get currency rates
GET http://localhost:8000/conversions/

{
    "base_currency": "USD",
    "target_currency": "EUR"
}


# Get historical currency rates
GET http://localhost:8000/historical-rates/2023-01-01

# Get historical currency rates with base currency and target currency
GET http://localhost:8000/historical-rates/2023-01-01?base_currency=USD&target_currency=EUR

# Get all users
GET http://localhost:8000/users/

No authentication required for this endpoint.
```


## API Documentation

The API documentation can be found at `http://localhost:8000/docs`

## Testing

The API can be tested using the `test.py` file.

## License

MIT