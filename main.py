from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field

app = FastAPI(
    title="Trading App"
)


@app.exception_handler(ResponseValidationError)
async def vaidation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )


fake_users = [
    {"id": 1, "role": "admin", "name": ["Jack"]},
    {"id": 2, "role": "user", "name": "John"},
    {"id": 3, "role": "trader", "name": "Jane", "degree": []},
    {"id": 4, "role": "investor", "name": "Luis", "degree": [
        {"id": 1, "created_at": "2021-09-09T00:00:00", "type_degree": "expert"}
    ]},
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]

fake_trades = [
    {"id": 1, "user_id": 1, "symbol": "BTCUSD", "side": "buy", "price": 10000, "amount": 0.1},
    {"id": 2, "user_id": 2, "symbol": "ETHUSD", "side": "sell", "price": 2000, "amount": 1},
    {"id": 3, "user_id": 3, "symbol": "BTCUSD", "side": "buy", "price": 10500, "amount": 0.2},
    {"id": 4, "user_id": 1, "symbol": "ETHUSD", "side": "buy", "price": 2100, "amount": 0.5},
    {"id": 5, "user_id": 2, "symbol": "BTCUSD", "side": "sell", "price": 10200, "amount": 0.1},
]

class Trade(BaseModel):
    id: int
    user_id: int
    symbol: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float



@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
