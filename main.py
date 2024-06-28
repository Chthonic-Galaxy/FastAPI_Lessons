from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Trading App"
)


fake_users = [
    {"id": 1, "role": "Admin", "name": "Jack"},
    {"id": 2, "role": "User", "name": "John"},
    {"id": 3, "role": "User", "name": "Jane"},
]


@app.get("/users/{user_id}")
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
