import uuid
from datetime import datetime, timedelta
from typing import Tuple, List

from sqlalchemy.orm import Session

from . import models, schemas, security


# decorator that passes db session to function as first argument
def db_session(func):
    from .database import SessionLocal

    def wrapper(*args, **kwargs):
        # fixme this is horrible implementation of getting session
        db = SessionLocal()
        result = func(db, *args, **kwargs)
        db.close()
        return result

    return wrapper


@db_session
def init_db(db: Session):
    # from sqlalchemy import text
    from .database import engine
    # db.execute(text("DROP TABLE IF EXISTS classification CASCADE;"
    #                 "DROP TABLE IF EXISTS files CASCADE;"
    #                 "DROP TABLE IF EXISTS project_classes CASCADE;"
    #                 "DROP TABLE IF EXISTS projects CASCADE;"
    #                 "DROP TABLE IF EXISTS tokens CASCADE;"
    #                 "DROP TABLE IF EXISTS users CASCADE;"))
    # db.commit()
    models.Base.metadata.create_all(bind=engine)
    db.commit()


@db_session
def user_token_expired(db: Session, user: str):
    db_token = db.query(models.Tokens).filter(models.Tokens.owner == user).first()
    if db_token:
        # compare token expiration date with current date
        return db_token.expire < datetime.now()
    return True


@db_session
def user_valid_token(db: Session, user: str, token: str):
    db_token = db.query(models.Tokens).filter(models.Tokens.owner == user).first()
    if db_token:
        return db_token.token == token
    return False


@db_session
def is_user_exist(db: Session, user: str):
    db_user = db.query(models.Users).filter(models.Users.name == user).first()
    if db_user:
        return True
    return False


@db_session
def user_have_token(db: Session, user: str):
    db_token = db.query(models.Tokens).filter(models.Tokens.owner == user).first()
    if db_token:
        return True
    return False


@db_session
def check_auth(db: Session, user: str, token: uuid) -> Tuple[bool, str]:
    if user is None or len(user) == 0:
        return False, "User name is empty"
    if token is None:
        return False, "Token is empty"
    if not is_user_exist(user):
        return False, "User not found"
    if user_token_expired(user):
        return False, "Token expired, please login again"
    if not user_valid_token(user, uuid.UUID(token)):
        return False, "Invalid token, try login again or contact administrator"
    return True, "Auth OK"


@db_session
def is_password_correct(db: Session, user: str, password: str):
    db_user = db.query(models.Users).filter(models.Users.name == user).first()
    if db_user:
        return security.check_hash(password, db_user.password)
    return False


@db_session  # make first registered user admin
def register_new_user(db: Session, user: str, password: str) -> bool:
    db_user = models.Users(name=user, password=security.hash_data(password))
    db.add(db_user)
    try:
        db.commit()
    except Exception as e:
        print(type(e).__name__)
        return False
    db.refresh(db_user)
    return True


@db_session
def get_token(db: Session, user: str) -> Tuple[bool, dict]:
    db_token = db.query(models.Tokens).filter(models.Tokens.owner == user).first()
    if db_token:
        return True, {"token": str(db_token.token), "expire": str(db_token.expire)}
    return False, {}


@db_session
def generate_token(db: Session, user: str) -> Tuple[bool, dict]:
    token = uuid.uuid4()
    expire = datetime.now() + timedelta(days=1)
    # if user already have token, update it
    if user_have_token(user):
        db_token = db.query(models.Tokens).filter(models.Tokens.owner == user).first()
        db_token.token = token
        db_token.expire = expire
        db.commit()
        db.refresh(db_token)
    else:
        # else create new token
        db_token = models.Tokens(token=token, owner=user, expire=expire)
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
    return get_token(user)


@db_session
def add_history_entry(db: Session, url: str, language: str, result: str, success: bool, requester: str, image_path: str,
                      text_path: str):
    entry = models.History(url=url,
                           language=language,
                           result=result,
                           success=success,
                           requester=requester,
                           image_path=image_path,
                           text_path=text_path,
                           timestamp=datetime.now())
    db.add(entry)
    try:
        db.commit()
    except Exception as e:
        print(f'failed to add history entry, {entry}')
        print(type(e).__name__)
        return False
    db.refresh(entry)
    return True


@db_session
def get_history(db: Session, user: str):
    history = db.query(models.History).filter(models.History.requester == user).all()
    return [schemas.HistoryEntry(
        id_=entry.id_,
        url=entry.url,
        language=entry.language,
        result=entry.result,
        success=1 if entry.success else 0,
        requester=entry.requester,
        text_path=entry.text_path,
        image_path=entry.image_path,
        timestamp=str(entry.timestamp),
    ).dict() for entry in history]
