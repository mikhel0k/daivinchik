from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


def transactional_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: AsyncSession = kwargs.get("session")

        if session is None:
            raise RuntimeError("AsyncSession not found in kwargs")

        try:
            result = await func(*args, **kwargs)
            await session.commit()
            return result
        except HTTPException:
            await session.rollback()
            raise
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
    return wrapper