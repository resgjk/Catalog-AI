import re

import bcrypt
from fastapi import APIRouter, Body, Depends
from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel

from db.database import async_session_maker
from models.ai import AIModel
from models.category import CategoryModel
from models.user import UserModel
from models.user_ai import UserAIModel

router = APIRouter(prefix="/api/v1", tags=["location"])


# категории ии
@router.get("/category")
async def get_categories():
    async with async_session_maker() as session:
        query = (select(CategoryModel))
        result = await session.execute(query)
        result = result.scalars().all()
        return result


# избранные ии юзера
@router.get("/ai/favorite/{user_id}")
async def get_fovorite_ais(user_id: int):
    async with async_session_maker() as session:
        query = (select(AIModel)
                 .where(AIModel.id == UserAIModel.ai_id)
                 .where(UserAIModel.user_id == user_id))
        result = await session.execute(query)
        result = result.scalars().all()
        return result



# список нейронок категории
@router.get("/ai/{category}")
async def get_ais(category: int):
    async with async_session_maker() as session:
        query = (select(AIModel).where(AIModel.category_id == category))
        result = await session.execute(query)
        result = result.scalars().all()
        return result

# нейронка

class UserRegister(BaseModel):
    login: str
    email: str
    password: str


class UserLogin(BaseModel):
    login: str
    password: str


@router.post("/user/regiter")
async def regiter(user: UserRegister = Body()):
    async with async_session_maker() as session:
        query = (select(UserModel).where(UserModel.login == user.login))
        try:
            res = await session.execute(query)
            res = res.scalars().one()
            if res:
                return {"response": "User Already Exist"}
        except Exception:
            ...
        pattern_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern_email, user.email):
            return {"response": "Incorrect Email"}
        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
        stmt = (insert(UserModel)
                .values(**dict(user)).returning(UserModel))
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()


@router.post("/user/login")
async def login(user: UserLogin = Body()):
    async with async_session_maker() as session:
        query = (select(UserModel).where(UserModel.login == user.login))
        result = await session.execute(query)
        try:
            result = result.scalars().one()
            if result and bcrypt.checkpw(user.password.encode("utf-8"), result.password):
                return result
            return {"response": "Incorrect Password"}
        except NoResultFound:
            return {"response": "User Not Found"}
