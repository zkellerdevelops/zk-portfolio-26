# zachkeller.net — portfolio

A hand-built static recreation of my Webflow portfolio, ready to host on GitHub Pages.
No build step, no framework — just HTML, one CSS file, and one small JS file.

## Structure

```
index.html                          Home (hero + project grid)
work/
  amazon-haul/index.html            (password gated)
  amazon-climate-pledge-friendly/   (password gated)
  amazon-explore-v2/                (password gated)
  lonely-planet-search/
  lonely-planet-destinations/
assets/
  css/style.css
  js/gate.js                        Client-side password gate
  img/                              All images (self-hosted)
```

Clean URLs (`/work/amazon-haul`) work because each page is an `index.html` in its own folder.

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

## Deploy to GitHub Pages

1. Push this folder to a repo (e.g. `zkellerdevelops.github.io` for a root user site, or any
   repo with Pages enabled).
2. In **Settings → Pages**, set the source to the branch and `/ (root)` folder.
3. For a custom domain (`zachkeller.net`): add a `CNAME` file containing `www.zachkeller.net`
   and point your DNS at GitHub Pages.

Paths are relative, so the site also works from a project subpath (`user.github.io/repo/`).
