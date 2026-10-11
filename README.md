# Sole Studio — Shoe Store Inventory Management

A full-stack inventory management app built with Python/Flask, MongoDB, and Bootstrap 5. Features a dual-view UI (card grid and sortable data table), dynamic Pixabay image fetch, and a filter sidebar with gender, brand, size, and price filters.

## Features

- **Dual view** — toggle between a card grid and a sortable spreadsheet table
- **Filter sidebar** — gender (Men's / Women's / Kids'), brand checkboxes, size grid, price range, with active filter chips
- **Auto images** — Pixabay API fetches shoe photos on item creation with brand-tag validation
- **Stats dashboard** — live SKU count, total units, retail value, and low-stock alert
- **Full CRUD** — add, edit quantity, and delete items; product detail modal on every item
- **35 seed items** across Nike, Adidas, Converse, Vans, New Balance, ASICS, Puma, Reebok, Hoka, Saucony

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask, Flask-CORS |
| Database | MongoDB (local, port 27017) |
| Frontend | Vanilla JS, Bootstrap 5.3, Bootstrap Icons |
| Images | Pixabay API |

## Setup

### 1. Start MongoDB
```bash
mkdir -p /tmp/mongodata && mongod --dbpath /tmp/mongodata --fork --logpath /tmp/mongod.log
```

### 2. Install backend dependencies
```bash
cd backend
pip3 install -r requirements.txt
```

### 3. Add your Pixabay API key
Create `backend/.env`:
```
PIXABAY_API_KEY=your_key_here
```
Get a free key at [pixabay.com/api/docs](https://pixabay.com/api/docs/). Images will fall back to placeholders if omitted.

### 4. Run the backend
```bash
cd backend
python3 app.py
```
Server runs at `http://localhost:5050`.

### 5. Open the frontend
Open `frontend/index.html` directly in your browser.

### 6. Seed sample data
```bash
curl -X POST http://localhost:5050/seed
```
Loads 35 shoes across 10 brands with auto-fetched images (~30 seconds with Pixabay).

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | List all items |
| POST | `/inventory` | Add a new item (auto-fetches image) |
| PUT | `/inventory/<id>` | Update item quantity |
| DELETE | `/inventory/<id>` | Remove an item |
| POST | `/seed` | Reset and load 35 sample items |

## Project Structure

```
shoe-store/
├── backend/
│   ├── app.py          # Flask REST API + Pixabay image fetch
│   ├── requirements.txt
│   └── .env            # PIXABAY_API_KEY (gitignored)
└── frontend/
    └── index.html      # Single-file frontend (JS + CSS + HTML)
```
