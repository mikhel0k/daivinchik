from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from profile_service.core.db import get_db
from profile_service.schemas import ProfileResponse, ProfileCreate, ProfileUpdate, ProfileFind
from profile_service.services import ProfileService

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", response_model=ProfileResponse)
async def create_profile(
        profile: ProfileCreate,
        session: AsyncSession = Depends(get_db)
):
    return await ProfileService.create_profile(profile, session=session)


@router.get("/{profile_id}", response_model=dict)
async def read_profile(
        profile_id:int,
        session: AsyncSession = Depends(get_db)
):
    profile, photos = await ProfileService.get_profile(profile_id, session=session)
    return {
        "profile": profile,
        "photos": photos
    }


@router.patch("/{profile_id}", response_model=ProfileResponse)
async def update_profile(
        profile_id: int,
        profile: ProfileUpdate,
        session: AsyncSession = Depends(get_db),
):
    return await ProfileService.update_profile(profile_id, profile, session=session)


@router.delete("/{profile_id}")
async def delete_profile(
        profile_id: int,
        session: AsyncSession = Depends(get_db)
):
    return await ProfileService.delete_profile(profile_id, session=session)


@router.get("/", response_model=list[ProfileResponse])
async def read_profiles_by_filter(
        city: str,
        sex: str,
        min_age: int,
        max_age: int,
        session: AsyncSession = Depends(get_db)
):
    return await ProfileService.get_profiles_by_filter(
    ProfileFind(
        city=city,
        sex=sex,
        min_age=min_age,
        max_age=max_age,
    ), session=session)
