from pathlib import Path

import frontmatter
import markdown
from pygments.formatters import HtmlFormatter

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"

md = markdown.Markdown(
    extensions=[
        "fenced_code",
        "codehilite",
        "tables",
        "toc",
        "meta",
        "smarty",
    ],
    extension_configs={
        "codehilite": {"css_class": "highlight", "linenums": False},
        "toc": {"permalink": True},
    },
)


def get_pygments_css() -> str:
    """Return Pygments CSS for the 'monokai' theme."""
    return HtmlFormatter(style="monokai").get_style_defs(".highlight")


def parse_post(filepath: Path) -> dict:
    """Parse a Markdown file with YAML frontmatter and return metadata + HTML."""
    post = frontmatter.load(filepath)
    md.reset()
    html = md.convert(post.content)
    toc = getattr(md, "toc", "")

    reading_time = max(1, len(post.content.split()) // 200)

    return {
        "title": post.get("title", filepath.stem),
        "date": post.get("date"),
        "tags": post.get("tags", []),
        "description": post.get("description", ""),
        "status": post.get("status", "merged"),
        "slug": filepath.stem,
        "content": html,
        "toc": toc,
        "reading_time": reading_time,
    }


def get_all_posts() -> list[dict]:
    """Load all blog posts from the content/blog directory, sorted by date desc."""
    blog_dir = CONTENT_DIR / "blog"
    if not blog_dir.exists():
        return []
    posts = []
    for f in blog_dir.glob("*.md"):
        posts.append(parse_post(f))
    posts.sort(key=lambda p: p["date"] or "", reverse=True)
    return posts


def get_post(slug: str) -> dict | None:
    """Load a single blog post by slug."""
    blog_dir = CONTENT_DIR / "blog"
    filepath = blog_dir / f"{slug}.md"
    if not filepath.exists():
        return None
    return parse_post(filepath)
