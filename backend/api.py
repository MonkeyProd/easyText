import datetime
import json
from os import listdir
from shutil import make_archive
from typing import Annotated
import validators

import fastapi
from fastapi import FastAPI, UploadFile, Request, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from starlette.responses import JSONResponse
from sqlalchemy_db import backend as db

from api_schemas import LoginBody, ParseUrlBody
from sqlalchemy_db.schemas import HistoryEntry
from neuro.nn import parse

db.init_db()

app = FastAPI()

origins = ["http://localhost:3000", "http://easy-text.ru"]

GLOBAL_HEADERS = {"Content-Type": "application/json",
                  "Access-Control-Allow-Origin": "*"}
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
    print(f'auth: {success}, message: {msg}')
    if not success:
        print(msg)
        raise fastapi.HTTPException(status_code=401, detail="Authorization failure: " + msg)


@app.post("/register")
async def register_page(body: LoginBody):
    user = body.user
    password = body.password
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


@app.post("/login")
async def login(body: LoginBody):
    user = body.user
    password = body.password
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
                print("token success not expired", json_token)
                return JSONResponse(headers=GLOBAL_HEADERS, status_code=200, content=json_token)
            else:
                return JSONResponse(headers=GLOBAL_HEADERS, status_code=500,
                                    content="Internal error. failed to retrieve token from database")
    return JSONResponse(headers=GLOBAL_HEADERS, status_code=401, content="Invalid authentication credentials")


@app.post('/parse')
async def parse_url(body: ParseUrlBody, user: Annotated[str | None, Cookie()] = None,
                    token: Annotated[str | None, Cookie()] = None):
    check_auth(user, token)
    url = body.url
    language = body.language

    invalid_url = not validators.url(url)
    empty_url = len(url) == 0
    no_url = url is None
    if invalid_url or empty_url or no_url:
        return JSONResponse(headers=GLOBAL_HEADERS, status_code=500, content="Invalid URL")
    print('started parsing')
    try:
        result_name = f'{user}_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}'
        text, image_path, text_path = parse(url, language, result_name)
        success = True
    except Exception as e:
        text = str(e)
        image_path = text_path = ''
        success = False
    history_success = db.add_history_entry(url, language, text, success, user, image_path, text_path)
    if not success:
        return JSONResponse(headers=GLOBAL_HEADERS, status_code=500, content="Internal error. Failed to parse.")
    if not history_success:
        print('failed to add history entry')
    return JSONResponse(headers=GLOBAL_HEADERS, status_code=200, content=f"{text}")


@app.get('/download/{file_type}/{file_name}')
async def download_file(file_type: str, file_name: str, user: Annotated[str | None, Cookie()] = None,
                        token: Annotated[str | None, Cookie()] = None):
    check_auth(user, token)
    return FileResponse(path=f'{file_type}/{file_name}', filename=file_name, media_type='image/png')


@app.post('/history', response_model=list[HistoryEntry])
async def get_history(user: Annotated[str | None, Cookie()] = None,
                      token: Annotated[str | None, Cookie()] = None):
    check_auth(user, token)
    history = db.get_history(user)
    return JSONResponse(headers=GLOBAL_HEADERS, status_code=200, content=history)


@app.get('/test')
async def test():
    return JSONResponse(headers=GLOBAL_HEADERS, status_code=200, content="test")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000, host='0.0.0.0')
