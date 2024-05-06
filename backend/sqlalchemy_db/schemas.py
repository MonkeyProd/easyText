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


class HistoryEntry(BaseModel):
    id_: int
    url: str
    language: str
    result: str
    success: int
    requester: str
    timestamp: str

    class Config:
        orm_mode = True
