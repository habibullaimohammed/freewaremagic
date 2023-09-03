from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from routers import windows, mac, iphone, android, consoleGames, articles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(windows.router)
app.include_router(mac.router)
app.include_router(iphone.router)
app.include_router(android.router)
app.include_router(consoleGames.router)
app.include_router(articles.router)
