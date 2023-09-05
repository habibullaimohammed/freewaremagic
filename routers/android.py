from fastapi import APIRouter, Depends, Request, Form
from starlette import status
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user
import testModel
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/android",
    tags=["android"],
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
async def get_windows(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    android_apps = db.query(testModel.Android).all()
    app_details = db.query(testModel.Android).all()
    return templates.TemplateResponse("apps.html", {"request": request, "android_apps": android_apps, "user": user, "app_details": app_details})


@router.get("/add-android-apps", response_class=HTMLResponse)
async def add_new_android_software(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-android-software.html", {"request": request, "user": user})


@router.post("/add-android-apps", response_class=HTMLResponse)
async def add_android_app(request: Request,
                          title: str = Form(),
                          description: str = Form(),
                          image_url: str = Form(),
                          download_url: str = Form(),
                          download_url2: str = Form(),
                          category: str = Form(),
                          sub_category: str = Form(),
                          db: Session = Depends(get_db)
                          ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    android_model = testModel.Android()
    android_model.title = title
    android_model.description = description
    android_model.image_url = image_url
    android_model.download_url = download_url
    android_model.download_url2 = download_url2
    android_model.category = category
    android_model.sub_category = sub_category
    android_model.owner_id = user.get("id")

    db.add(android_model)
    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/edit-android-apps/{title}", response_class=HTMLResponse)
async def edit_android_software(title: str, request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    title = title.replace("-", " ")
    app_details = db.query(testModel.Android).filter(testModel.Android.title == title).first()
    return templates.TemplateResponse("edit-android-software.html", {"request": request, "user": user, "app_details": app_details})


@router.post("/edit-android-apps/{title}", response_class=HTMLResponse)
async def edit_android_app(request: Request,
                          title_name: str = Form(),
                          description: str = Form(),
                          image_url: str = Form(),
                          download_url: str = Form(),
                          download_url2: str = Form(),
                          category_name: str = Form(),
                          sub_category: str = Form(),
                          db: Session = Depends(get_db)
                          ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    title_name = title_name.replace("-", " ")
    android_model = testModel.Android()
    android_model.title = title_name
    android_model.description = description
    android_model.image_url = image_url
    android_model.download_url = download_url
    android_model.download_url2 = download_url2
    android_model.category = category_name
    android_model.sub_category = sub_category
    android_model.owner_id = user.get("id")

    db.add(android_model)
    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{title}")
async def delete_todo(request: Request, title: str, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(testModel.Android).filter(testModel.Android.title == title).filter(testModel.Android.owner_id == user.get("id")).first()
    if todo_model is None:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    db.query(testModel.Android).filter(testModel.Android.title == title).delete()
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/{category}")
async def android_category(category: str, request: Request, db: Session = Depends(get_db)):
    category = category.replace("-", " ")
    current_category = db.query(testModel.Android).filter(testModel.Android.category == category).all()
    return templates.TemplateResponse("app-category.html", {"request": request, "current_category": current_category, "category": category})


@router.get("/{category}/{title}")
async def android_category(category: str, title: str, request: Request, db: Session = Depends(get_db)):
    title = title.replace("-", " ")
    app_details = db.query(testModel.Android).filter(testModel.Android.title == title).first()
    return templates.TemplateResponse("app-details.html", {"request": request, "app_details": app_details})



