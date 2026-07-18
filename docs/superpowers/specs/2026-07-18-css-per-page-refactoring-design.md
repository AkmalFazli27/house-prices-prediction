# CSS Per-Page Refactoring — Omah.AI

**Date:** 2026-07-18

## Goal
Split `app/static/css/style.css` (1079 lines) into one shared `base.css` + one CSS file per page, making the stylesheet easier to maintain.

## Architecture

```
app/static/css/
├── base.css     (~250 lines) — reset, :root, body, navbar, .btn-predict, .result-banner, utility classes
├── home.css     (~180 lines) — hero, mode cards, stats, how-it-works
├── simple.css   (~200 lines) — form layout, sidebar, inputs, range slider
└── detail.css   (~250 lines) — banner, sidebar nav, sections, fields, submit bar
```

Each template links exactly two files: `base.css` + its own page CSS.

## File Contents

### base.css
- CSS reset (`*`, `*::before`, `*::after`) — from `style.css:1-7`
- `:root` custom properties — from `style.css:9-36`
- `body` — from `style.css:38-44`
- Navbar (`.navbar`, `.navbar-logo`, `.navbar-links`) — from `style.css:226-287`
- `.btn-predict` (shared between simple and detail) — from `style.css:697-721`
- `.result-banner` / `.error-banner` — from `style.css:750-798`
- New utility classes:
  - `.card` — `background: var(--surface); border: 1px solid var(--outline); border-radius: 8px;`
  - `.flex-center` — `display: flex; align-items: center; gap: 10px;`
  - `.select-arrow` — shared SVG arrow for `<select>` dropdowns
  - `.focus-ring` — shared focus style (`border-color + box-shadow`)

### home.css
- Hero (`.hero`, `.hero-badge`) — from `style.css:46-109`
- Mode cards (`.mode-section`, `.mode-grid`, `.mode-card`) — from `style.css:111-224`
- Stats (`.stats-section`, `.stats-grid`, `.stat-card`) — from `style.css:289-351`
- How it works (`.how-section`, `.how-grid`, `.how-step`) — from `style.css:353-462`

### simple.css
- Simple layout (`.simple-layout`) — from `style.css:464-480`
- Sidebar (`.simple-sidebar`, `.sidebar-card`, `.sidebar-badge`) — from `style.css:482-529, 730-744`
- Form card (`.form-card`) — from `style.css:531-545`
- Form sections (`.form-section`, `.form-section-label`, `.optional-badge`) — from `style.css:547-579`
- Form grid (`.form-grid`, `.form-group-full`) — from `style.css:581-596`
- Form inputs (`.form-group`, `.form-input`, `select.form-input`) — from `style.css:598-641`
- Range slider (`.range-wrapper`, `.form-range`, `.range-value`) — from `style.css:643-689`
- Submit (`.form-submit`, `.form-disclaimer`) — from `style.css:691-728`

### detail.css
- Detail layout (`.detail-layout`) — from `style.css:800-815`
- Detail sidebar (`.detail-sidebar`, `.detail-sidebar-nav`, `.detail-sidebar-item`) — from `style.css:817-892`
- Detail content header (`.detail-content`, `.detail-header`) — from `style.css:894-913`
- Detail sections (`.detail-section`, `.detail-section-header`) — from `style.css:915-943`
- Detail field grid (`.detail-field-grid`, `.detail-field`) — from `style.css:945-997`
- Detail range wrapper (`.detail-range-wrapper`, `.detail-range-value`) — from `style.css:999-1045`
- Detail submit bar (`.detail-submit-bar`) — from `style.css:1047-1079`

### Removed
- `.detail-field-grid-3` (`style.css:951-953`) — unused in any template

### Template Changes
| Template | Old link | New links |
|----------|----------|-----------|
| `index.html` | `style.css` | `base.css` + `home.css` |
| `simple.html` | `style.css` | `base.css` + `simple.css` |
| `detail.html` | `style.css` | `base.css` + `detail.css` |

Also remove the fallback `../static/css/style.css` line from all three templates.

## No Functional Changes
- All class names remain the same
- HTML structure unchanged
- Zero risk of visual regression
