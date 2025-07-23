from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
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

@router.post('/add')
async def add_film(db: Annotated[AsyncSession, Depends(get_db)], film_name: str = Form(...), film_author: str = Form(...)):
    await db.execute(insert(Film).values(title=film_name, author=film_author))
    await db.commit()
    return RedirectResponse('/', status_code=303)


