from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .BaseModel import BaseModel


class PhotoModel(BaseModel):
    __tablename__ = "photos"
    profile_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    link: Mapped[str] = mapped_column(String(500), nullable=False)

    profile: Mapped["ProfileModel"] = relationship(
        "ProfileModel",
        back_populates="photos",
    )
