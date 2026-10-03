from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    #portrait of character
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)

    buttons: Mapped[list[Button]] = relationship(back_populates="character")

    #doesn't need to include png, buttonRand.html will include it 
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Button(Base):
    __tablename__ = "buttons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    damage: Mapped[str | None] = mapped_column(String(30), nullable=True)

    #wheater button hits high, low, all, or is a throw
    guard: Mapped[str | None] = mapped_column(String(30), nullable=True)

    #the frames where a button isn't active yet
    startup: Mapped[int | None] = mapped_column(Integer, nullable = True)

    #the frames where the button is active and can deal damage or hit
    active: Mapped[str | None] = mapped_column(String(30), nullable = True)

    #the frames where the button is recovering 
    recovery: Mapped[str] = mapped_column(String(30), nullable = False)

    #the amt of frame advantage the other player has blocked the button
    onblock: Mapped[str | None] = mapped_column(String(30), nullable = True)

    #the archtype of button can be head, body, chest, foot, projectile, throw 
    attribute: Mapped[str | None] = mapped_column(String(30), nullable=True)

    #the frames where the button can't be hit by buttons which the mentioned attribute
    invuln: Mapped[str | None] = mapped_column(String(50), nullable=True)

    #image of button
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)

    #id of the character the button belongs to, list is main.py
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=False, index=True )

    character: Mapped[Character] = relationship(back_populates="buttons")

    #doesn't need to include png, buttonRand.html will include it 
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"