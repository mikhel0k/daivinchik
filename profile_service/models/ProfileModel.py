from sqlalchemy import String, Integer, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel
from profile_service.enums import SexAllowed, StatusAllowed

class ProfileModel(BaseModel):
    __tablename__ = "profiles"
    __table_args__ = (
        Index("ix_profiles_city_sex_status", "city", "sex", "status"),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    sex: Mapped[SexAllowed] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[StatusAllowed] = mapped_column(String(20), nullable=False)

    photos: Mapped[list["PhotoModel"]] = relationship(
        "PhotoModel",
        back_populates="profile",
        cascade="all, delete-orphan",
    )
