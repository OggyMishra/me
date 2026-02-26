"""Static site freezer — crawls the FastAPI app and saves HTML to dist/."""

import asyncio
import shutil
from pathlib import Path

from httpx import ASGITransport, AsyncClient

from app.main import app
from app.markdown_engine import get_all_posts

BASE_DIR = Path(__file__).resolve().parent
DIST = BASE_DIR / "dist"


async def build():
    # Clean dist
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        # Static routes
        routes = ["/", "/about", "/projects", "/blog"]

        # Blog post routes
        for post in get_all_posts():
            routes.append(f"/blog/{post['slug']}")

        # Fetch and save each route
        for route in routes:
            resp = await client.get(route)
            if resp.status_code != 200:
                print(f"  WARN: {route} returned {resp.status_code}")
                continue

            # Determine output path
            if route == "/":
                out = DIST / "index.html"
            else:
                out = DIST / route.lstrip("/") / "index.html"

            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(resp.text, encoding="utf-8")
            print(f"  OK: {route} -> {out.relative_to(DIST)}")

    # Copy static assets
    src_static = BASE_DIR / "static"
    dst_static = DIST / "static"
    if src_static.exists():
        shutil.copytree(src_static, dst_static)
        print(f"  Copied static/ -> dist/static/")

    # Copy CNAME
    cname = BASE_DIR / "CNAME"
    if cname.exists():
        shutil.copy2(cname, DIST / "CNAME")
        print(f"  Copied CNAME")

    # Copy favicon
    favicon = BASE_DIR / "static" / "images" / "favicon.ico"
    if favicon.exists():
        shutil.copy2(favicon, DIST / "favicon.ico")
        print(f"  Copied favicon.ico")

    print(f"\nBuild complete. Output in {DIST}/")


if __name__ == "__main__":
    asyncio.run(build())
