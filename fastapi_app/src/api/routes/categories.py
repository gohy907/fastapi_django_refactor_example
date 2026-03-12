
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from core.db import database
from repositories.categories import CategoryRepository
from repositories.users import UserRepository

router = APIRouter()


async def get_db():
    async with database.session() as session:
        yield session


@router.post(
    "/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(db)

    if await repo.does_category_exist(title=category_in.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this title already exists",
        )

    user_repo = UserRepository(db)
    if not await user_repo.does_user_exist_by_id(id=category_in.author_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this id does not exist"
        )

    category_date = category_in.model_dump()

    new_category = await repo.create(category_date)
    return new_category


@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category(category_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(db)
    user = await repo.get(category_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return user


# @router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
# async def update_user(
#     user_id: uuid.UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
# ):
#     repo = UserRepository(db)
#
#     db_user = await repo.get(user_id)
#     if db_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#
#     update_data = user_update.model_dump(exclude_unset=True)
#     updated_user = await repo.update(db_user, update_data)
#     return updated_user
#
#
# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
#     repo = UserRepository(db)
#
#     db_user = await repo.get(user_id)
#     if db_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#
#     await repo.delete(db_user)
#     return
