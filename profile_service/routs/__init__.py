from fastapi import APIRouter
from .PhotoRouts import router as photo_router
from .ProfileRouts import router as profile_router


router = APIRouter()
router.include_router(photo_router)
router.include_router(profile_router)
