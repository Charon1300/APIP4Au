from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException
#database
from database import Base, engine, get_db

from sqlalchemy import select
from sqlalchemy.orm import Session

import models

#schemas
from schemas import CharacterCreate, CharacterResponse, ButtonCreate, ButtonResponse

import random

Base.metadata.create_all(bind = engine)


app = FastAPI()


app.mount("/static", StaticFiles(directory = "static"), name = "static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory = "templates")

#frontend
@app.get("/", include_in_schema=False, name="home")
@app.get("/characters", include_in_schema=False, name="characters")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Character))
    characters = result.scalars().all()
    #can include vars to templates with {"posts": posts}
    return templates.TemplateResponse(request,"home.html", {"characters": characters, "title": "Home"})

@app.get("/characters/{character_id}", include_in_schema = False)
def post_page(request: Request, character_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Character).where(models.Character.id == character_id))
    character = result.scalars().first()
    if character:
        name = character.name[:50]
        
        return templates.TemplateResponse(request, "post.html", {"character": character, "name": name})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/ABAD", include_in_schema=False, name="random")
def random_button(request: Request, db: Annotated[Session, Depends(get_db)]):
    button_id = random.randrange(1, 4)
    prev_id = None
    
    f = open("previousNum", "r")
    prev_id = int(f.read())
    f.close()
    
    
    if button_id == prev_id:
        val = list(range(1, 4))
        val.remove(prev_id)
    
        button_id = random.choice(val)
    
    f = open("previousNum", "w")
    f.write(str(button_id))
    f.close()
        
    result = db.execute(select(models.Button).where(models.Button.id == button_id))
    button = result.scalars().first()
    if button:

        id = button.id
        name = button.name[:30]
        damage = button.damage
        guard = button.guard[:10]
        startup = button.startup
        active = button.active
        recovery = button.recovery
        onblock = button.onblock
        image_file = button.image_file[:200]
        character_id = button.character_id

        return templates.TemplateResponse(request, "buttonRand.html", {"button": button, "id": id, "name": name, "damage": damage ,"guard": guard, "startup": startup, "active": active, "recovery": recovery, "onblock": onblock, "image_file": image_file, "character_id": character_id})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


            
#api

#get all characters
@app.get("/api/characters", response_model=list[CharacterResponse])
def get_characters(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Character))
    characters = result.scalars().all()
    return characters



#get specific character
@app.get("/api/characters/{character_id}", response_model=CharacterResponse)
def get_character(character_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Character).where(models.Character.id == character_id))
    character = result.scalars().first()
    if character:
        return character
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

#create character
@app.post("/api/characters", response_model = CharacterResponse, status_code = status.HTTP_201_CREATED)
def create_charater(character: CharacterCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Character).where(models.Character.name == character.name))
    existing_character = result.scalars().first()
    if existing_character:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="chacter already exist",
        )
    new_character = models.Character(
        name = character.name,
        image_file = character.image_file
    )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character

#get all buttons
@app.get("/api/buttons", response_model=list[ButtonResponse])
def get_buttons(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Button))
    buttons = result.scalars().all()
    return buttons



#get specific button
@app.get("/api/buttons/{button_id}", response_model=ButtonResponse)
def get_button(button_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Button).where(models.Button.id == button_id))
    button = result.scalars().first()
    if button:
        return button
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="button not found")



@app.get("/api/button/random", response_model=ButtonResponse)
def get_random_button(db: Annotated[Session, Depends(get_db)]):
    button_id = random.randrange(1, 4)
    prev_id = None

    f = open("previousNum", "r")
    prev_id = int(f.read())
    f.close()


    if button_id == prev_id:
        val = list(range(1, 4))
        val.remove(prev_id)

        button_id = random.choice(val)

    f = open("previousNum", "w")
    f.write(str(button_id))
    f.close()
    
    result = db.execute(select(models.Button).where(models.Button.id == button_id))
    button = result.scalars().first()
    if button:
        return button
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="button not found")
    



#create button
@app.post("/api/buttons", response_model = ButtonResponse, status_code = status.HTTP_201_CREATED)
def create_button(button: ButtonCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Button).where(models.Button.image_file == button.image_file))
    existing_button = result.scalars().first()
    if existing_button: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="button already exist",
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
        character_id = button.character_id,
    )
    db.add(new_button)
    db.commit()
    db.refresh(new_button)
    return new_button


#error handling
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
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
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

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
