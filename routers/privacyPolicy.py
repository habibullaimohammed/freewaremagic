from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/privacy-policy",
    tags=["privacy-policy"],
    responses={404: {"description": "Not Found"}}
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_windows(request: Request):
    return templates.TemplateResponse("privacy-policy.html", {"request": request})
