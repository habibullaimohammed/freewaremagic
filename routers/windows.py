from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/windows",
    tags=["windows"],
    responses={404: {"description": "Not Found"}}
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_windows(request: Request):
    return templates.TemplateResponse("apps.html", {"request": request})


@router.get("/games", response_class=HTMLResponse)
async def get_windows(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})