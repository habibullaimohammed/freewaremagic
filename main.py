from fastapi import FastAPI, Request
import testModel
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse
from routers.auth import get_current_user
from routers import windows, mac, iphone, android, consoleGames, articles, contact, cookiePolicy, privacyPolicy, termOfUse, users, auth

app = FastAPI()
testModel.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = await get_current_user(request)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(windows.router)
app.include_router(mac.router)
app.include_router(iphone.router)
app.include_router(android.router)
app.include_router(articles.router)
app.include_router(consoleGames.router)
app.include_router(contact.router)
app.include_router(cookiePolicy.router)
app.include_router(privacyPolicy.router)
app.include_router(termOfUse.router)
