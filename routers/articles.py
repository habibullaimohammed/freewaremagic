from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not Found"}}
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_windows(request: Request):
    return templates.TemplateResponse("articles.html", {"request": request})


@router.get("/add-article", response_class=HTMLResponse)
async def get_windows(request: Request):
    return templates.TemplateResponse("add-article.html", {"request": request})

@router.get("/{title}", response_class=HTMLResponse)
async def get_windows(request: Request, title: str):
    return templates.TemplateResponse("article-details.html", {"request": request, "title": title})


