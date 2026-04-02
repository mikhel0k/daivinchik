from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from profile_service.models import PhotoModel


async def create_photo(
        photo: PhotoModel,
        session: AsyncSession,
) -> PhotoModel:
    session.add(photo)
    await session.flush()
    await session.refresh(photo)
    return photo


async def get_photo_by_id(
        photo_id: int,
        session: AsyncSession,
) -> PhotoModel | None:
    return await session.get(PhotoModel, photo_id)


async def get_photos_by_profile_id(
        profile_id: int,
        session: AsyncSession,
) -> Sequence[PhotoModel]:
    stmt = select(PhotoModel).where(PhotoModel.profile_id == profile_id)
    res = await session.execute(stmt)
    return res.scalars().all()


async def delete_photo(
        photo: PhotoModel,
        session: AsyncSession,
) -> None:
    await session.delete(photo)
    await session.flush()
    return None
