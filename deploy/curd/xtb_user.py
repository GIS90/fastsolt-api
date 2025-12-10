# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    xtb_user

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 22:39
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = xtb_user.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from deploy.schema.dao.xtb_user import XtbUserModel


class XtbUserBo:
    async def get_by_id(self, db: AsyncSession, user_id: int) -> Optional[XtbUserModel]:
        result = await db.execute(select(XtbUserModel).where(XtbUserModel.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_rtx_id(self, db: AsyncSession, rtx_id: str) -> Optional[XtbUserModel]:
        result = await db.execute(select(XtbUserModel).where(XtbUserModel.rtx_id == rtx_id))
        return result.scalar_one_or_none()

    async def get_by_md5_id(self, db: AsyncSession, md5_id: str) -> Optional[XtbUserModel]:
        result = await db.execute(select(XtbUserModel).where(XtbUserModel.md5_id == md5_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[XtbUserModel]:
        result = await db.execute(select(XtbUserModel).where(XtbUserModel.fullname == name))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[XtbUserModel]:
        result = await db.execute(select(XtbUserModel).where(XtbUserModel.email == email))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, offset: int = 0, limit: int = 100) -> List:
        result = await db.execute(select(XtbUserModel).offset(offset).limit(limit))
        return result.scalars().all()

    #
    # @staticmethod
    # async def create(db: AsyncSession, user_in: UserCreate) -> User:
    #     # 在实际项目中，这里应该对密码进行哈希处理
    #     db_user = User(
    #         email=user_in.email,
    #         username=user_in.username,
    #         full_name=user_in.full_name,
    #         hashed_password=user_in.password + "_hashed"  # 简化处理，实际应使用密码哈希
    #     )
    #     db.add(db_user)
    #     await db.commit()
    #     await db.refresh(db_user)
    #     return db_user
    #
    # @staticmethod
    # async def update(db: AsyncSession, user_id: int, user_in: UserUpdate) -> Optional[User]:
    #     """
    #     :param db:
    #     :param user_id:
    #     :param user_in:
    #     :return:
    #
    #     # 方法2: 直接更新
    #     # stmt = update(User).where(User.id == user_id).values(**update_data)
    #     # await self.session.execute(stmt)
    #     # await self.session.commit()
    #     # return await self.get_user_by_id(user_id)
    #     """
    #     user = await CRUDUser.get_by_id(db, user_id)
    #     if user:
    #         update_data = user_in.model_dump(exclude_unset=True)
    #         if "password" in update_data:
    #             update_data["hashed_password"] = update_data.pop("password") + "_hashed"
    #
    #         for field, value in update_data.items():
    #             setattr(user, field, value)
    #
    #         await db.commit()
    #         await db.refresh(user)
    #     return user
    #
    # @staticmethod
    # async def delete(db: AsyncSession, user_id: int) -> bool:
    #     user = await CRUDUser.get_by_id(db, user_id)
    #     if user:
    #         await db.delete(user)
    #         await db.commit()
    #         return True
    #     return False
    #

