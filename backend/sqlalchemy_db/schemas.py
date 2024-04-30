from pydantic import BaseModel


# database schemas

class User(BaseModel):
    id: int
    name: str
    password: str


class Token(BaseModel):
    token: str
    owner: str
    expire: str
