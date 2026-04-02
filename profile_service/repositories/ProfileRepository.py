from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from profile_service.models import ProfileModel


async def get_profile_by_id(
        profile_id: int,
        session: AsyncSession,
) -> ProfileModel | None:
    return await session.get(ProfileModel, profile_id)


async def get_profiles_filtered(
        city: str,
        sex: str,
        status: str,
        min_age: int,
        max_age: int,
        session: AsyncSession,
) -> Sequence[ProfileModel]:
    stmt = (
        select(ProfileModel)
        .where(ProfileModel.city == city)
        .where(ProfileModel.sex == sex)
        .where(ProfileModel.status == status)
        .where(ProfileModel.age >= min_age)
        .where(ProfileModel.age <= max_age)
    )
    res = await session.execute(stmt)
    return res.scalars().all()


async def create_profile(
        profile: ProfileModel,
        session: AsyncSession,
) -> ProfileModel:
    session.add(profile)
    await session.flush()
    await session.refresh(profile)
    return profile


async def update_profile(
        profile: ProfileModel,
        session: AsyncSession,
) -> ProfileModel:
    await session.flush()
    await session.refresh(profile)
    return profile
