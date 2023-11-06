from pydantic import BaseModel

class Register(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

class Login(BaseModel):
    email:str
    password:str
    
class User(BaseModel):
    username: str
    email: str
    full_name: str
    created_at: str