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

Base.metadata.create_all(bind = engine)


app = FastAPI()


app.mount("/static", StaticFiles(directory = "static"), name = "static")

templates = Jinja2Templates(directory = "templates")


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Charaters))
    posts = result.scalar().all()
    #can include vars to templates with {"posts": posts}
    return templates.TemplateResponse(request,"home.html", {"posts": posts, "title": "Home"})

@app.get("/posts/{character_id}", include_in_schema = False)
def post_page(request: Request, character_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Charaters).where(models.Charaters.id == character_id))
    post = result.scalar().first()
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(request, "post.html", {"post": post, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            

@app.get("/api/posts", response_model=list[CharacterResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Charaters))
    posts = result.scalars().all()
    return posts



@app.get("/api/posts/{post_id}", response_model=CharacterResponse)
def get_post(character_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Charaters).where(models.Charaters.id == character_id))
    post = result.scalars().first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.post("/api/posts", response_model = CharacterResponse, status_code = status.HTTP_201_CREATED)
def create_charater(character: CharacterCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Charaters).where(models.Charaters.name == character.name))
    existing_character = result.scalars().first()
    if existing_character:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="chacter already exist",
        )
    new_character = models.Charaters(
        name=character.name
    )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character


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