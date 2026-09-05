# website

Slug-based static site hosting on GitHub Pages.

## Live URLs

- Portal: https://singhalshubham89.github.io/website/
- DSA Cheat Sheet: https://singhalshubham89.github.io/website/dsa-cheat-sheet/
- Resume: https://singhalshubham89.github.io/website/resume/

## How it works

Each site uses a **slug** as its public path:

```text
https://singhalshubham89.github.io/website/<slug>/
```

Repository layout:

```text
website/
  index.html                 # portal
  sites.json                 # slug registry
  <slug>/
    index.html               # site entry point
    assets/                  # optional css/js/images
  scripts/
    new-site.sh              # scaffold a new site
    validate-sites.sh        # verify registry + folders
```

## Add a new site

```bash
./scripts/new-site.sh my-portfolio "My Portfolio" \
  --description "Personal projects and resume." \
  --tags portfolio,resume
```

Then replace `my-portfolio/index.html` with your static site (or add more files under that folder).

Register manually instead:

1. Create `<slug>/index.html`
2. Add an entry to `sites.json`:

```json
{
  "slug": "my-portfolio",
  "title": "My Portfolio",
  "description": "Personal projects and resume.",
  "tags": ["portfolio", "resume"]
}
```

3. Validate, commit, and push:

```bash
./scripts/validate-sites.sh
git add .
git commit -m "Add my-portfolio site."
git push
```

## Slug rules

- Lowercase letters, numbers, and hyphens only
- Example: `dsa-cheat-sheet`, `tax-calculator`, `blog2026`
- Slug folder name must match `sites.json`

## Local preview

```bash
python3 -m http.server 8080
```

Open http://localhost:8080
