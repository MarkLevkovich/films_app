from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routers import film


app = FastAPI()
templates = Jinja2Templates(directory='static')

@app.get('/')
async def hello(request: Request):
    return templates.TemplateResponse(
        'hello.html',
        {
            'request': request
        }
    )


app.include_router(film.router)
