from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .auth import get_current_user
import models
from config.database import engine, SessionLocal
from starlette import status
from starlette.responses import RedirectResponse


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not Found"}}
)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def get_windows(request: Request, page: int = Query(1, alias="page"), items_per_page: int = Query(1, alias="items_per_page"), db: Session = Depends(get_db)):
    user = await get_current_user(request)

    offset = (page - 1) * items_per_page

    articles = db.query(models.Articles).all()
    all_articles = db.query(models.Articles).offset(offset).limit(items_per_page).all()
    total_article = db.query(models.Articles).count()
    total_pages = (total_article + items_per_page - 1) // items_per_page
    return templates.TemplateResponse("articles.html", {"request": request, "user": user, "articles": articles, "all_articles": all_articles, "page": page, "items_per_page": items_per_page, "total_pages": total_pages, "total_article": total_article})


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
    article_model = models.Articles()
    article_model.title = title
    article_model.sub_title = sub_title
    article_model.quill_description = quill_description
    article_model.image_url = image_url
    article_model.owner_id = user.get("id")

    db.add(article_model)
    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/{title}", response_class=HTMLResponse)
async def get_windows(request: Request, title: str, db: Session = Depends(get_db)):
    title = title.replace("-", " ")
    articles = db.query(models.Articles).all()
    article_details = db.query(models.Articles).filter(models.Articles.title == title).first()
    return templates.TemplateResponse("article-details.html", {"request": request, "title": title, "article_details": article_details, "articles": articles})


