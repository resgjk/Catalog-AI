import re

import bcrypt
from fastapi import APIRouter, Body
from sqlalchemy import delete, select, insert, update, and_
from sqlalchemy.exc import NoResultFound

from db.database import async_session_maker
from models.ai import AIModel
from models.category import CategoryModel
from models.user import UserModel
from models.user_ai import UserAIModel
from schemas import *
from ai import query_ai

router = APIRouter(prefix="/api/v1")


@router.get("/categories")
async def get_categories():
    async with async_session_maker() as session:
        query = select(CategoryModel)
        categories = await session.execute(query)
        return categories.scalars().all()


@router.post("/ai/favorite")
async def post_to_favorite(user_ai: UserAi = Body()):
    async with async_session_maker() as session:
        stmt = insert(UserAIModel).values(**dict(user_ai))
        await session.execute(stmt)
        await session.commit()
        return {"response": "successfull"}


@router.delete("/ai/favorite")
async def datele_from_favorite(user_ai: UserAi = Body()):
    async with async_session_maker() as session:
        stmt = delete(UserAIModel).where(
            and_(
                UserAIModel.user_id == user_ai.user_id,
                UserAIModel.ai_id == user_ai.ai_id,
            )
        )
        await session.execute(stmt)
        await session.commit()
        return {"response": "successfull"}


@router.get("/ai/favorite/{user_id}")
async def get_favorite_ais(user_id: int):
    async with async_session_maker() as session:
        query = (
            select(AIModel)
            .where(AIModel.id == UserAIModel.ai_id)
            .where(UserAIModel.user_id == user_id)
        )
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/ai/{category}")
async def get_ai_by_categories(category: int):
    async with async_session_maker() as session:
        query = select(AIModel).where(AIModel.category_id == category)
        result = await session.execute(query)
        return result.scalars().all()


@router.post("/ai/query")
async def post_query(query: AiQuery = Body()):
    result = await query_ai(**dict(query))
    return {"response": result}


@router.post("/user/register")
async def register(user: UserRegister = Body()):
    async with async_session_maker() as session:
        query = select(UserModel).where(UserModel.login == user.login)

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
        stmt = insert(UserModel).values(**dict(user))
        res = await session.execute(stmt)
        await session.commit()
        return {"response": "successfull"}


@router.post("/user/login")
async def login(user: UserLogin = Body()):
    async with async_session_maker() as session:
        query = select(UserModel).where(UserModel.login == user.login)
        result = await session.execute(query)

        try:
            result = result.scalars().one()
            if result and bcrypt.checkpw(
                user.password.encode("utf-8"), result.password
            ):
                return result
            return {"response": "Incorrect Password"}
        except NoResultFound:
            return {"response": "User Not Found"}


@router.put("/user/photo")
async def post_user_photo(photo: UserPhoto = Body()):
    async with async_session_maker() as session:
        stmt = (
            update(UserModel)
            .where(UserModel.id == photo.user_id)
            .values(user_image=photo.photo_bytes.encode("utf-8"))
        )
        await session.execute(stmt)
        await session.commit()
        return {"response": "successfull"}
