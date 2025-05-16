from typing import Annotated
from fastapi import FastAPI, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from limits import parse
from limits.storage import storage_from_string
from limits.aio.strategies import FixedWindowRateLimiter

from . import models
from . import schemas
from frankfurter.rest_adapter import RestAdapter


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


frankfurter = RestAdapter() 

db = models.User()



memory = storage_from_string("async+memory://")
rate_limiter = FixedWindowRateLimiter(memory)
ten_per_minute = parse("10/minute")


def get_current_user(api_key: str = Header(..., alias="X-API-Key", description="Your API Key for authentication.")):
    user = db.get_user_by_api_key(api_key=api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key or User not found",
        )
    return user


@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserBase):

    if db.get_user_by_username(username=user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = db.add_user(username=user.username, password=user.password)
    return schemas.UserResponse.model_validate(user)    


@app.get("/users/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserResponse])
async def get_users() -> list[schemas.UserResponse]:
    return db.get_all_users()    


@app.get("/currencies/", status_code=status.HTTP_200_OK)
async def get_currencies(current_user: Annotated[schemas.UserResponse, Depends(get_current_user)]) -> dict:
    if current_user["credits"] < 1:
        raise HTTPException(status_code=403, detail="Not enough credits")

    window = await rate_limiter.get_window_stats(ten_per_minute, "subscriptions", current_user["id"])    
    remainder = window.remaining
    if remainder < 1:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    response = await frankfurter.get_currencies()
    if not response:
        raise HTTPException(status_code=404, detail="Currencies not found")
    
    await rate_limiter.hit(ten_per_minute, "subscriptions", current_user["id"])
    
    current_user["credits"] = current_user["credits"] - 1
    response = {
        "currencies": response,
        "credits": current_user["credits"],
    }    
    return response


@app.get("/conversions/", status_code=status.HTTP_200_OK)
async def get_currency_rates(conversion: schemas.Conversion, current_user: Annotated[schemas.UserResponse, Depends(get_current_user)]) -> dict:
    if current_user["credits"] < 1:
        raise HTTPException(status_code=403, detail="Not enough credits")
    
    window = await rate_limiter.get_window_stats(ten_per_minute, "subscriptions", current_user["id"])    
    remainder = window.remaining
    if remainder < 1:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    response = await frankfurter.get_currency_rates(base_currency=conversion.base_currency, target_currency=conversion.target_currency)
    if not response:
        raise HTTPException(status_code=404, detail="Currency rates not found")
    
    rate_limiter.hit(ten_per_minute, "subscriptions", current_user["id"])
    
    current_user["credits"] = current_user["credits"] - 1
    response = {
        "base_currency": conversion.base_currency,
        "target_currency": conversion.target_currency,
        "amount": conversion.amount,
        "rate": response["rates"][conversion.target_currency],
        "converted_amount": conversion.amount * response["rates"][conversion.target_currency],
        "credits": current_user["credits"]
    }

    return response


@app.get("/historical-rates/{date}", status_code=status.HTTP_200_OK)
async def get_historical_currency_rates(date: str, base_currency: str = None, target_currency: str = None, current_user: Annotated[schemas.UserResponse, Depends(get_current_user)] = None) -> dict:
    if current_user["credits"] < 1:
        raise HTTPException(status_code=403, detail="Not enough credits")
    
    window = await rate_limiter.get_window_stats(ten_per_minute, "subscriptions", current_user["id"])    
    remainder = window.remaining
    if remainder < 1:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    if not base_currency:
        base_currency = "USD"
    if not target_currency:
        target_currency = "EUR"
    
    response = await frankfurter.get_historical_currency_rates(date=date, base_currency=base_currency, target_currency=target_currency)
    if not response:
        raise HTTPException(status_code=404, detail="Historical currency rates not found")
    
    rate_limiter.hit(ten_per_minute, "subscriptions", current_user["id"])
    
    current_user["credits"] = current_user["credits"] - 1
    response = {
        "base_currency": base_currency,
        "date": date,
        "rates": response,
        "credits": current_user["credits"]
    }

    return response