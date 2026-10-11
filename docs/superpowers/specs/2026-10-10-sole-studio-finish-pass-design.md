# Sole Studio — Finish Pass Design

**Date:** 2026-10-10
**Project:** Sole Studio Inventory Management (Flask + MongoDB)

---

## Overview

Complete the remaining features of the Sole Studio shoe inventory app, push to GitHub, and add a resume entry. The app is already fully functional with card view, filters, modals, and Pixabay image fetch. This pass adds view toggle, gender filtering, gender in forms/modals, and ships the project publicly.

---

## 1. View Toggle (Cards ↔ Table)

**Approach:** Two separate containers, show/hide based on `viewMode` state variable.

- Add two icon buttons to the toolbar (right of search, left of Add Shoe): grid icon and table icon
- Active view button highlighted with accent purple border/background
- `viewMode` defaults to `'card'`
- `#productGrid` (existing) used for card view
- New `#productTable` div added below `#productGrid` for table view, hidden by default
- `applyFilters()` routes to `renderCards(result)` or `renderTable(result)` based on `viewMode`

**Table spec:**
- Columns: Brand · Name · Gender · Size · Color · Price · Stock · Actions
- Column headers are clickable — sort asc/desc with arrow indicator (`↑` / `↓`)
- Sort state: `sortCol = null`, `sortDir = 'asc'`
- Clicking an already-active header flips direction
- Stock cell click opens existing edit qty modal
- Row click (outside action buttons) opens existing product detail modal
- Delete button in Actions column calls existing `deleteItem()`
- Styled to match dark purple theme (no Bootstrap table default colors)

---

## 2. Gender Filter

**Approach:** Pill buttons (mutually exclusive), new sidebar section above Brand.

- New "Gender" collapsible section in filter sidebar, above Brand
- Four pill buttons: `All` · `Men's` · `Women's` · `Kids'`
- `filters.gender = null` (null = All; string = specific gender)
- Selecting a pill sets `filters.gender` and calls `applyFilters()`
- Active pill styled with accent purple (same as active size buttons)
- Active non-All gender shows as a removable filter chip
- `clearAllFilters()` resets gender to null (All)

---

## 3. Gender in Add Form

- New `<select class="form-field">` field labeled "Gender" added to the form grid
- Options: `Men's` / `Women's` / `Kids'` (no empty default — required)
- Field ID: `fgender`
- POST body includes `gender: document.getElementById("fgender").value`

---

## 4. Gender in Detail Modal

- New `<div class="detail-spec-row">` for Gender added between Color and Stock rows
- Element ID: `detailGender`
- `openProduct()` populates it: `document.getElementById("detailGender").textContent = item.gender ?? "—"`

---

## 5. GitHub

- Repo name: `Sole-Studio` under `TrueEldenLord`
- Public repo
- Initialize git in `/shoe-store/`, commit all files (excluding `.env` per `.gitignore`)
- Push to `main`
- Use `/opt/homebrew/bin/gh` for repo creation (system `gh` opens browser)

---

## 6. Resume Entry

- Locate resume file in the project directory and add Sole Studio entry
- Highlight: Python/Flask, MongoDB, REST API, Bootstrap 5, Pixabay API, dynamic image fetching, responsive UI

---

## Implementation Order

1. Gender filter (sidebar + `applyFilters()`)
2. Gender in add form
3. Gender in detail modal
4. View toggle (toolbar buttons + `renderTable()` + sort logic)
5. GitHub repo + push
6. Resume entry

---

## Files Changed

- `frontend/index.html` — all frontend changes (single file)
- `backend/app.py` — no changes needed (gender already stored; PUT only updates quantity)
- Resume file — TBD path

---

## Constraints

- No new dependencies — vanilla JS + Bootstrap 5 only
- Flask runs on port 5050 (macOS AirPlay blocks 5000)
- Use `python3` not `python` (pyenv)
- `.env` excluded from git (contains Pixabay key)
- `gh` CLI at `/opt/homebrew/bin/gh`
