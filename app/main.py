from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

from library.md import *
from library.notion_conn import get_all_domains, get_article_list, get_article
from library import config as cfg

import re

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")

    nav_text = ["curly-giggle", "home"]
    nav_path = ["/" if path == "curly-giggle" else "/" + path for path in nav_text]
    nav_text = [text.upper() for text in nav_text]

    title = "curly-giggle"

    return templates.TemplateResponse(
        "homepage.html",
        {
            "request": request,
            "page": list(zip(nav_text, nav_path)),
            "title": title,
            "data": data,
        },
    )


@app.get("/resume", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("resume.md")

    nav_text = ("curly-giggle" + request.url.path).split("/")
    nav_path = ["/" if path == "curly-giggle" else "/" + path for path in nav_text]
    nav_text = [text.upper() for text in nav_text]

    title = "Resume • curly-giggle"

    return templates.TemplateResponse(
        "resume.html",
        {
            "request": request,
            "page": list(zip(nav_text, nav_path)),
            "title": title,
            "data": data,
        },
    )


@app.get("/articles", response_class=HTMLResponse)
async def home(request: Request):
    domains = get_all_domains(cfg.DATABASE_ID, cfg.HEADERS)

    title = "Articles • curly-giggle"

    nav_text = ("curly-giggle" + request.url.path).split("/")
    nav_path = ["/" if path == "curly-giggle" else "/" + path for path in nav_text]
    nav_text = [text.upper() for text in nav_text]

    articles = {}

    for domain in domains:
        articles[domain] = get_article_list(cfg.DATABASE_ID, cfg.HEADERS, domain)

    return templates.TemplateResponse(
        "articles.html",
        {
            "request": request,
            "page": list(zip(nav_text, nav_path)),
            "data": articles,
            "title": title,
            "color": domains,
        },
    )


@app.get("/articles/{url}", response_class=HTMLResponse)
async def home(request: Request, url: str):
    id = re.findall(r"-\w+$", url)[0]
    nav_text = ("curly-giggle" + request.url.path).split("/")
    nav_path = ["/" if path == "curly-giggle" else "/" + path for path in nav_text]
    nav_text[-1] = nav_text[-1].replace(id, "")
    title = nav_text[-1].replace("-", " ") + " • curly-giggle"
    nav_text = [text.upper() for text in nav_text]
    id = re.findall(r"-\w+$", url)[0][1:]

    cover, data = get_article(id, cfg.HEADERS)

    return templates.TemplateResponse(
        "content.html",
        {
            "request": request,
            "page": list(zip(nav_text, nav_path)),
            "title": title,
            "data": data,
            "cover": cover,
        },
    )
