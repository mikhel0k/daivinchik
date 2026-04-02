from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from profile_service.core.db import get_db
from profile_service.services import PhotoService
from profile_service.schemas import PhotoResponse, PhotoUpdate, PhotoCreate


router = APIRouter(
    prefix="/photos",
    tags=["Photos"],
)


@router.post("/", response_model=PhotoResponse)
async def create_new_photo(
        photo: PhotoCreate,
        session: AsyncSession = Depends(get_db)
):
    return await PhotoService.create_photo(photo, session=session)


@router.get("/", response_model=list[PhotoResponse])
async def get_photos_by_profile_id(
        profile_id: int,
        session: AsyncSession = Depends(get_db)
):
    return await PhotoService.get_photos_by_profile_id(profile_id, session=session)


@router.delete("/{photo_id}")
async def delete_photo(
        photo_id: int,
        session: AsyncSession = Depends(get_db)
):
    return await PhotoService.delete_photo_by_id(photo_id, session=session)
