from pydantic import BaseModel

class LoginBody(BaseModel):
    user: str
    password: str
    
class ParseUrlBody(BaseModel):
    language: str
    url: str