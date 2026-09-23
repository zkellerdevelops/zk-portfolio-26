#!/usr/bin/env python3
"""Static site build for zachkeller.net.

Reads content from content/ (JSON) and writes HTML to the repo root:
  - index.html                 (home: hero + project grid)
  - work/<slug>/index.html      (one per project with "has_page": true)

Zero dependencies — standard library only. Run:  python3 build.py

Image paths in content are repo-root-relative (e.g. "assets/img/foo.png"),
matching Pages CMS media output. build.py prepends a per-page prefix so the
links resolve from the home page (root) and from work pages (../../).

To add a project: create content/projects/<slug>.json (copy an existing one),
drop its images in assets/img/, then run this script. See README.md.
"""
import json
import os
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")

HOME_PREFIX = ""        # home page lives at repo root
WORK_PREFIX = "../../"  # work/<slug>/ pages are two levels deep


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_projects():
    d = os.path.join(CONTENT, "projects")
    projects = [load_json(os.path.join(d, f)) for f in os.listdir(d) if f.endswith(".json")]
    projects.sort(key=lambda p: p.get("order", 999))
    return projects


# ---------- shared partials ----------
def head(title, prefix, extra_meta=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
{extra_meta}  <link rel="shortcut icon" type="image/png" href="{prefix}{SITE['favicon']}" />
  <link rel="apple-touch-icon" href="{prefix}{SITE['apple_icon']}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;0,900;1,400&family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{prefix}assets/css/style.css" />
</head>
"""


def footer(link_href, prefix):
    return f"""  <footer class="footer-wrap">
    <a href="{link_href}" class="footer-link">
      <img src="{prefix}{SITE['logo']}" width="15" alt="ZLK logo" class="footer-logo" />
      <span class="paragraph-tiny">{escape(SITE['footer'])}</span>
    </a>
  </footer>
"""


def contact_section():
    c = SITE["contact"]
    return f"""      <section class="section"><div class="container">
        <div class="email-section">
          <h3>{escape(c['heading'])}</h3>
          <p>{escape(c['blurb'])}</p>
          <a class="email-link" href="mailto:{c['email']}?subject=You've%20got%20mail!">{escape(c['email'])}</a>
        </div>
      </div></section>
"""


# ---------- home ----------
def build_home(projects):
    px = HOME_PREFIX
    meta = SITE["meta"]
    extra = f"""  <meta name="description" content="{escape(meta['description'])}" />
  <meta property="og:title" content="{escape(meta['og_title'])}" />
  <meta property="og:description" content="{escape(meta['description'])}" />
  <meta property="og:image" content="{px}{meta['og_image']}" />
  <meta property="og:type" content="website" />
  <meta name="twitter:card" content="summary_large_image" />
"""
    social = "\n".join(
        f'          <a href="{s["url"]}" target="_blank" rel="noopener" class="link-box"><img src="{px}{s["icon"]}" alt="{escape(s["name"])}" /></a>'
        for s in SITE["social"]
    )

    cards = []
    for p in projects:
        title = escape(p["card_title"])
        img = f'<img src="{px}{p["thumbnail"]}" alt="{title} thumbnail" />'
        label = f'<div class="project-title">{title}</div>'
        if p.get("has_page"):
            cards.append(f'        <a href="work/{p["slug"]}/" class="project-card">\n          {img}\n          {label}\n        </a>')
        else:
            cards.append(f'        <span class="project-card is-disabled" aria-disabled="true">\n          {img}\n          {label}\n        </span>')
    grid = "\n".join(cards)

    doc = head(meta["title"], px, extra) + f"""<body>
  <nav class="navigation">
    <a href="/" class="logo-link" aria-current="page">
      <img src="{px}{SITE['logo']}" width="75" alt="ZLK logo" class="logo-image" />
    </a>
  </nav>

  <main class="section">
    <div class="container">
      <section class="intro-wrap">
        <div class="name-text">{escape(SITE['name'])}</div>
        <div class="paragraph-light">{escape(SITE['role'])}</div>
        <div class="hello">{escape(SITE['hello'])}</div>
        <h1 class="tagline">{escape(SITE['tagline'])}</h1>
        <div class="social-row">
{social}
        </div>
      </section>

      <section class="project-grid">
{grid}
      </section>
    </div>
  </main>

{footer("/", px)}</body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print("built index.html")


# ---------- case study blocks ----------
def render_block(b, px):
    t = b.get("type")
    if t == "images":
        top = b.get("top_spacing", False)
        parts = ['<section class="section feature-img"><div class="container">']
        for i, d in enumerate(b.get("desktop", [])):
            extra = " top-spacing" if (top and i > 0) else ""
            parts.append(f'<img class="detail-header-image img-desktop{extra}" src="{px}{d}" alt="" loading="lazy" />')
        for m in b.get("mobile", []):
            parts.append(f'<img class="detail-header-image img-mobile" src="{px}{m}" alt="" loading="lazy" />')
        parts.append('</div></section>')
        return "\n      ".join(parts)
    if t == "desc":
        # body may contain intentional inline HTML (<br>, <strong>, <em>) — kept as-is
        return ('<section class="section"><div class="container">\n'
                '        <div class="project-description-grid">\n'
                f'          <div><div class="position-name-text">{escape(b["heading"])}</div></div>\n'
                f'          <div class="paragraph-light">{b["body"]}</div>\n'
                '        </div>\n      </div></section>')
    if t == "launch_center":
        return ('<section class="launch-centered">\n'
                f'        <div class="position-name-text" style="text-align:center">{escape(b["label"])}</div>\n'
                f'        <a href="{b["url"]}" target="_blank" rel="noopener" class="button-2">Launch</a>\n'
                '      </section>')
    return ""


def build_project(p):
    px = WORK_PREFIX
    protected = p.get("protected", False)
    extra = f'  <meta property="og:title" content="{escape(p["title"])}" />\n'

    gate = ""
    if protected:
        gate = """
  <div class="gate">
    <h1>Protected work</h1>
    <p class="paragraph-light">This case study is password protected. Enter the password to continue.</p>
    <form id="gate-form">
      <input id="gate-input" type="password" placeholder="Enter password" autofocus />
      <button type="submit">Submit</button>
    </form>
    <div id="gate-error" class="error"></div>
  </div>
"""

    ovl = ""
    if p.get("overview_launch"):
        ol = p["overview_launch"]
        ovl = ('\n          <div class="launch-block">\n'
               f'            <div class="position-name-text">{escape(ol["label"])}</div>\n'
               f'            <a href="{ol["url"]}" target="_blank" rel="noopener" class="button-2">Launch</a>\n'
               '          </div>')

    wrap_open = "<div data-protected>" if protected else "<div>"
    blocks_html = "\n      ".join(render_block(b, px) for b in p.get("blocks", []))

    doc = head(p["title"], px, extra) + f"""<body>
  <nav class="navigation">
    <a href="../../" class="logo-link"><img src="{px}{SITE['logo']}" width="75" alt="ZLK logo" class="logo-image" /></a>
  </nav>
{gate}  <main class="content">
    {wrap_open}
      <section class="section"><div class="container">
        <div class="project-overview-grid">
          <div>
            <h1 class="heading-jumbo">{escape(p["title"])}</h1>
            <div class="paragraph-light">{escape(p["role"])}</div>
          </div>
          <div>
            <div class="position-name-text">Project Overview</div>
            <div class="paragraph-light">{escape(p["overview"])}</div>
          </div>
          <div>
            <div class="position-name-text">Project Goal</div>
            <div class="paragraph-light">{escape(p["goal"])}</div>
          </div>{ovl}
        </div>
      </div></section>
      {blocks_html}
{contact_section()}    </div>
  </main>

{footer("../../", px)}"""
    if protected:
        doc += "  <script src=\"../../assets/js/gate.js\"></script>\n"
    doc += "</body>\n</html>\n"

    d = os.path.join(ROOT, "work", p["slug"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"built work/{p['slug']}/index.html")


SITE = load_json(os.path.join(CONTENT, "site.json"))


def main():
    projects = load_projects()
    build_home(projects)
    for p in projects:
        if p.get("has_page"):
            build_project(p)
    print("done.")


if __name__ == "__main__":
    main()
