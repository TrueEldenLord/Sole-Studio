# Shoe Store Management System

A full-stack inventory management app for a shoe store. Owners can add, remove, and update shoe inventory stored in MongoDB.

## Tech Stack

- **Backend:** Python (Flask) REST API
- **Frontend:** HTML + Bootstrap 5 + Vanilla JS
- **Database:** MongoDB

## Setup

### 1. Start MongoDB
Make sure MongoDB is running locally on port 27017.

### 2. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the backend
```bash
python app.py
```
Server runs at `http://localhost:5000`.

### 4. Open the frontend
Open `frontend/index.html` directly in your browser.

## Seed Sample Data
Click the **"Seed Sample Data"** button in the UI, or call the endpoint directly:
```bash
curl -X POST http://localhost:5000/seed
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | List all items |
| POST | `/inventory` | Add a new item |
| PUT | `/inventory/<id>` | Update item quantity |
| DELETE | `/inventory/<id>` | Remove an item |
| POST | `/seed` | Load sample data |
