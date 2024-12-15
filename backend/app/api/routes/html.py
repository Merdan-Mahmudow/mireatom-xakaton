from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="/app/app/templates")




@router.get('/formula')
async def formula_html_content(requset: Request):
    return templates.TemplateResponse("formula.html", {"request": requset})

@router.get('/')
async def index_html_content(requset: Request):
    return templates.TemplateResponse("index.html", {"request": requset})

@router.get("/convert")
async def convert_html_content(requset: Request):
    return templates.TemplateResponse("convert.html", {"request": requset})

@router.get("/instructions")
async def instructions_html_conent(requset: Request):
    return templates.TemplateResponse("instruction.html", {"request": requset})