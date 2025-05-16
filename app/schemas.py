from typing import Dict, List
from pydantic import BaseModel, Field
import datetime

class UserBase(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    api_key: str = Field(..., description="API key")
    is_active: bool = Field(..., description="Is active")
    created_at: datetime.datetime = Field(..., description="Created at")
    credits: int = Field(..., description="Credits")


class Currencies(BaseModel):
    currencies: Dict[str, float] = Field(..., description="Currencies")
    credits: int = Field(..., description="Credits")


class Conversion(BaseModel):
    base_currency: str = Field(..., description="Currency code")
    target_currency: str = Field(..., description="Currency name")
    amount: float = Field(..., description="Currency amount")


class Historical(BaseModel):
    date: str = Field(..., description="Date")
    base_currency: str | None = Field(..., description="Currency code")
    target_currency: str | None = Field(..., description="Currency name")
    