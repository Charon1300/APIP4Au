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
    damage: int | None
    guard: str = Field(min_length=1, max_length=10)
    startup: int | None
    active: int | None
    recovery: int | None
    onblock: int | None



class ButtonCreate(ButtonBase):
    character_id: int  # TEMPORARY


class ButtonResponse(ButtonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    character_id: int
    image_file: str | None
    image_path: str