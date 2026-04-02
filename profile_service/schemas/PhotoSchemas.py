from typing import Annotated

from pydantic import BaseModel, StrictInt, Field, ConfigDict


class PhotoBase(BaseModel):
    link: Annotated[str, Field(..., description="Link to the photo", max_length=500)]


class PhotoCreate(PhotoBase):
    profile_id: StrictInt


class PhotoUpdate(PhotoBase):
    pass

class PhotoResponse(PhotoBase):
    id: StrictInt
    profile_id: StrictInt

    model_config = ConfigDict(from_attributes=True)
