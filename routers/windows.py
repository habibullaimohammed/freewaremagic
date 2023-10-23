from fastapi import APIRouter, Depends, Request, Form, Query
from starlette import status
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user
import models
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/windows",
    tags=["windows"],
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
async def get_windows(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    windows_app = db.query(models.Windows).all()
    return templates.TemplateResponse("apps.html", {"request": request, "windows_app": windows_app, "user": user})


@router.get("/all-apps", response_class=HTMLResponse)
async def get_all_window_apps(request: Request, page: int = Query(1, alias="page"),
                               items_per_page: int = Query(2, alias="items_per_page"), db: Session = Depends(get_db)):
    # Calculate the offset based on the page number and items per page
    offset = (page - 1) * items_per_page

    # Fetch a subset of Android apps using the offset and items_per_page
    window_apps = db.query(models.Windows).offset(offset).limit(items_per_page).all()

    # Calculate the total number of Android apps in the database
    total_apps = db.query(models.Windows).count()

    # Calculate the total number of pages
    total_pages = (total_apps + items_per_page - 1) // items_per_page
    return templates.TemplateResponse("all-apps.html", {"request": request, "window_apps": window_apps, "page": page,
                                                        "items_per_page": items_per_page, "total_pages": total_pages,
                                                        "total_apps": total_apps})


@router.get("/top-downloads", response_class=HTMLResponse)
async def get_all_window_apps(request: Request, page: int = Query(1, alias="page"),
                               items_per_page: int = Query(2, alias="items_per_page"), db: Session = Depends(get_db)):
    # Calculate the offset based on the page number and items per page
    offset = (page - 1) * items_per_page

    # Fetch a subset of Android apps using the offset and items_per_page
    window_apps = db.query(models.Windows).offset(offset).limit(items_per_page).all()

    # Calculate the total number of Android apps in the database
    total_apps = db.query(models.Windows).count()

    # Calculate the total number of pages
    total_pages = (total_apps + items_per_page - 1) // items_per_page
    return templates.TemplateResponse("top-downloads.html",
                                      {"request": request, "window_apps": window_apps, "page": page,
                                       "items_per_page": items_per_page, "total_pages": total_pages,
                                       "total_apps": total_apps})


# @router.get("/software/{name}")
# async def window_app_details(name: str, request: Request, db: Session = Depends(get_db)):
#     name = name.replace("-", " ")
#     user = await get_current_user(request)
#     app_details = db.query(models.Windows).filter(models.Windows.name == name).first()
#     window_apps = db.query(models.Windows).all()
#     return templates.TemplateResponse("app-details.html", {"request": request, "app_details": app_details, "user": user,
#                                                            "window_apps": window_apps})


@router.get("/software/{name}/download")
async def window_app_download(name: str, request: Request, db: Session = Depends(get_db)):
    name = name.replace("-", " ")
    name = name.capitalize()
    user = await get_current_user(request)
    app_details = db.query(models.Windows).filter(models.Windows.name == name).first()
    window_apps = db.query(models.Windows).all()
    return templates.TemplateResponse("download.html", {"request": request, "app_details": app_details, "user": user,
                                                        "window_apps": window_apps})


@router.get("/add-window-apps", response_class=HTMLResponse)
async def add_new_window_app(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-android-software.html", {"request": request, "user": user})


@router.post("/add-window-apps", response_class=HTMLResponse)
async def add_window_app(request: Request,
                          name: str = Form(),
                          title: str = Form(),
                          developer: str = Form(),
                          quill_description: str = Form(),
                          image_url: str = Form(),
                          background_image_url: str = Form(),
                          download_url_getintopc: str = Form(),
                          download_url_igetintopc: str = Form(),
                          download_url_softonic: str = Form(),
                          download_url_filehippo: str = Form(),
                          download_url_moddroid: str = Form(),
                          category: str = Form(),
                          sub_category: str = Form(),
                          db: Session = Depends(get_db)
                          ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    window_model = models.Windows()
    window_model.name = name
    window_model.title = title
    window_model.developer = developer
    window_model.quill_description = quill_description
    window_model.image_url = image_url
    window_model.background_image_url = background_image_url
    window_model.download_url_getintopc = download_url_getintopc
    window_model.download_url_igetintopc = download_url_igetintopc
    window_model.download_url_softonic = download_url_softonic
    window_model.download_url_filehippo = download_url_filehippo
    window_model.download_url_moddroid = download_url_moddroid
    window_model.category = category
    window_model.sub_category = sub_category
    window_model.owner_id = user.get("id")

    db.add(window_model)
    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{title}")
async def delete_todo(request: Request, title: str, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(models.Windows).filter(models.Windows.title == title).filter(
        models.Windows.owner_id == user.get("id")).first()
    if todo_model is None:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    db.query(models.Windows).filter(models.Windows.title == title).delete()
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/{category}")
async def window_category(category: str, request: Request, db: Session = Depends(get_db)):
    category = category.replace("-", " ")
    current_category = db.query(models.Windows).filter(models.Windows.category == category).all()
    return templates.TemplateResponse("app-category.html",
                                      {"request": request, "current_category": current_category, "category": category})


@router.get("/{category}/{sub_category}")
async def window_subcategory(category: str, sub_category: str, request: Request, db: Session = Depends(get_db)):
    category = category.replace("-", " ")
    sub_category = sub_category.replace("-", " ")

    current_category = db.query(models.Windows).filter(
        models.Windows.category == category,
        models.Windows.sub_category == sub_category
    ).all()

    return templates.TemplateResponse("app-sub-category.html",
                                      {"request": request, "current_category": current_category, "category": category,
                                       "sub_category": sub_category})


@router.post("/increase-download-count/{name}")
async def increase_download_count(name: str, db: Session = Depends(get_db)):
    # Assuming title is a unique identifier for the Android app
    name = name.replace("-", " ")

    # Query the Android app by title
    window_app = db.query(models.Windows).filter(models.Windows.name == name).first()

    if window_app:
        # Increase the download count by 1 (you can adjust the increment as needed)
        window_app.download_count += 1

        # Commit the changes to the database
        db.commit()

        return {"message": f"Download count for {window_app.name} increased successfully"}
    else:
        return {"error": "Android app not found"}

# You can call this route from your HTML templates or frontend code whenever a download button is clicked.
