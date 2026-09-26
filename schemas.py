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
    damage: int | None = Field(default=0)
    guard: str | None = Field(default="nothing", max_length=10)
    startup: int | None = Field(default=0)
    active: int | None  = Field(default=0)
    recovery: int 
    onblock: int | None  = Field(default=0)
    attribute: str | None = Field(default="nothing", max_length=30)
    invuln: str | None = Field(default="nothing", max_length=50)



class ButtonCreate(ButtonBase):
    character_id: int  # TEMPORARY


class ButtonResponse(ButtonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    character_id: int
    image_file: str | None
    image_path: str