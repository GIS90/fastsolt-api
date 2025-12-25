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
from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.attributes import InstrumentedAttribute

from deploy.schema.dao.xtb_user import XtbUserModel


class XtbUserBo:

    async def _get_user_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbUserModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbUserModel, field):
                    return None
                _field = getattr(XtbUserModel, field)
            else:
                _field = field

            result = await db.execute(select(XtbUserModel).where(_field == value))
            return result.scalar_one_or_none()
        except Exception as exec:
            raise Exception(f"[{self.__class__.__name__}*查询One]{exec}")

    async def get_by_id(self, db: AsyncSession, user_id: int):
        return await self._get_user_by_field(db, XtbUserModel.id, user_id)

    async def get_by_rtx_id(self, db: AsyncSession, rtx_id: str):
        return await self._get_user_by_field(db, XtbUserModel.rtx_id, rtx_id)

    async def get_by_md5_id(self, db: AsyncSession, md5_id: str):
        return await self._get_user_by_field(db, XtbUserModel.md5_id, md5_id)

    async def get_by_name(self, db: AsyncSession, name: str):
        return await self._get_user_by_field(db, XtbUserModel.fullname, name)

    async def get_by_email(self, db: AsyncSession, email: str):
        return await self._get_user_by_field(db, XtbUserModel.email, email)

    async def get_by_phone(self, db: AsyncSession, phone: str):
        return await self._get_user_by_field(db, XtbUserModel.phone, phone)

    @classmethod
    async def get_all(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15
    ) -> Optional[List]:
        try:
            result = await db.execute(
                select(XtbUserModel).offset(offset).limit(limit)
            )
            return result.scalars().all()
        except Exception as exec:
            raise Exception(f"[{cls.__name__}*查询All]{exec}")

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

