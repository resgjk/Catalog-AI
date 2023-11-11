from fastapi import APIRouter, Body, Depends
from sqlalchemy import select, insert

from db.database import async_session_maker
from models.ai import AIModel
from models.category import CategoryModel

router = APIRouter(prefix="/api/v1", tags=["location"])


@router.get("")
async def get_categories():
    async with async_session_maker() as session:
        # query = (select(CategoryModel))
        query = (insert)
        result = await session.execute(query)
        # result = result.scalars().all()
        return result


# избранные ии юзера

# категории ии

# список нейронок категории

# нейронка

# регистрация и вход

# 