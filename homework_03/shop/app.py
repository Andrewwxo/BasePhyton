from typing import Optional

from fastapi import FastAPI, Body, Depends, Query
from schemas import UserIn, UserOut, User, CalcInput
import crud
from dependencies import get_user_by_token

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hi"}


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/items/")
def create_item(data: dict = Body(...)):
    return {
        "item": data,
    }


@app.get("/add/")
def add_two_numbers(a: int, b: int):
    return {"sum": a + b}


@app.get("/sub/")
def sub_two_numbers(
    # query string dependency
    q: Optional[str] = Query(None),
    # query string dependency too!
    calc_input: CalcInput = Depends(),
):
    return {
        "q": q,
        "sub": calc_input.a - calc_input.b,
    }


@app.get("/users/me/", response_model=UserOut)
def get_me(user: User = Depends(get_user_by_token)):
    return user


@app.post("/users/", response_model=UserOut)
def create_user(user_in: UserIn):
    user = crud.create_user(user_in)
    return user


@app.get("/users/", response_model=list[UserOut])
def get_users():
    users = crud.list_users()
    return users



