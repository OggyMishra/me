from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import EXPERIENCE, PROJECTS, SITE, SKILLS
from app.markdown_engine import get_all_posts, get_post, get_pygments_css

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")


def ctx(request: Request, **kwargs) -> dict:
    """Build a common template context."""
    return {"request": request, "site": SITE, **kwargs}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    posts = get_all_posts()[:3]
    return templates.TemplateResponse(
        "index.html",
        ctx(request, projects=PROJECTS, recent_posts=posts, skills=SKILLS),
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        ctx(request, experience=EXPERIENCE, skills=SKILLS),
    )


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    return templates.TemplateResponse(
        "projects.html",
        ctx(request, projects=PROJECTS),
    )


@app.get("/blog", response_class=HTMLResponse)
async def blog_index(request: Request):
    posts = get_all_posts()
    return templates.TemplateResponse(
        "blog/index.html",
        ctx(request, posts=posts),
    )


@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    post = get_post(slug)
    if post is None:
        return HTMLResponse("Not found", status_code=404)
    pygments_css = get_pygments_css()
    return templates.TemplateResponse(
        "blog/post.html",
        ctx(request, post=post, pygments_css=pygments_css),
    )
