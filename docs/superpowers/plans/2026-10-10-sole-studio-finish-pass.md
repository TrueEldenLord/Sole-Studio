# Sole Studio Finish Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add gender filter, view toggle (cards ↔ sortable table), gender in add form + detail modal, then push to GitHub and update the resume.

**Architecture:** All frontend changes live in a single file (`frontend/index.html`). New HTML sections are inserted into the existing layout; new JS functions extend the existing filter/render pipeline. No new dependencies. Backend (`app.py`) is untouched — gender is already stored.

**Tech Stack:** Vanilla JS, Bootstrap 5.3, Bootstrap Icons, Python/Flask 5050, MongoDB 27017

## Global Constraints

- All frontend code lives in `frontend/index.html` — no separate JS/CSS files
- No new npm packages, CDN scripts, or Python packages
- Flask runs on port 5050 (`const API = "http://localhost:5050"`)
- `gh` CLI at `/opt/homebrew/bin/gh` (system `gh` alias opens browser — do NOT use it)
- MongoDB at `mongodb://localhost:27017/`
- Use `python3` (not `python`)
- `.env` is gitignored — never commit it
- XSS: always wrap user-supplied strings through `escHtml()` before inserting into innerHTML

---

### Task 1: Gender Filter Sidebar

**Files:**
- Modify: `frontend/index.html`

**What this adds:**
- New "Gender" collapsible section in the filter sidebar (inserted above the Brand section)
- CSS for `.gender-pills` / `.gender-pill` / `.gender-pill.active`
- `filters.gender = ""` added to the filters state object (empty string = All)
- `setGender(val, btn)` function
- `applyFilters()` updated to filter by gender
- `renderChips()` updated to show active gender chip
- `removeChip()` updated to handle `'gender'` type
- `clearAllFilters()` updated to reset gender

- [ ] **Step 1: Add `.gender-pills` CSS**

  Inside the `<style>` block, after the `.size-btn.active` rule (around line 101), add:

  ```css
  /* Gender pills */
  .gender-pills { display:flex;flex-wrap:wrap;gap:.35rem; }
  .gender-pill { padding:.28rem .7rem;border-radius:20px;border:1px solid var(--border);background:var(--surface2);color:var(--muted2);font-size:.75rem;font-weight:600;font-family:inherit;cursor:pointer;transition:all .15s; }
  .gender-pill:hover { border-color:var(--accent-light);color:var(--text); }
  .gender-pill.active { background:var(--accent);border-color:var(--accent);color:#fff; }
  ```

- [ ] **Step 2: Add Gender sidebar section to HTML**

  In the `<aside class="filter-sidebar">` block, insert a new `filter-section` div **before** the existing Brand section (before the `<!-- Brand -->` comment):

  ```html
  <!-- Gender -->
  <div class="filter-section">
    <div class="filter-section-header open" onclick="toggleSection(this)">
      Gender <i class="bi bi-chevron-down chevron"></i>
    </div>
    <div class="filter-section-body">
      <div class="gender-pills">
        <button class="gender-pill active" data-gender="" onclick="setGender(this.dataset.gender,this)">All</button>
        <button class="gender-pill" data-gender="Men's" onclick="setGender(this.dataset.gender,this)">Men's</button>
        <button class="gender-pill" data-gender="Women's" onclick="setGender(this.dataset.gender,this)">Women's</button>
        <button class="gender-pill" data-gender="Kids'" onclick="setGender(this.dataset.gender,this)">Kids'</button>
      </div>
    </div>
  </div>
  ```

- [ ] **Step 3: Add `gender` to the filters state object**

  Find:
  ```js
  const filters = { brands: new Set(), sizes: new Set(), minPrice: null, maxPrice: null, search: "" };
  ```
  Replace with:
  ```js
  const filters = { brands: new Set(), sizes: new Set(), minPrice: null, maxPrice: null, search: "", gender: "" };
  ```

- [ ] **Step 4: Add `setGender()` function**

  After the `clearAllFilters()` function, add:

  ```js
  function setGender(val, btn) {
    filters.gender = val;
    document.querySelectorAll('.gender-pill').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    applyFilters();
  }
  ```

- [ ] **Step 5: Update `applyFilters()` to filter by gender**

  Find the line:
  ```js
  if (filters.search)      result = result.filter(i => i.name.toLowerCase().includes(filters.search) || i.brand.toLowerCase().includes(filters.search));
  ```
  Add this line immediately after it:
  ```js
  if (filters.gender)      result = result.filter(i => i.gender === filters.gender);
  ```

- [ ] **Step 6: Update `renderChips()` to show gender chip**

  In `renderChips()`, after the `maxPrice` chip line, add:
  ```js
  if (filters.gender) chips.push(`<span class="filter-chip">${escHtml(filters.gender)}<button onclick="removeChip('gender')">✕</button></span>`);
  ```

- [ ] **Step 7: Update `removeChip()` to handle gender**

  In `removeChip()`, after the `maxPrice` branch, add:
  ```js
  else if (type === 'gender') {
    filters.gender = '';
    document.querySelectorAll('.gender-pill').forEach(p => p.classList.toggle('active', p.dataset.gender === ''));
  }
  ```

- [ ] **Step 8: Update `clearAllFilters()` to reset gender**

  In `clearAllFilters()`, after the `searchInput` value reset line, add:
  ```js
  filters.gender = '';
  document.querySelectorAll('.gender-pill').forEach(p => p.classList.toggle('active', p.dataset.gender === ''));
  ```

- [ ] **Step 9: Verify in browser**

  Start Flask + MongoDB if not running:
  ```bash
  mkdir -p /tmp/mongodata && mongod --dbpath /tmp/mongodata --fork --logpath /tmp/mongod.log
  cd "/Users/Alex/Documents/Resume Projects/shoe-store/backend" && python3 app.py
  ```
  Open `frontend/index.html` in browser. Check:
  - Sidebar shows "Gender" section above Brand with 4 pill buttons
  - Clicking "Men's" filters cards to only Men's items; chip "Men's" appears
  - Clicking the ✕ on the chip resets to All
  - "Clear all" resets gender pills back to "All" active

---

### Task 2: Gender in Add Form + Detail Modal

**Files:**
- Modify: `frontend/index.html`

**What this adds:**
- Gender `<select>` field in the add form
- `gender` field included in POST body
- Gender spec row in the product detail modal
- `openProduct()` populates the gender row

- [ ] **Step 1: Add Gender field to the add form**

  In the `<form id="addForm">` form grid, after the Quantity field div, add:

  ```html
  <div><label class="form-label-sm">Gender</label>
    <select class="form-field" id="fgender" required>
      <option value="">Select…</option>
      <option value="Men's">Men's</option>
      <option value="Women's">Women's</option>
      <option value="Kids'">Kids'</option>
    </select>
  </div>
  ```

- [ ] **Step 2: Include gender in the POST body**

  In the `addForm` submit handler, find:
  ```js
  quantity: parseInt(document.getElementById("fqty").value),
  ```
  Add a comma and the gender field after it:
  ```js
  quantity: parseInt(document.getElementById("fqty").value),
  gender:   document.getElementById("fgender").value,
  ```

- [ ] **Step 3: Add Gender row to the detail modal**

  In `#productModal`, find the Color spec row:
  ```html
  <div class="detail-spec-row"><span class="detail-spec-label">Color</span><span class="detail-spec-val" id="detailColor"></span></div>
  ```
  Add immediately after it:
  ```html
  <div class="detail-spec-row"><span class="detail-spec-label">Gender</span><span class="detail-spec-val" id="detailGender"></span></div>
  ```

- [ ] **Step 4: Populate gender in `openProduct()`**

  In `openProduct()`, after the line that sets `detailColor`, add:
  ```js
  document.getElementById("detailGender").textContent = item.gender || "—";
  ```

- [ ] **Step 5: Verify in browser**

  - Click "Add Shoe" — confirm Gender dropdown appears in the form
  - Add a test shoe with gender "Women's" — confirm it appears in the card grid
  - Click the card — confirm the detail modal shows a Gender row with "Women's"
  - Delete the test shoe when done

---

### Task 3: View Toggle — Buttons, CSS, Container

**Files:**
- Modify: `frontend/index.html`

**What this adds:**
- `.view-toggle` / `.view-btn` CSS
- `.inv-table` table CSS (styling only — no renderTable yet)
- Two icon buttons in the toolbar (grid / table)
- `#productTable` empty container div below `#productGrid`
- `viewMode` state variable
- `setView(mode)` function
- `applyFilters()` updated to route to card or table render

- [ ] **Step 1: Add view toggle and table CSS**

  In the `<style>` block, after the `.empty-state` rules, add:

  ```css
  /* ══ VIEW TOGGLE ══ */
  .view-toggle { display:flex;border:1px solid var(--border);border-radius:8px;overflow:hidden; }
  .view-btn { width:34px;height:34px;background:var(--surface);border:none;color:var(--muted2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:.9rem;transition:all .15s; }
  .view-btn:hover { color:var(--text);background:var(--surface2); }
  .view-btn.active { background:rgba(124,58,237,.2);color:var(--accent-light); }

  /* ══ INVENTORY TABLE ══ */
  .inv-table { border-collapse:collapse;width:100%; }
  .inv-table th { background:var(--surface2);color:var(--muted2);font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.07em;padding:.65rem .9rem;border-bottom:1px solid var(--border);cursor:pointer;user-select:none;white-space:nowrap; }
  .inv-table th:hover { color:var(--text); }
  .inv-table td { padding:.6rem .9rem;border-bottom:1px solid var(--border);font-size:.85rem;vertical-align:middle; }
  .inv-table tbody tr:hover td { background:var(--surface2);cursor:pointer; }
  .sort-arrow { font-size:.7rem;margin-left:.25rem;color:var(--accent-light); }
  ```

- [ ] **Step 2: Add view toggle buttons to the toolbar**

  In `.product-toolbar`, find the `.toolbar-right` div:
  ```html
  <div class="toolbar-right">
  ```
  Add the toggle group as the first child inside `.toolbar-right` (before the search wrap):
  ```html
  <div class="view-toggle">
    <button class="view-btn active" id="viewCardBtn" onclick="setView('card')" title="Card view"><i class="bi bi-grid-3x3-gap-fill"></i></button>
    <button class="view-btn" id="viewTableBtn" onclick="setView('table')" title="Table view"><i class="bi bi-table"></i></button>
  </div>
  ```

- [ ] **Step 3: Add `#productTable` container below `#productGrid`**

  After `<div class="product-grid" id="productGrid"></div>`, add:
  ```html
  <div id="productTable" style="display:none;overflow-x:auto;"></div>
  ```

- [ ] **Step 4: Add `viewMode` state and `setView()` function**

  After the `const filters = ...` line, add:
  ```js
  let viewMode = 'card';
  let sortCol  = null;
  let sortDir  = 'asc';
  ```

  After the `clearAllFilters()` function, add:
  ```js
  function setView(mode) {
    viewMode = mode;
    document.getElementById('viewCardBtn').classList.toggle('active', mode === 'card');
    document.getElementById('viewTableBtn').classList.toggle('active', mode === 'table');
    document.getElementById('productGrid').style.display  = mode === 'card'  ? '' : 'none';
    document.getElementById('productTable').style.display = mode === 'table' ? '' : 'none';
    applyFilters();
  }
  ```

- [ ] **Step 5: Update `applyFilters()` to route by viewMode**

  In `applyFilters()`, replace:
  ```js
  renderCards(result);
  renderChips();
  ```
  With:
  ```js
  if (viewMode === 'table') renderTable(result);
  else renderCards(result);
  renderChips();
  ```

- [ ] **Step 6: Verify toggle buttons render**

  Reload the browser. Confirm two icon buttons appear in the toolbar (grid + table icons). Card view button should be highlighted purple. Clicking the table button should highlight it and hide the card grid — the table container will be empty for now (renderTable not yet written). That's expected.

---

### Task 4: `renderTable()` + `sortTable()`

**Files:**
- Modify: `frontend/index.html`

**What this adds:**
- `renderTable(items)` — renders a styled `<table>` inside `#productTable` with sort arrows
- `sortTable(col)` — toggles sort column/direction and calls `applyFilters()`
- Table rows: clickable (opens detail modal), stock cell opens edit qty modal, delete button

- [ ] **Step 1: Add `sortTable()` function**

  After the `setView()` function, add:
  ```js
  function sortTable(col) {
    if (sortCol === col) sortDir = sortDir === 'asc' ? 'desc' : 'asc';
    else { sortCol = col; sortDir = 'asc'; }
    applyFilters();
  }
  ```

- [ ] **Step 2: Add `renderTable()` function**

  After `sortTable()`, add the full `renderTable()` function:

  ```js
  function renderTable(items) {
    const container = document.getElementById("productTable");
    document.getElementById("resultCount").textContent = items.length;
    if (!items.length) {
      container.innerHTML = `<div class="empty-state"><i class="bi bi-bag-x"></i><p>No items match your filters.</p></div>`;
      return;
    }

    const cols = ['brand','name','gender','size','color','price','quantity'];
    const labels = { brand:'Brand', name:'Name', gender:'Gender', size:'Size', color:'Color', price:'Price', quantity:'Stock' };

    let sorted = [...items];
    if (sortCol) {
      sorted.sort((a, b) => {
        let av = a[sortCol], bv = b[sortCol];
        if (typeof av === 'string') av = av.toLowerCase();
        if (typeof bv === 'string') bv = bv.toLowerCase();
        if (av < bv) return sortDir === 'asc' ? -1 : 1;
        if (av > bv) return sortDir === 'asc' ?  1 : -1;
        return 0;
      });
    }

    const thead = cols.map(col => {
      const arrow = sortCol === col ? (sortDir === 'asc' ? ' ↑' : ' ↓') : '';
      return `<th onclick="sortTable('${col}')">${labels[col]}<span class="sort-arrow">${arrow}</span></th>`;
    }).join('') + '<th>Actions</th>';

    const tbody = sorted.map(item => `
      <tr onclick="openProduct('${item._id}')">
        <td><span class="product-brand">${escHtml(item.brand)}</span></td>
        <td style="font-weight:600">${escHtml(item.name)}</td>
        <td style="color:var(--muted2)">${escHtml(item.gender || '—')}</td>
        <td>${item.size}</td>
        <td style="color:var(--muted2)">${escHtml(item.color)}</td>
        <td style="color:var(--accent-light);font-weight:700">$${parseFloat(item.price).toFixed(2)}</td>
        <td onclick="event.stopPropagation();openEdit('${item._id}',${item.quantity})">${qtyBadge(item.quantity)}</td>
        <td onclick="event.stopPropagation()">
          <button class="btn-del" style="width:auto;padding:.3rem .6rem" onclick="deleteItem('${item._id}')">
            <i class="bi bi-trash3-fill"></i>
          </button>
        </td>
      </tr>`).join('');

    container.innerHTML = `
      <table class="inv-table">
        <thead><tr>${thead}</tr></thead>
        <tbody>${tbody}</tbody>
      </table>`;
  }
  ```

- [ ] **Step 3: Verify table view in browser**

  Reload. Click the table icon button. Confirm:
  - Table appears with all 35 seeded items
  - All 8 columns visible: Brand, Name, Gender, Size, Color, Price, Stock, Actions
  - Clicking "Brand" header sorts A→Z, clicking again sorts Z→A (arrow indicator updates)
  - Clicking "Price" header sorts numeric correctly
  - Clicking a row opens the detail modal
  - Clicking the Stock cell opens the edit qty modal
  - Clicking the trash button deletes the item (reload inventory after confirming)
  - Switching back to card view works; gender filter works in both views

---

### Task 5: GitHub — Init, Commit, Push

**Files:**
- Create: `shoe-store/.git/` (via `git init`)
- No code changes

- [ ] **Step 1: Initialize git repo**

  ```bash
  cd "/Users/Alex/Documents/Resume Projects/shoe-store"
  git init
  git branch -M main
  ```
  Expected: `Initialized empty Git repository in .../shoe-store/.git/`

- [ ] **Step 2: Verify .gitignore is correct**

  ```bash
  cat "/Users/Alex/Documents/Resume Projects/shoe-store/.gitignore"
  ```
  Confirm `.env` is listed. If missing, add it:
  ```bash
  echo ".env" >> "/Users/Alex/Documents/Resume Projects/shoe-store/.gitignore"
  ```

- [ ] **Step 3: Stage and commit all files**

  ```bash
  cd "/Users/Alex/Documents/Resume Projects/shoe-store"
  git add .
  git status
  ```
  Confirm `backend/.env` does NOT appear in staged files. Then commit:
  ```bash
  git commit -m "feat: Sole Studio inventory management system

  Full-stack shoe store inventory app built with Python/Flask, MongoDB,
  and vanilla JS + Bootstrap 5. Features: product card grid, sortable
  data table view toggle, gender/brand/size/price filter sidebar,
  Pixabay auto-image fetch, product detail modal, stats dashboard.
  35 seed items across 10 brands."
  ```

- [ ] **Step 4: Create GitHub repo and push**

  ```bash
  /opt/homebrew/bin/gh repo create TrueEldenLord/Sole-Studio \
    --public \
    --description "Full-stack shoe store inventory management — Flask, MongoDB, Bootstrap 5" \
    --source="/Users/Alex/Documents/Resume Projects/shoe-store" \
    --remote=origin \
    --push
  ```
  Expected: repo created and code pushed to `main`.

- [ ] **Step 5: Confirm repo is live**

  ```bash
  /opt/homebrew/bin/gh repo view TrueEldenLord/Sole-Studio
  ```
  Confirm repo URL, description, and that files are present.

---

### Task 6: Resume Update

**Files:**
- Modify: `/Users/Alex/Documents/Resumes/Resume_Alexis_Sanchez.tex`

**What this updates:**
- Replace the existing 2-bullet Shoe Store entry (lines 77–82) with a 3-bullet entry that reflects the completed feature set and GitHub repo

- [ ] **Step 1: Replace the Shoe Store project entry**

  Find the existing entry (lines 77–82):
  ```latex
  \noindent\textbf{SHOE STORE MANAGEMENT SYSTEM \textbar\ PYTHON \& JS}
  \hfill Fall 2024
  \begin{itemize}
    \item Created a system that stores the inventory of a business allowing the owner to add, remove and change the inventory quantity all stored in an external DB using MongoDB.
    \item Built the UI using the Bootstrap framework, integrated with a MongoDB backend.
  \end{itemize}
  ```

  Replace with:
  ```latex
  \noindent\textbf{SOLE STUDIO — SHOE STORE MANAGEMENT SYSTEM \textbar\ PYTHON, JS}
  \hfill Fall 2026
  \begin{itemize}
    \item Built a full-stack inventory management app with a Python/Flask REST API (GET/POST/PUT/DELETE), MongoDB backend, and a responsive Bootstrap 5 frontend featuring a dual-view UI (card grid and sortable data table).
    \item Integrated the Pixabay API to auto-fetch product images on item creation, with multi-pass brand-tag validation to ensure image accuracy across 10 shoe brands.
    \item Implemented a dynamic filter sidebar (gender, brand, size, price range) with active filter chips, real-time search, and low-stock alerting; deployed source to GitHub.
  \end{itemize}
  ```

- [ ] **Step 2: Verify the .tex file compiles (optional but recommended)**

  If `pdflatex` is available:
  ```bash
  cd /Users/Alex/Documents/Resumes
  pdflatex Resume_Alexis_Sanchez.tex
  ```
  Expected: `Resume_Alexis_Sanchez.pdf` generated with no errors. Open to confirm the Sole Studio entry looks correct.

  If `pdflatex` is not installed, skip — the `.tex` source edit is sufficient.
