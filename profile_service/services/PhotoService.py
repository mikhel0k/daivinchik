from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from profile_service.core import transactional_handler
from profile_service.schemas import PhotoCreate, PhotoResponse
from profile_service.models import PhotoModel
from profile_service.repositories import PhotoRepository


@transactional_handler
async def create_photo(
        photo_data: PhotoCreate,
        *,
        session: AsyncSession,
) -> PhotoResponse:
    photo = PhotoModel(**photo_data.model_dump())
    photo_res = await PhotoRepository.create_photo(photo, session)
    return PhotoResponse.model_validate(photo_res)


async def get_photo_by_id(
        photo_id: int,
        *,
        session: AsyncSession,
) -> PhotoResponse:
    photo_res = await PhotoRepository.get_photo_by_id(photo_id, session)
    if not photo_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return PhotoResponse.model_validate(photo_res)


async def get_photos_by_profile_id(
        profile_id: int,
        *,
        session: AsyncSession,
) -> list[PhotoResponse]:
    photo_res = await PhotoRepository.get_photos_by_profile_id(profile_id, session)
    return [PhotoResponse.model_validate(photo) for photo in photo_res]


@transactional_handler
async def delete_photo_by_id(
        photo_id: int,
        *,
        session: AsyncSession,
) -> None:
    photo_res = await PhotoRepository.get_photo_by_id(photo_id, session)
    if not photo_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    await PhotoRepository.delete_photo(photo_res, session)
