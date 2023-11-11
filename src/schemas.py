from pydantic import BaseModel


class UserRegister(BaseModel):
    login: str
    email: str
    password: str


class UserLogin(BaseModel):
    login: str
    password: str


class UserPhoto(BaseModel):
    user_id: int
    photo_bytes: str