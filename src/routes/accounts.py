from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db, UserModel, UserGroupModel, UserGroupEnum, ActivationTokenModel, PasswordResetTokenModel, RefreshTokenModel
from security.token_manager import create_access_token, create_refresh_token
from schemas.accounts import RegisterUserSchema, ActivateUserSchema, LoginSchema

router = APIRouter()


@router.post("/register", response_model=RegisterUserSchema)
async def register_user(register_data: RegisterUserSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.email == register_data.email))
    user_exist = result.scalars().first()

    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    result = await db.execute(select(UserGroupModel).where(UserGroupModel.name == UserGroupEnum.USER))
    user_group = result.scalars().first()

    new_user = UserModel(email=register_data.email, group_id=user_group.id)
    db.add(new_user)
    await db.commit()
    return new_user


@router.post("/activate", response_model=ActivateUserSchema)
async def activate_user(activation_data: ActivateUserSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.email == activation_data.email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = True
    await db.commit()
    return {"message": "User activated successfully"}


@router.post("/login", response_model=LoginSchema)
async def login_user(login_data: LoginSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.email == login_data.email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}
