from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from db.db import get_db
from sqlalchemy import select, update, delete, insert
from models.film import Film
from schemas import CreateFilm
from slugify import slugify

router = APIRouter(prefix='/film', tags=['film'])
templates = Jinja2Templates(directory='static')

@router.get('/all')
async def get_all(db: Annotated[AsyncSession, Depends(get_db)], request: Request):
    films = await db.execute(select(Film))
    films_list = films.scalars().all()
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'films': films_list,
        }
    )


@router.get('/edit')
async def edit_page(request: Request):
    return templates.TemplateResponse(
        'edit.html',
        {
            'request': request
        }
    )

@router.post('/create')
async def create_category(db: Annotated[AsyncSession, Depends(get_db)], create_film: CreateFilm):
    await db.execute(insert(Film).values(title=create_film.title,
                                       author=create_film.author))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


