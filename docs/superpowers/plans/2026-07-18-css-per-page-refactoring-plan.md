# CSS Per-Page Refactoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split `app/static/css/style.css` (1079 lines) into `base.css` + one CSS file per page.

**Architecture:** One shared `base.css` (reset, vars, navbar, shared components, utilities) + `home.css` (homepage), `simple.css` (Quick Mode), `detail.css` (Detailed Mode). Each template links `base.css` + its own page CSS.

**Tech Stack:** Vanilla CSS (no preprocessor), Jinja2 templating

---

## File Structure

```
app/static/css/
├── base.css      ← NEW (shared: reset, :root, body, navbar, .btn-predict, .result-banner, .error-banner, utility classes)
├── home.css      ← NEW (homepage: hero, mode cards, stats, how-it-works)
├── simple.css    ← NEW (Quick Mode: form layout, sidebar, inputs, range slider)
├── detail.css    ← NEW (Detailed Mode: layout, sidebar nav, sections, fields, submit bar)
└── style.css     ← DELETED (old monolithic file)

app/templates/
├── index.html    ← MODIFY (CSS links)
├── simple.html   ← MODIFY (CSS links)
└── detail.html   ← MODIFY (CSS links)
```

---

### Task 1: Create `base.css`

**Files:**
- Create: `app/static/css/base.css`

- [ ] **Step 1: Write base.css**

Copy these sections from `style.css`, keeping them exactly as-is:

```css
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #0F172A;
  --on-primary: #FFFFFF;
  --secondary: #0D9488;
  --on-secondary: #FFFFFF;
  --surface: #FFFFFF;
  --surface-container: #F8FAFC;
  --surface-container-low: #F1F5F9;
  --on-surface: #1E293B;
  --on-surface-variant: #64748B;
  --outline: #E2E8F0;
  --outline-variant: #CBD5E1;

  --font-display: 'Hanken Grotesk', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-label: 'JetBrains Mono', monospace;

  --gutter: 24px;
  --stack-sm: 12px;
  --stack-md: 24px;
  --stack-lg: 40px;
  --margin-desktop: 48px;
  --margin-mobile: 16px;
  --container-max: 1280px;

  --error: #ba1a1a;
}

body {
  font-family: var(--font-body);
  color: var(--on-surface);
  background: var(--surface);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* Navbar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: var(--surface);
  border-bottom: 1px solid var(--outline);
  height: 64px;
}

.navbar .container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--margin-desktop);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-logo {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: var(--stack-md);
  list-style: none;
}

.navbar-links a {
  font-family: var(--font-label);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  text-decoration: none;
  color: var(--on-surface-variant);
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
}

.navbar-links a:hover {
  color: var(--secondary);
}

.navbar-links a.active {
  color: var(--secondary);
  border-bottom-color: var(--secondary);
}

@media (max-width: 768px) {
  .navbar .container {
    padding: 0 var(--margin-mobile);
  }
}

/* Shared utility classes */

.card {
  background: var(--surface);
  border: 1px solid var(--outline);
  border-radius: 8px;
}

.flex-center {
  display: flex;
  align-items: center;
  gap: 10px;
}

.select-arrow {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
  cursor: pointer;
}

/* Predict button (shared between simple and detail) */
.btn-predict {
  width: 100%;
  padding: 14px 24px;
  border: none;
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  background: var(--primary);
  color: var(--on-primary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.2s;
}

.btn-predict:hover {
  background: var(--secondary);
}

.btn-predict .material-symbols-outlined {
  font-size: 20px;
}

/* Result / Error banners (shared between simple and detail) */
.result-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(13, 148, 136, 0.08);
  border: 1px solid var(--secondary);
  border-radius: 8px;
  padding: var(--stack-md);
  margin-bottom: var(--stack-md);
}

.result-banner .material-symbols-outlined {
  font-size: 28px;
  color: var(--secondary);
}

.result-banner strong {
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--on-surface);
}

.result-value {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--secondary);
  margin-left: 8px;
}

.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(186, 26, 26, 0.08);
  border: 1px solid var(--error);
  border-radius: 8px;
  padding: var(--stack-md);
  margin-bottom: var(--stack-md);
  color: var(--error);
}

.error-banner .material-symbols-outlined {
  font-size: 24px;
}

.error-banner span:last-child {
  font-size: 0.875rem;
}
```

- [ ] **Step 2: Verify**

```bash
Get-ChildItem -LiteralPath "app/static/css/base.css"
```

Expected: File exists, readable.

- [ ] **Step 3: Commit**

```bash
git add app/static/css/base.css
git commit -m "refactor(css): create base.css with shared styles (reset, vars, navbar, utilities)"
```

---

### Task 2: Create `home.css`

**Files:**
- Create: `app/static/css/home.css`

- [ ] **Step 1: Write home.css**

Copy these sections from `style.css`:

```css
/* Hero Section */
.hero {
  padding: 60px 0 40px;
  text-align: center;
}

.hero .container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--margin-desktop);
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 16px;
  border-radius: 999px;
  background: rgba(13, 148, 136, 0.08);
  color: var(--secondary);
  border: 1px solid rgba(13, 148, 136, 0.15);
  font-family: var(--font-label);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: var(--stack-md);
}

.hero h1 {
  font-family: var(--font-display);
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: var(--on-surface);
  max-width: 900px;
  margin: 0 auto var(--stack-md);
}

.hero p {
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--on-surface-variant);
  max-width: 600px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .hero {
    padding: 40px 0 24px;
  }

  .hero .container {
    padding: 0 var(--margin-mobile);
  }

  .hero h1 {
    font-size: 2rem;
  }

  .hero p {
    font-size: 1rem;
  }
}

/* Mode Cards */
.mode-section {
  padding-bottom: 80px;
}

.mode-section .container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--margin-desktop);
}

.mode-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--gutter);
  max-width: 900px;
  margin: 0 auto;
}

.mode-card {
  background: var(--surface);
  border: 1px solid var(--outline);
  border-radius: 8px;
  padding: var(--stack-lg);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  transition: transform 0.3s, border-color 0.3s;
}

.mode-card:hover {
  transform: translateY(-4px);
  border-color: var(--secondary);
}

.mode-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: var(--surface-container);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--stack-md);
  color: var(--secondary);
  transition: background 0.3s, color 0.3s;
}

.mode-card:hover .mode-card-icon {
  background: var(--secondary);
  color: var(--on-secondary);
}

.mode-card-icon .material-symbols-outlined {
  font-size: 24px;
}

.mode-card h2 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: var(--stack-sm);
  color: var(--on-surface);
}

.mode-card p {
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--on-surface-variant);
  margin-bottom: var(--stack-md);
  flex: 1;
}

.mode-card .btn {
  width: 100%;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  background: var(--primary);
  color: var(--on-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.2s;
  text-decoration: none;
}

.mode-card .btn:hover {
  background: var(--secondary);
}

.mode-card .btn .material-symbols-outlined {
  font-size: 20px;
}

@media (max-width: 768px) {
  .mode-grid {
    grid-template-columns: 1fr;
  }

  .mode-section .container {
    padding: 0 var(--margin-mobile);
  }

  .mode-card {
    padding: var(--stack-md);
  }
}

/* Stats Bar */
.stats-section {
  background: var(--surface-container-low);
  padding: var(--stack-lg) 0;
}

.stats-section .container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--margin-desktop);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--gutter);
  max-width: 900px;
  margin: 0 auto;
}

.stat-card {
  text-align: center;
  padding: var(--stack-md);
}

.stat-card-icon {
  font-size: 2rem;
  color: var(--secondary);
  margin-bottom: var(--stack-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-card .stat-value {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--on-surface);
  display: block;
}

.stat-card .stat-label {
  font-family: var(--font-label);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--on-surface-variant);
  margin-top: 4px;
  display: block;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: var(--stack-md);
  }

  .stats-section .container {
    padding: 0 var(--margin-mobile);
  }
}

/* How It Works */
.how-section {
  padding: var(--stack-lg) 0;
  background: var(--surface);
}

.how-section .container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--margin-desktop);
}

.how-section h2 {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: var(--stack-lg);
  color: var(--on-surface);
}

.how-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--gutter);
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
}

.how-grid::before {
  content: '';
  position: absolute;
  top: 28px;
  left: calc(12.5% + 24px);
  right: calc(12.5% + 24px);
  height: 2px;
  background: var(--outline);
  z-index: 0;
}

.how-step {
  text-align: center;
  position: relative;
  z-index: 1;
}

.how-step-number {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary);
  color: var(--on-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--stack-md);
  font-family: var(--font-label);
  font-size: 1rem;
  font-weight: 600;
  border: 4px solid var(--surface);
}

.how-step-icon {
  font-size: 1.5rem;
  color: var(--secondary);
  margin-bottom: var(--stack-sm);
  display: block;
}

.how-step h3 {
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--on-surface);
}

.how-step p {
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--on-surface-variant);
  max-width: 220px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .how-grid {
    grid-template-columns: 1fr 1fr;
    gap: var(--stack-lg);
  }

  .how-grid::before {
    display: none;
  }

  .how-section .container {
    padding: 0 var(--margin-mobile);
  }

  .how-step p {
    max-width: none;
  }
}

@media (max-width: 480px) {
  .how-grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 2: Verify**

```bash
Get-ChildItem -LiteralPath "app/static/css/home.css"
```

Expected: File exists.

- [ ] **Step 3: Commit**

```bash
git add app/static/css/home.css
git commit -m "refactor(css): create home.css with homepage styles (hero, cards, stats, how-it-works)"
```

---

### Task 3: Create `simple.css`

**Files:**
- Create: `app/static/css/simple.css`

- [ ] **Step 1: Write simple.css**

```css
/* Simple Mode Form Layout */
.simple-layout {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: var(--stack-lg) var(--margin-desktop);
  display: grid;
  grid-template-columns: 4fr 8fr;
  gap: var(--gutter);
  align-items: start;
}

@media (max-width: 900px) {
  .simple-layout {
    grid-template-columns: 1fr;
    padding: var(--stack-md) var(--margin-mobile);
  }
}

/* Sidebar */
.simple-sidebar {
  position: sticky;
  top: calc(64px + var(--stack-lg));
}

@media (max-width: 900px) {
  .simple-sidebar {
    position: static;
  }
}

.sidebar-card {
  background: var(--surface-container-low);
  border: 1px solid var(--outline);
  border-radius: 8px;
  padding: var(--stack-md);
}

.sidebar-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: var(--secondary);
  color: var(--on-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--stack-sm);
}

.sidebar-icon .material-symbols-outlined {
  font-size: 24px;
}

.sidebar-card h2 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: var(--stack-sm);
  color: var(--on-surface);
}

.sidebar-card p {
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--on-surface-variant);
}

/* Sidebar Badge */
.sidebar-badge {
  display: inline-block;
  font-family: var(--font-label);
  font-size: 0.65rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--secondary);
  background: rgba(13, 148, 136, 0.08);
  border: 1px solid rgba(13, 148, 136, 0.15);
  padding: 2px 10px;
  border-radius: 999px;
  margin-bottom: var(--stack-sm);
}

/* Form Card */
.form-card {
  background: var(--surface);
  border: 1px solid var(--outline);
  border-radius: 8px;
  padding: var(--stack-lg);
}

.form-card h1 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: var(--stack-md);
  color: var(--on-surface);
}

/* Form Sections */
.form-section {
  margin-bottom: var(--stack-md);
  padding-bottom: var(--stack-md);
  border-bottom: 1px solid var(--outline);
}

.form-section:last-of-type {
  border-bottom: none;
}

.form-section-label {
  display: block;
  font-family: var(--font-label);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--on-surface-variant);
  margin-bottom: var(--stack-sm);
}

.optional-badge {
  font-family: var(--font-label);
  font-size: 0.65rem;
  color: var(--on-surface-variant);
  background: var(--surface-container);
  padding: 2px 8px;
  border-radius: 4px;
  text-transform: lowercase;
  letter-spacing: normal;
  margin-left: 6px;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--stack-sm);
}

.form-group-full {
  grid-column: 1 / -1;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

/* Form Inputs */
.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--on-surface);
  margin-bottom: 4px;
}

.form-input {
  height: 44px;
  padding: 0 12px;
  border: 1px solid var(--outline);
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: 0.875rem;
  color: var(--on-surface);
  background: var(--surface-container-low);
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
  width: 100%;
}

.form-input:focus {
  border-color: var(--secondary);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.form-input::placeholder {
  color: var(--outline-variant);
}

select.form-input {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
  cursor: pointer;
}

/* Range Slider */
.range-wrapper {
  display: flex;
  align-items: center;
  gap: var(--stack-sm);
}

.form-range {
  flex: 1;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: var(--outline);
  border-radius: 3px;
  outline: none;
  cursor: pointer;
}

.form-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--secondary);
  cursor: pointer;
  border: 2px solid var(--surface);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

.form-range::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--secondary);
  cursor: pointer;
  border: 2px solid var(--surface);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

.range-value {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--secondary);
  min-width: 24px;
  text-align: center;
}

/* Submit */
.form-submit {
  margin-top: var(--stack-md);
  text-align: center;
}

.form-disclaimer {
  font-size: 0.75rem;
  font-style: italic;
  color: var(--on-surface-variant);
  margin-top: var(--stack-sm);
}
```

- [ ] **Step 2: Verify**

```bash
Get-ChildItem -LiteralPath "app/static/css/simple.css"
```

Expected: File exists.

- [ ] **Step 3: Commit**

```bash
git add app/static/css/simple.css
git commit -m "refactor(css): create simple.css with Quick Mode form styles"
```

---

### Task 4: Create `detail.css`

**Files:**
- Create: `app/static/css/detail.css`

- [ ] **Step 1: Write detail.css**

```css
/* Detail Layout */
.detail-layout {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: var(--stack-lg) var(--margin-desktop);
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: var(--gutter);
  align-items: start;
}

@media (max-width: 900px) {
  .detail-layout {
    grid-template-columns: 1fr;
    padding: var(--stack-md) var(--margin-mobile);
  }
}

/* Detail Sidebar */
.detail-sidebar {
  position: sticky;
  top: calc(64px + var(--stack-lg));
  max-height: calc(100vh - 64px - var(--stack-lg) * 2);
  overflow-y: auto;
}

.detail-sidebar::-webkit-scrollbar {
  width: 4px;
}

.detail-sidebar::-webkit-scrollbar-thumb {
  background: var(--outline-variant);
  border-radius: 2px;
}

@media (max-width: 900px) {
  .detail-sidebar {
    position: static;
    max-height: none;
    overflow-y: visible;
  }
}

.detail-sidebar-nav {
  background: var(--surface);
  border: 1px solid var(--outline);
  border-radius: 8px;
  padding: var(--stack-sm);
}

.detail-sidebar-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--on-surface-variant);
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
  cursor: pointer;
  border: none;
  width: 100%;
  text-align: left;
  font-family: var(--font-body);
}

.detail-sidebar-item:hover {
  background: var(--surface-container);
}

.detail-sidebar-item.active {
  background: var(--secondary);
  color: var(--on-secondary);
}

.detail-sidebar-item .material-symbols-outlined {
  font-size: 18px;
}

.detail-sidebar-item .badge {
  margin-left: auto;
  font-family: var(--font-label);
  font-size: 0.65rem;
  background: var(--surface-container);
  padding: 1px 6px;
  border-radius: 4px;
  color: var(--on-surface-variant);
}

.detail-sidebar-item.active .badge {
  background: rgba(255,255,255,0.2);
  color: var(--on-secondary);
}

/* Detail Content */
.detail-content {
  min-width: 0;
}

.detail-header {
  margin-bottom: var(--stack-md);
}

.detail-header h1 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--on-surface);
}

.detail-header p {
  font-size: 0.875rem;
  color: var(--on-surface-variant);
}

/* Detail Sections */
.detail-section {
  background: var(--surface);
  border: 1px solid var(--outline);
  border-radius: 8px;
  padding: var(--stack-md);
  margin-bottom: var(--gutter);
  scroll-margin-top: calc(64px + var(--stack-md));
}

.detail-section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: var(--stack-md);
  padding-bottom: var(--stack-sm);
  border-bottom: 1px solid var(--outline);
}

.detail-section-header .material-symbols-outlined {
  font-size: 22px;
  color: var(--secondary);
}

.detail-section-header h2 {
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--on-surface);
}

.detail-field-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--stack-sm);
}

/* Detail Fields */
.detail-field {
  display: flex;
  flex-direction: column;
}

.detail-field label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--on-surface-variant);
  margin-bottom: 3px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.detail-field input,
.detail-field select {
  height: 40px;
  padding: 0 10px;
  border: 1px solid var(--outline);
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: var(--on-surface);
  background: var(--surface-container-low);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  width: 100%;
}

.detail-field input:focus,
.detail-field select:focus {
  border-color: var(--secondary);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.detail-field select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 30px;
  cursor: pointer;
}

/* Detail Range Wrapper */
.detail-range-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-range-wrapper input[type="range"] {
  flex: 1;
  height: 5px;
  -webkit-appearance: none;
  appearance: none;
  background: var(--outline);
  border-radius: 3px;
  outline: none;
  cursor: pointer;
  padding: 0;
}

.detail-range-wrapper input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--secondary);
  cursor: pointer;
  border: 2px solid var(--surface);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

.detail-range-wrapper input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--secondary);
  cursor: pointer;
  border: 2px solid var(--surface);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

.detail-range-value {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 600;
  color: var(--secondary);
  min-width: 20px;
  text-align: center;
}

/* Detail Submit Bar */
.detail-submit-bar {
  position: sticky;
  bottom: 16px;
  z-index: 40;
  background: var(--surface);
  border: 1px solid var(--outline);
  border-radius: 8px;
  padding: var(--stack-sm) var(--stack-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  margin-top: var(--stack-md);
}

.detail-submit-bar .btn-predict {
  width: auto;
  padding: 12px 32px;
}

@media (max-width: 600px) {
  .detail-field-grid {
    grid-template-columns: 1fr;
  }

  .detail-submit-bar {
    flex-direction: column;
    gap: var(--stack-sm);
    text-align: center;
  }

  .detail-submit-bar .btn-predict {
    width: 100%;
  }
}
```

- [ ] **Step 2: Verify**

```bash
Get-ChildItem -LiteralPath "app/static/css/detail.css"
```

Expected: File exists.

- [ ] **Step 3: Commit**

```bash
git add app/static/css/detail.css
git commit -m "refactor(css): create detail.css with Detailed Mode form styles"
```

---

### Task 5: Update template CSS links

**Files:**
- Modify: `app/templates/index.html`
- Modify: `app/templates/simple.html`
- Modify: `app/templates/detail.html`

- [ ] **Step 1: Update `index.html`** — replace `style.css` links with `base.css` + `home.css`

In `app/templates/index.html`:

Old:
```html
  <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
  <link rel="stylesheet" href="../static/css/style.css">
```

New:
```html
  <link rel="stylesheet" href="{{ url_for('static', path='/css/base.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', path='/css/home.css') }}">
```

- [ ] **Step 2: Commit index.html**

```bash
git add app/templates/index.html
git commit -m "refactor(templates): update index.html to link base.css + home.css"
```

- [ ] **Step 3: Update `simple.html`** — replace with `base.css` + `simple.css`

In `app/templates/index.html`:

Old:
```html
  <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
  <link rel="stylesheet" href="../static/css/style.css">
```

New:
```html
  <link rel="stylesheet" href="{{ url_for('static', path='/css/base.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', path='/css/home.css') }}">
```

- [ ] **Step 4: Update `simple.html`** — replace with `base.css` + `simple.css`

In `app/templates/simple.html`:

Old:
```html
  <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
  <link rel="stylesheet" href="../static/css/style.css">
```

New:
```html
  <link rel="stylesheet" href="{{ url_for('static', path='/css/base.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', path='/css/simple.css') }}">
```

- [ ] **Step 5: Commit simple.html**

```bash
git add app/templates/simple.html
git commit -m "refactor(templates): update simple.html to link base.css + simple.css"
```

- [ ] **Step 6: Update `detail.html`** — replace with `base.css` + `detail.css`

In `app/templates/detail.html`:

Old:
```html
  <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
  <link rel="stylesheet" href="../static/css/style.css">
```

New:
```html
  <link rel="stylesheet" href="{{ url_for('static', path='/css/base.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', path='/css/detail.css') }}">
```

- [ ] **Step 7: Commit detail.html**

```bash
git add app/templates/detail.html
git commit -m "refactor(templates): update detail.html to link base.css + detail.css"
```

---

### Task 6: Delete old `style.css`

**Files:**
- Delete: `app/static/css/style.css`

- [ ] **Step 1: Remove old file**

```bash
Remove-Item -LiteralPath "app/static/css/style.css"
```

- [ ] **Step 2: Verify deletion**

```bash
Test-Path -LiteralPath "app/static/css/style.css"
```

Expected: `False`

- [ ] **Step 3: Commit deletion**

```bash
git rm app/static/css/style.css
git commit -m "refactor(css): remove monolithic style.css (split into per-page files)"
```

---

### Task 7: Verify

- [ ] **Step 1: Restart server and check all pages**

Kill any running uvicorn, then:

```bash
& "D:\Ameng\Data Science Project\house-prices-prediction\api-env\Scripts\uvicorn.exe" app.main:app --reload
```

Wait for it to start, then in another terminal:

```bash
Invoke-WebRequest -Uri http://localhost:8000 -UseBasicParsing | Select-Object StatusCode
Invoke-WebRequest -Uri http://localhost:8000/simple -UseBasicParsing | Select-Object StatusCode
Invoke-WebRequest -Uri http://localhost:8000/detail -UseBasicParsing | Select-Object StatusCode
Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing | Select-Object StatusCode
```

Expected: All return `200`.

- [ ] **Step 2: Check CSS content loads**

```bash
$base = Invoke-WebRequest -Uri http://localhost:8000 -UseBasicParsing
$base.RawContent -match "base\.css|home\.css"
$simple = Invoke-WebRequest -Uri http://localhost:8000/simple -UseBasicParsing
$simple.RawContent -match "base\.css|simple\.css"
$detail = Invoke-WebRequest -Uri http://localhost:8000/detail -UseBasicParsing
$detail.RawContent -match "base\.css|detail\.css"
```

Expected: Each page matches its own two CSS files.

---

## Self-Review Checklist

1. **Spec coverage:** Every section from the spec has a corresponding task — `base.css` (Task 1), `home.css` (Task 2), `simple.css` (Task 3), `detail.css` (Task 4), template updates (Task 5), delete old file (Task 6), verify (Task 7). No gaps.

2. **Placeholder scan:** All code blocks contain actual CSS content. No TBD, TODO, or vague steps.

3. **Type consistency:** All class names match between CSS files and templates. Template links use `url_for('static', path='/css/...')` consistently.

4. **Edge cases:** Verify step restarts server to avoid stale cache. All three pages checked independently.
