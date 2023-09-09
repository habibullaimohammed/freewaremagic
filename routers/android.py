from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query
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
    return templates.TemplateResponse("apps.html", {"request": request, "android_apps": android_apps, "user": user})


@router.get("/all-apps", response_class=HTMLResponse)
async def get_all_android_apps(request: Request, page: int = Query(1, alias="page"), items_per_page: int = Query(2, alias="items_per_page"), db: Session = Depends(get_db)):
    # Calculate the offset based on the page number and items per page
    offset = (page - 1) * items_per_page

    # Fetch a subset of Android apps using the offset and items_per_page
    android_apps = db.query(testModel.Android).offset(offset).limit(items_per_page).all()

    # Calculate the total number of Android apps in the database
    total_apps = db.query(testModel.Android).count()

    # Calculate the total number of pages
    total_pages = (total_apps + items_per_page - 1) // items_per_page
    return templates.TemplateResponse("all-apps.html", {"request": request, "android_apps": android_apps,  "page": page, "items_per_page": items_per_page, "total_pages": total_pages})


@router.get("/top-downloads", response_class=HTMLResponse)
async def get_windows(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    android_apps = db.query(testModel.Android).all()
    return templates.TemplateResponse("top-downloads.html", {"request": request, "android_apps": android_apps, "user": user})


@router.get("/software/{title}")
async def android_app(title: str, request: Request, db: Session = Depends(get_db)):
    title = title.replace("-", " ")
    user = await get_current_user(request)
    app_details = db.query(testModel.Android).filter(testModel.Android.title == title).first()
    android_apps = db.query(testModel.Android).all()
    return templates.TemplateResponse("app-details.html", {"request": request, "app_details": app_details, "user": user,
                                                           "android_apps": android_apps})


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
                          quill_description: str = Form(),
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
    android_model.quill_description = quill_description
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
    return templates.TemplateResponse("edit-android-software.html",
                                      {"request": request, "user": user, "app_details": app_details})


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

    todo_model = db.query(testModel.Android).filter(testModel.Android.title == title).filter(
        testModel.Android.owner_id == user.get("id")).first()
    if todo_model is None:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    db.query(testModel.Android).filter(testModel.Android.title == title).delete()
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/{category}")
async def android_category(category: str, request: Request, db: Session = Depends(get_db)):
    category = category.replace("-", " ")
    current_category = db.query(testModel.Android).filter(testModel.Android.category == category).all()
    return templates.TemplateResponse("app-category.html",
                                      {"request": request, "current_category": current_category, "category": category})


@router.get("/{category}/{sub_category}")
async def android_category(category: str, sub_category: str, request: Request, db: Session = Depends(get_db)):
    category = category.replace("-", " ")
    sub_category = sub_category.replace("-", " ")

    current_category = db.query(testModel.Android).filter(
        testModel.Android.category == category,
        testModel.Android.sub_category == sub_category
    ).all()

    return templates.TemplateResponse("app-sub-category.html",
                                      {"request": request, "current_category": current_category, "category": category,
                                       "sub_category": sub_category})


@router.post("/increase-download-count/{title}")
async def increase_download_count(title: str, db: Session = Depends(get_db)):
    # Assuming title is a unique identifier for the Android app
    title = title.replace("-", " ")

    # Query the Android app by title
    android_app = db.query(testModel.Android).filter(testModel.Android.title == title).first()

    if android_app:
        # Increase the download count by 1 (you can adjust the increment as needed)
        android_app.download_count += 1

        # Commit the changes to the database
        db.commit()

        return {"message": f"Download count for {android_app.title} increased successfully"}
    else:
        return {"error": "Android app not found"}

# You can call this route from your HTML templates or frontend code whenever a download button is clicked.
