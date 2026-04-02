from typing import Annotated

from pydantic import BaseModel, Field, StrictInt, model_validator, ConfigDict

from profile_service.enums import SexAllowed, StatusAllowed



class ProfileBase(BaseModel):
    name: Annotated[str, Field(..., max_length=100, min_length=1, description="Profile name")]
    age: Annotated[int, Field(..., ge=10, le=100, description="Age of the profile")]
    city: Annotated[str, Field(..., max_length=100, min_length=1, description="City of the profile")]
    sex: Annotated[SexAllowed, Field(..., description="Gender of the profile")]
    description: Annotated[str | None, Field(None, min_length=1, description="Description of the profile")]
    status: Annotated[StatusAllowed, Field(..., description="Status of the profile")]


class ProfileCreate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: StrictInt

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    name: Annotated[str | None, Field(None, max_length=100, min_length=1, description="Profile name")] = None
    age: Annotated[int | None, Field(None, ge=10, le=100, description="Age of the profile")] = None
    city: Annotated[str | None, Field(None, max_length=100, min_length=1, description="City of the profile")] = None
    sex: Annotated[SexAllowed | None, Field(None, description="Gender of the profile")] = None
    description: Annotated[str | None, Field(None, min_length=1, description="Description of the profile")] = None
    status: Annotated[StatusAllowed | None, Field(None, description="Status of the profile")] = None


class ProfileFind(BaseModel):
    city: Annotated[str, Field(..., max_length=100, min_length=1, description="City of the profile")]
    sex: Annotated[SexAllowed, Field(..., description="Gender of the profile")]
    status: Annotated[StatusAllowed, Field(..., description="Status of the profile")]
    min_age: Annotated[int, Field(..., ge=10, le=100, description="Min age of the profile")]
    max_age: Annotated[int, Field(..., ge=10, le=100, description="Max age of the profile")]

    @model_validator(mode="after")
    def validate_age_range(self):
        if self.max_age < self.min_age:
            raise ValueError("max_age must be greater than or equal to min_age")
        return self
