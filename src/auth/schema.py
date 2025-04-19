from pydantic import BaseModel
from fastapi import Form

class LoginDetails(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...)
    ):
        return cls(username=username, password=password)

class UserDetails(BaseModel):
    username: str

class NewUser(BaseModel):
    name: str
    username: str
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str = ''
    id_token: str = ''
    refresh_token :str = ''