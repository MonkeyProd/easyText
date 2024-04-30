import json
from os import listdir
from shutil import make_archive

import fastapi
from fastapi import FastAPI, UploadFile, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from starlette.responses import JSONResponse
from sqlalchemy_db import backend as db

db.init_db()

app = FastAPI()

GLOBAL_HEADERS = {"Content-Type": "application/json",
                  "Access-Control-Allow-Origin": "*"}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_auth(user: str = '', token: str = ''):
    print(f'Checking auth for user[{user}] with token[{token}]')
    success, msg = db.check_auth(user, token)
    if not success:
        print(msg)
        raise fastapi.HTTPException(status_code=401, detail="Authorization failure: " + msg)


@app.post("/register")
async def register_page(user: str = '', password: str = ''):
    if not user or not password:
        return JSONResponse(headers=GLOBAL_HEADERS, status_code=400, content="Missing user or password")
    if db.is_user_exist(user):
        return JSONResponse(headers=GLOBAL_HEADERS, status_code=400, content="User already exists!")
    success = db.register_new_user(user, password)
    if not success:
        return JSONResponse(headers=GLOBAL_HEADERS, status_code=500,
                            content="Internal server error. falied to register new user :(")
    return JSONResponse(headers=GLOBAL_HEADERS, status_code=200,
                        content="Successful registration! Redirection to login page in 5 seconds...")


@app.get("/login")
async def login(user: str = '', password: str = ''):
    if not db.is_user_exist(user):
        return JSONResponse(headers=GLOBAL_HEADERS, status_code=401, content="Invalid authentication credentials")
    if db.is_password_correct(user, password):
        user_have_token = db.user_have_token(user)
        user_token_expired = db.user_token_expired(user)
        need_to_generate_token = (not user_have_token) or user_token_expired
        if need_to_generate_token:
            # generate new token
            # save new token (or replace old expired one)
            # return new token
            success, json_token = db.generate_token(user)
            if success:
                print("token success expired", json_token)
                return JSONResponse(headers=GLOBAL_HEADERS, status_code=200, content=json_token)
            else:
                return JSONResponse(headers=GLOBAL_HEADERS, status_code=500,
                                    content="Internal error. failed to generate token")
        else:
            success, json_token = db.get_token(user)
            # return existing token
            if success:
                json_token['role'] = db.get_user_role(user)
                print("token success not expired", json_token)
                return JSONResponse(headers=GLOBAL_HEADERS, status_code=200, content=json_token)
            else:
                return JSONResponse(headers=GLOBAL_HEADERS, status_code=500,
                                    content="Internal error. failed to retrieve token from database")
    return JSONResponse(headers=GLOBAL_HEADERS, status_code=401, content="Invalid authentication credentials")


@app.get('/test')
async def test():
    return JSONResponse(headers=GLOBAL_HEADERS, status_code=200, content="test")


# настройкst_pathи
# папка DATA чтобы можно было обозначить
# добавить флаг обозначающий может ли пользователь менять дефолтное расположение проекта
# чтобы админ мог перемещать проекты

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000, host='127.0.0.1')
