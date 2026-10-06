from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler

from starlette.exceptions import HTTPException as StarletteHTTPException
#database
from database import engine, get_db

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from contextlib import asynccontextmanager

import models

#schemas
from schemas import CharacterCreate, CharacterResponse, ButtonCreate, ButtonResponse, ButtonUpdate

import random

#get random button
@asynccontextmanager
async def lifespan(app: FastAPI):
    #gets rand number from range, doesn't include stop
    button_id = random.randrange(1, 3)
    prev_id = None

    #reads from prevNum to get yesterdays num
    f = open("previousNum", "r")
    prev_id = int(f.read())
    f.close() 

    #if it is the same then get random from range not including prev_id
    if button_id == prev_id:
        val = list(range(1, 3))
        val.remove(prev_id)

        button_id = random.choice(val)

    
    #records currNum
    f = open("currentNum", "w")
    f.write(str(button_id))
    f.close()
    yield
    #on shut down records pervNum 
    f = open("previousNum", "w")
    f.write(str(button_id))
    f.close()
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

#static and media folders
app.mount("/static", StaticFiles(directory = "static"), name = "static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory = "templates")

#missing naoto 2[c], teddie 5bb,5bbb, yukiko 4b
#Character order for charcter id to buttons 
#shows what buttons belong to which character
characterList = {
    1: "Margaret",
    2: "Sho",
    3: "Naoto",
    4: "Teddie",
    5: "Yukiiko",
    6: "Yu",
    7: "Yosuke",
    8: "Chie",
    9: "Kanji",
    10: "Minazuki",
    11: "Marie",
    12: "Ken and Koromaru",
    13: "Yukari",
    14: "Labrys",
    15: "Mitsuru",
    16: "Aigis",
    17: "Adachi",
    18: "Elizabeth",
    19: "Akihiko",
    20: "Shadow Labrys",
    21: "Junpei",
    22: "Rise"
    }



#frontend
#testing 
"""
@app.get("/", include_in_schema=False, name="home")
@app.get("/characters", include_in_schema=False, name="characters")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Character).options(selectinload(models.Character.buttons)))
    characters = result.scalars().all()
    #can include vars to templates with {"posts": posts}
    return templates.TemplateResponse(request,"home.html", {"characters": characters, "title": "Home"})

@app.get("/characters/{character_id}", include_in_schema = False)
async def post_page(request: Request, character_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Character).where(models.Character.id == character_id))
    character = result.scalars().first()
    if character:
        name = character.name[:50]
        
        return templates.TemplateResponse(request, "post.html", {"character": character, "name": name})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
"""
#get random button
@app.get("/P4UBD", include_in_schema=False, name="random")
async def random_button(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    
    #currNum has the number for the button id 
    f = open("currentNum", "r")
    id = int(f.read())
    f.close()

    #use said id to get button info
    result = await db.execute(select(models.Button).where(models.Button.id == id))
    button = result.scalars().first()
    if button:

        id = button.id
        name = button.name[:30]
        damage = button.damage[:30]
        guard = button.guard[:30]
        startup = button.startup
        active = button.active[:30]
        recovery = button.recovery[:30]
        onblock = button.onblock[:30]
        attribute = button.attribute[:30]
        invuln = button.invuln[:50]
        image_file = button.image_file[:200]
        character_id = button.character_id

        #give info to buttonRand html page for template 
        return templates.TemplateResponse(request, "buttonRand.html", {"button": button, "id": id, "name": name, "damage": damage ,"guard": guard, "startup": startup, "active": active, "recovery": recovery, "onblock": onblock, "attribute": attribute, "invuln": invuln, "image_file": image_file, "character_id": character_id, "characterList": characterList})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Button not found")


            
#api

#get all characters
@app.get("/api/characters", response_model=list[CharacterResponse])
async def get_characters(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Character))
    characters = result.scalars().all()
    return characters



#get specific character
@app.get("/api/characters/{character_id}", response_model=CharacterResponse)
async def get_character(character_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Character).where(models.Character.id == character_id))
    character = result.scalars().first()
    if character:
        return character
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

#create character
@app.post("/api/characters", response_model = CharacterResponse, status_code = status.HTTP_201_CREATED)
async def create_charater(character: CharacterCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Character).where(models.Character.name == character.name))
    existing_character = result.scalars().first()
    if existing_character:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Character already exist",
        )
    new_character = models.Character(
        name = character.name,
        image_file = character.image_file
    )
    db.add(new_character)
    await db.commit()
    await db.refresh(new_character)
    return new_character



#get all buttons
@app.get("/api/buttons", response_model=list[ButtonResponse])
async def get_buttons(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Button))
    buttons = result.scalars().all()
    return buttons



#get specific button
@app.get("/api/buttons/{button_id}", response_model=ButtonResponse)
async def get_button(button_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Button).where(models.Button.id == button_id))
    button = result.scalars().first()
    if button:
        return button
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Button not found")

#edit button
@app.patch("/api/buttons/{button_id}", response_model=ButtonResponse)
async def edit_button(button_id: int, button_data: ButtonUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Button).where(models.Button.id == button_id))
    button = result.scalars().first()
    if not button:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Button not found")

    updata_data = button_data.model_dump(exclude_unset=True)
    for field, value in updata_data.items():
        setattr(button, field, value)
    
    await db.commit()
    await db.refresh(button)
    return button

#create button
@app.post("/api/buttons", response_model = ButtonResponse, status_code = status.HTTP_201_CREATED)
async def create_button(button: ButtonCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Button).where(models.Button.image_file == button.image_file))
    existing_button = result.scalars().first()
    if existing_button: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Button already exist",
        )
    new_button = models.Button(
        name = button.name,
        image_file = button.image_file,
        damage = button.damage,
        guard = button.guard,
        startup = button.startup,
        active = button.active,
        recovery = button.recovery,
        onblock = button.onblock,
        attribute = button.attribute,
        invuln = button.invuln,

        character_id = button.character_id,
    )
    db.add(new_button)
    await db.commit()
    await db.refresh(new_button)
    return new_button


#error handling
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    

    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)


    message = (
            exception.detail
            if exception.detail
            else "An error occurred. Please check your request and try again."
        )
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception)

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )

if __name__ == "__main__":
    print("Hello")
