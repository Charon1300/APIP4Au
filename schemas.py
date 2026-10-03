from pydantic import BaseModel, ConfigDict, Field

class CharaterBase(BaseModel):
    name: str = Field(min_length = 1, max_length = 10)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)
    
    
class CharacterCreate(CharaterBase):
    pass

class CharacterResponse(CharaterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    
    image_file: str | None 
    image_path: str


class ButtonBase(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)
    damage: str = Field(default="0", min_length=1, max_length=30)

    #wheater button hits high, low, all, or is a throw
    guard: str | None = Field(default="nothing", max_length=30)

    #the frames where a button isn't active yet
    startup: int | None = Field(default=0)

    #the frames where the button is active and can deal damage or hit
    active: str = Field(default="0", min_length=1, max_length=30)

    #the frames where the button is recovering 
    recovery: str = Field(default="0", min_length=1, max_length=30)

    #the amt of frame advantage the other player has blocked the button
    onblock: str | None = Field(default="0", max_length=30)

    #the archtype of button can be head, body, chest, foot, projectile, throw 
    attribute: str | None = Field(default="nothing", max_length=30)

    #the frames where the button can't be hit by buttons which the mentioned attribute
    invuln: str | None = Field(default="nothing", max_length=50)



class ButtonCreate(ButtonBase):
    #id of the character the button belongs to, list is main.py
    character_id: int  

class ButtonUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)
    damage: str = Field(default="0", min_length=1, max_length=30)
    guard: str | None = Field(default="nothing", max_length=30)
    startup: int | None = Field(default=0)
    active: str = Field(default="0", min_length=1, max_length=30)
    recovery: str = Field(default="0", min_length=1, max_length=30)
    onblock: str | None = Field(default="0", max_length=30)
    attribute: str | None = Field(default="nothing", max_length=30)
    invuln: str | None = Field(default="nothing", max_length=50)
    character_id: int


class ButtonResponse(ButtonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    character_id: int
    image_file: str | None
    image_path: str