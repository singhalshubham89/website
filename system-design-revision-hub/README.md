# System Design Interview Revision Hub

Static, offline-friendly revision site for **HLD**, **LLD**, **distributed systems**, **Java concurrency**, **design patterns**, **case studies**, and **interview prep**.

## Tech

- HTML5, CSS3, vanilla ES6+ JavaScript
- [Mermaid.js](https://mermaid.js.org/) (CDN) for diagrams
- [Prism.js](https://prismjs.com/) (CDN) for Java syntax highlighting
- `localStorage` for theme, bookmarks, revision checkboxes, and recently viewed topics

No frameworks, no backend, no build step required to **use** the site.

Content depth uses honest **`status`**: `complete` (curated code/diagrams), `partial` (template prose). Regenerate after editing `generate_data.py`.

## Quick start

### Option A — local HTTP server (recommended)

Mermaid and some CDNs behave more reliably over HTTP:

```bash
cd system-design-revision-hub
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

### Option B — open file directly

Open `index.html` in your browser. If diagrams fail to load, use Option A.

## Structure

| File | Purpose |
|------|---------|
| `index.html` | Shell, CDN scripts, data bundles |
| `styles.css` | Layout, dark/light theme, print styles |
| `app.js` | Routing, search, render, progress, bookmarks |
| `data/*.js` | Topic content (generated) |
| `generate_data.py` | Regenerates `data/*.js` after syllabus edits |

## Navigation sections

1. Dashboard (progress + status checklist)
2. High-Level Design (HLD)
3. Low-Level Design (LLD)
4. Distributed Systems (HLD topics flagged `distributed`)
5. Concurrency & Multithreading
6. Java Implementation Library
7. SOLID Principles (LLD topics flagged `solid`)
8. Design Patterns (23 GoF + related)
9. Architecture Decision Matrix (`HUB_DECISIONS`)
10. Architecture Diagram Library (`HUB_DIAGRAMS`)
11. System Design Case Studies
12. LLD Coding Exercises (`exercise: true` on java-library topics)
13. Interview Questions
14. One-Day Revision Cheat Sheet (`HUB_ONE_DAY`, print-friendly)

## Regenerate content

```bash
python3 generate_data.py
```

## Portal

Listed on the parent site via `sites.json` as **System Design Revision Hub**.