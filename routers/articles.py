from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .auth import get_current_user
import testModel
from config.database import engine, SessionLocal
from starlette import status
from starlette.responses import RedirectResponse


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not Found"}}
)

testModel.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def get_windows(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse("articles.html", {"request": request, "user": user})


@router.get("/add-article", response_class=HTMLResponse)
async def get_windows(request: Request):
    return templates.TemplateResponse("add-article.html", {"request": request})


@router.post("/add-article", response_class=HTMLResponse)
async def add_android_app(request: Request,
                          title: str = Form(),
                          sub_title: str = Form(),
                          quill_description: str = Form(),
                          image_url: str = Form(),
                          db: Session = Depends(get_db)
                          ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    article_model = testModel.Articles()
    article_model.title = title
    article_model.sub_title = sub_title
    article_model.quill_description = quill_description
    article_model.image_url = image_url
    article_model.owner_id = user.get("id")

    db.add(article_model)
    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/{title}", response_class=HTMLResponse)
async def get_windows(request: Request, title: str):
    return templates.TemplateResponse("article-details.html", {"request": request, "title": title})


