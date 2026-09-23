# zachkeller.net — portfolio

A static recreation of my Webflow portfolio, ready to host on GitHub Pages.
Content lives in JSON; a tiny zero-dependency Python script renders the HTML.

## Structure

```
content/                            SOURCE OF TRUTH — edit these
  site.json                         Name, tagline, socials, contact, meta
  projects/<slug>.json              One file per project (order, copy, images)
build.py                            Renders content/ -> HTML (stdlib only)

index.html                          GENERATED — home (hero + project grid)
work/<slug>/index.html              GENERATED — one per project
assets/
  css/style.css
  js/gate.js                        Client-side password gate
  img/                              All images (self-hosted)
```

The `index.html` files are **generated** — edit `content/`, then run `python3 build.py`.
The generated HTML is committed too, so any host (even plain GitHub Pages with no build
step) serves the site as-is.

Clean URLs (`/work/amazon-haul`) work because each page is an `index.html` in its own folder.

## Editing content

Everything is driven by the JSON in `content/`. After any edit, run:

```bash
python3 build.py
```

**Edit text / a project:** open the relevant `content/projects/<slug>.json` (or
`content/site.json`) and change the values. Prose fields may contain inline HTML
(`<br>`, `<strong>`, `<em>`); all other text is auto-escaped.

**Add a new project / case study:**
1. Copy an existing file, e.g. `cp content/projects/amazon-haul.json content/projects/my-project.json`
2. Edit it: set a unique `slug`, an `order` (controls grid position), `card_title`,
   `thumbnail`, `title`, `role`, `overview`, `goal`, and the `blocks` array.
3. Drop the referenced images into `assets/img/` (filenames must match).
4. Run `python3 build.py`. A new `work/my-project/index.html` appears and the home
   grid updates automatically.

**Project JSON fields:**
| Field | Purpose |
|---|---|
| `slug` | URL segment + folder name (`work/<slug>/`) |
| `order` | Position in the home grid (ascending) |
| `card_title`, `thumbnail` | Home-grid card label + image |
| `has_page` | `false` = grid card only, no page (e.g. Deals & Promotions) |
| `protected` | `true` = client-side password gate |
| `title`, `role`, `overview`, `goal` | Case-study header |
| `overview_launch` | Optional `{label, url}` button in the header |
| `blocks` | Ordered content: see block types below |

**Block types** (each entry in `blocks`):
- `{"type": "feature_img", "desktop": "a.png", "mobile": "b.png"}` — full-width image (auto-swaps at 767px)
- `{"type": "desc", "heading": "...", "body": "..."}` — text section (two-column on desktop)
- `{"type": "imgs", "desktop": ["a.png"], "mobile": ["b.png"]}` — one or more full-width images
- `{"type": "launch_center", "label": "...", "url": "..."}` — centered launch button

## Password-protected pages

The three Amazon case studies are gated with a client-side prompt (password: `thinkbig`),
mirroring the original Webflow protection.

**This is not real security.** The content ships inside the page HTML and is visible to
anyone who views source or inspects network traffic. It only stops casual browsing. If any
of this material is confidential, do not publish it to a public site — use a private,
authenticated host instead.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Editing in a browser (Pages CMS)

[Pages CMS](https://pagescms.org) gives a clean web UI for editing content — no code,
no local setup. It's configured by [`.pages.yml`](.pages.yml) at the repo root.

**One-time setup:**
1. Go to [app.pagescms.org](https://app.pagescms.org) and sign in with GitHub.
2. Authorize it for the `zkellerdevelops/zk-portfolio-26` repo.
3. It reads `.pages.yml` and shows **Site settings** + a **Projects** collection.

**Editing:** change fields in the UI and save. Pages CMS commits to `content/*.json`,
which triggers the GitHub Action below to rebuild and redeploy — changes go live in a
minute or two. Images upload straight into `assets/img/`.

The `blocks` field is a drag-orderable list where each item is one of: **Image(s)**,
**Text section**, or **Centered launch button** — the same structure `build.py` renders.

## Deployment (GitHub Actions)

[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) runs `build.py` and deploys
to GitHub Pages on every push to `main` (including Pages CMS commits).

**One-time setup:** in **Settings → Pages**, set **Source: GitHub Actions**.

This repo isn't named `zkellerdevelops.github.io`, so it deploys to
`zkellerdevelops.github.io/zk-portfolio-26/`. Paths are relative, so the subpath works.

**Custom domain (`zachkeller.net`):** add a `CNAME` file at the repo root containing
`www.zachkeller.net`, set it under Settings → Pages → Custom domain, and point your DNS
at GitHub Pages.

> Note: the generated HTML is also committed for portability (any static host works with
> no build). After editing content locally, run `python3 build.py` before committing so the
> committed HTML stays in sync. The live site is always rebuilt by the Action regardless.
