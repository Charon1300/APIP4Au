from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from typing import Annotated, Any 

def truncate_str(val: Any) -> Any:
    return val[:30] if isinstance(val, str) else val

type TruncatedStr = Annotated[str, BeforeValidator(truncate_str)]

class CharaterBase(BaseModel):
    name: str = Field(min_length = 1, max_length = 50)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)
    
    
class CharacterCreate(CharaterBase):
    pass

class CharacterResponse(CharaterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    
    image_file: str | None 
    image_path: str


class ButtonBase(BaseModel):
    name: TruncatedStr = Field(min_length=1, max_length=30)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)
    damage: TruncatedStr = Field(default="0", min_length=1, max_length=30)

    #wheater button hits high, low, all, or is a throw
    guard: TruncatedStr | None = Field(default="nothing", max_length=30)

    #the frames where a button isn't active yet
    startup: TruncatedStr | None = Field(default="0", max_length=30)

    #the frames where the button is active and can deal damage or hit
    active: TruncatedStr = Field(default="0", min_length=1, max_length=30)

    #the frames where the button is recovering 
    recovery: TruncatedStr = Field(default="0", min_length=1, max_length=30)

    #the amt of frame advantage the other player has blocked the button
    onblock: TruncatedStr | None = Field(default="0", max_length=30)

    #the archtype of button can be head, body, chest, foot, projectile, throw 
    attribute: TruncatedStr | None = Field(default="nothing", max_length=30)

    #the frames where the button can't be hit by buttons which the mentioned attribute
    invuln: str | None = Field(default="nothing", max_length=50)



class ButtonCreate(ButtonBase):
    #id of the character the button belongs to, list is main.py
    character_id: int  

class ButtonUpdate(BaseModel):
    name: TruncatedStr = Field(min_length=1, max_length=30)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)
    damage: TruncatedStr = Field(default="0", min_length=1, max_length=30)
    guard: TruncatedStr | None = Field(default="nothing", max_length=30)
    startup: int | None = Field(default=0)
    active: TruncatedStr = Field(default="0", min_length=1, max_length=30)
    recovery: TruncatedStr = Field(default="0", min_length=1, max_length=30)
    onblock: TruncatedStr | None = Field(default="0", max_length=30)
    attribute: TruncatedStr | None = Field(default="nothing", max_length=30)
    invuln: str | None = Field(default="nothing", max_length=50)
    character_id: int


class ButtonResponse(ButtonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    character_id: int
    image_file: str | None
    image_path: str