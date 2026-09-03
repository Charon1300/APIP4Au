from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)

    buttons: Mapped[list[Button]] = relationship(back_populates="character")

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Button(Base):
    __tablename__ = "Buttons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    damage: Mapped[int] = mapped_column(Integer, nullable=True)
    guard: Mapped[str] = mapped_column(String(10), nullable=True)
    startup: Mapped[int] = mapped_column(Integer, nullable = True)
    active: Mapped[int] = mapped_column(Integer, nullable = True)
    recovery: Mapped[int] = mapped_column(Integer, nullable = False)
    onblock: Mapped[int] = mapped_column(Integer, nullable = True)
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)

    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=False, index=True )

    character: Mapped[Character] = relationship(back_populates="buttons")

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"