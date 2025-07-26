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
async def edit_page(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    films = await db.execute(select(Film))
    films_list = films.scalars().all()
    return templates.TemplateResponse(
        'edit.html',
        {
            'request': request,
            'films': films_list
        }
    )

@router.post('/add')
async def add_film(db: Annotated[AsyncSession, Depends(get_db)], film_name: str = Form(...), film_author: str = Form(...)):
    await db.execute(insert(Film).values(title=film_name, author=film_author))
    await db.commit()
    return RedirectResponse('/film/all', status_code=303)

@router.post('/del')
async def del_film(db: Annotated[AsyncSession, Depends(get_db)], film_id: int = Form(...)):
    await db.execute(delete(Film).where(Film.id==film_id))
    await db.commit()
    return RedirectResponse('/film/all', status_code=303)

@router.post('/manage')
async def manage_films(db: Annotated[AsyncSession, Depends(get_db)], film_id: int = Form(...), film_title: str = Form(...), film_author: str = Form(...)):
    await db.execute(update(Film).where(Film.id==film_id).values(title=film_title, author=film_author))
    await db.commit()
    return RedirectResponse('/film/all', status_code=303)


