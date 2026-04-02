from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from profile_service.core import transactional_handler, StatusAllowed
from profile_service.schemas import ProfileResponse, ProfileCreate, ProfileUpdate, ProfileFind, PhotoResponse
from profile_service.models import ProfileModel
from profile_service.repositories import ProfileRepository, PhotoRepository


@transactional_handler
async def create_profile(
        profile_data: ProfileCreate,
        *,
        session: AsyncSession,
) -> ProfileResponse:
    profile = ProfileModel(**profile_data.model_dump())
    profile_res = await ProfileRepository.create_profile(profile, session)
    return ProfileResponse.model_validate(profile_res)


async def get_profile(
        profile_id: int,
        *,
        session: AsyncSession,
) -> tuple[ProfileResponse, list[PhotoResponse]]:
    profile_res = await ProfileRepository.get_profile_by_id(profile_id, session)
    if not profile_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    photos = await PhotoRepository.get_photos_by_profile_id(profile_id, session)
    return ProfileResponse.model_validate(profile_res), [PhotoResponse.model_validate(photo) for photo in photos]


@transactional_handler
async def update_profile(
        profile_id: int,
        profile_data: ProfileUpdate,
        *,
        session: AsyncSession,
) -> ProfileResponse:
    profile_in_db = await ProfileRepository.get_profile_by_id(profile_id, session)
    if not profile_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile_in_db, key, value)
    profile_res = await ProfileRepository.update_profile(profile_in_db, session)
    return ProfileResponse.model_validate(profile_res)


@transactional_handler
async def delete_profile(
        profile_id: int,
        *,
        session: AsyncSession,
) -> dict:
    profile_in_db = await ProfileRepository.get_profile_by_id(profile_id, session)
    if not profile_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    profile_in_db.status = StatusAllowed.inactive
    await ProfileRepository.update_profile(profile_in_db, session)
    return {"status": "inactive"}


async def get_profiles_by_filter(
        filter_data: ProfileFind,
        *,
        session: AsyncSession,
) -> list[ProfileResponse]:
    profiles = await ProfileRepository.get_profiles_filtered(
        **filter_data.model_dump(),
        status=StatusAllowed.active,
        session = session
    )
    return [ProfileResponse.model_validate(profile) for profile in profiles]
