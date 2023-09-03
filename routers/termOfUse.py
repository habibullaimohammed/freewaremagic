from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/terms-of-use",
    tags=["terms-of-use"],
    responses={404: {"description": "Not Found"}}
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_windows(request: Request):
    return templates.TemplateResponse("term-of-use.html", {"request": request})
