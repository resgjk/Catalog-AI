import re

import bcrypt
from fastapi import APIRouter, Body, Depends
from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel

from db.database import async_session_maker
from models.ai import AIModel
from models.category import CategoryModel
from models.user import UserModel
from models.user_ai import UserAIModel
from schemas import UserLogin, UserRegister, UserPhoto

router = APIRouter(prefix="/api/v1")


@router.get("/categories")
async def get_categories():
    async with async_session_maker() as session:
        query = (select(CategoryModel))
        categories = await session.execute(query)
        return categories.scalars().all()


@router.get("/ai/favorite/{user_id}")
async def get_favorite_ais(user_id: int):
    async with async_session_maker() as session:
        query = (select(AIModel)
                 .where(AIModel.id == UserAIModel.ai_id)
                 .where(UserAIModel.user_id == user_id))
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/ai/{category}")
async def get_ai_by_categories(category: int):
    async with async_session_maker() as session:
        query = (select(AIModel)
                 .where(AIModel.category_id == category))
        result = await session.execute(query)
        return result.scalars().all()


@router.post("/user/register")
async def register(user: UserRegister = Body()):
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


@router.put("/user/photo")
async def post_user_photo(photo: UserPhoto = Body()):
    async with async_session_maker() as session:
        stmt = (update(UserModel)
                .where(UserModel.id == photo.user_id)
                .values(user_image=photo.photo_bytes.encode("utf-8")))
        await session.execute(stmt)
        await session.commit()
        return {"response": "successfull"}
