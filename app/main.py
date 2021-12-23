from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

from .library.md import *

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")

    return templates.TemplateResponse(
        "homepage.html", {"request": request, "page": "HOME", "data": data}
    )


@app.get("/resume", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("resume.md")

    return templates.TemplateResponse(
        "resume.html", {"request": request, "page": "RESUME", "data": data}
    )


@app.get("/articles", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("resume.md")

    return templates.TemplateResponse(
        "resume.html", {"request": request, "page": "ARTICLES", "data": data}
    )


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def page(request: Request, page_name: str):
    data = {"page": page_name}
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
