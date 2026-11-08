from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import requests as http
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client["shoe_store"]
inventory = db["inventory"]


SHOE_TAGS = {
    "shoe", "shoes", "sneaker", "sneakers", "footwear", "boot", "boots",
    "athletic", "running", "trainer", "trainers", "heel", "sole", "cleat",
    "nike", "adidas", "converse", "vans", "reebok", "puma", "new balance",
    "asics", "brooks", "saucony", "hoka", "jordan", "yeezy", "air max",
}

# For these brands, the Pixabay tags must include the brand name
BRAND_SPECIFIC = {
    "nike", "adidas", "converse", "vans", "asics", "puma", "reebok",
    "new balance", "brooks", "saucony", "hoka", "jordan",
}

def fetch_shoe_image(name, brand, color=None, used_ids=None):
    key = os.environ.get("PIXABAY_API_KEY", "")
    if not key:
        return None
    if used_ids is None:
        used_ids = set()

    # Pass 1 & 2: brand-specific queries with brand tag requirement
    # Pass 3: fallback — any shoe image, no brand requirement
    passes = [
        (f"{brand} {name} shoe sneaker", True),
        (f"{brand} sneaker shoe",        True),
        (f"{name} sneaker shoe",         False),
    ]
    try:
        for query, require_brand in passes:
            for page in range(1, 4):
                r = http.get(
                    "https://pixabay.com/api/",
                    params={
                        "key": key,
                        "q": query,
                        "image_type": "photo",
                        "orientation": "horizontal",
                        "per_page": 10,
                        "page": page,
                        "safesearch": "true",
                    },
                    timeout=6,
                )
                if r.status_code == 200:
                    for hit in r.json().get("hits", []):
                        if hit["id"] in used_ids:
                            continue
                        tags_str = hit.get("tags", "").lower()
                        tags = {t.strip() for t in tags_str.split(",")}
                        if not (tags & SHOE_TAGS):
                            continue
                        if require_brand and brand.lower() in BRAND_SPECIFIC and brand.lower() not in tags_str:
                            continue
                        used_ids.add(hit["id"])
                        return hit["webformatURL"]
    except Exception:
        pass
    return None


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


# ---------- Routes ----------

@app.get("/")
def serve_frontend():
    return send_from_directory("frontend", "index.html")


@app.get("/inventory")
def get_inventory():
    items = [serialize(item) for item in inventory.find()]
    return jsonify(items)


@app.post("/inventory")
def add_item():
    data = request.json
    required = ["name", "brand", "size", "color", "price", "quantity"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400
    if not data.get("image"):
        data["image"] = fetch_shoe_image(data["name"], data["brand"], data.get("color"))
    result = inventory.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201


@app.put("/inventory/<item_id>")
def update_quantity(item_id):
    data = request.json
    if "quantity" not in data:
        return jsonify({"error": "quantity required"}), 400
    result = inventory.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {"quantity": data["quantity"]}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"updated": True})


@app.delete("/inventory/<item_id>")
def delete_item(item_id):
    result = inventory.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"deleted": True})


@app.post("/seed")
def seed():
    inventory.delete_many({})
    sample = [
        # Nike — Men's
        {"name": "Air Max 90",       "brand": "Nike",        "gender": "Men's",   "size": 10,   "color": "White",   "price": 120.00, "quantity": 15},
        {"name": "Air Force 1",      "brand": "Nike",        "gender": "Men's",   "size": 11,   "color": "White",   "price": 110.00, "quantity": 20},
        {"name": "Air Jordan 1",     "brand": "Nike",        "gender": "Men's",   "size": 10,   "color": "Red",     "price": 180.00, "quantity": 7},
        {"name": "Dunk Low",         "brand": "Nike",        "gender": "Men's",   "size": 9,    "color": "Black",   "price": 110.00, "quantity": 14},
        {"name": "React Infinity",   "brand": "Nike",        "gender": "Men's",   "size": 12,   "color": "Blue",    "price": 160.00, "quantity": 9},
        # Nike — Women's
        {"name": "Air Max 270",      "brand": "Nike",        "gender": "Women's", "size": 7,    "color": "Pink",    "price": 150.00, "quantity": 11},
        {"name": "Free Run 5.0",     "brand": "Nike",        "gender": "Women's", "size": 8,    "color": "White",   "price": 100.00, "quantity": 14},
        # Nike — Kids'
        {"name": "Revolution 6",     "brand": "Nike",        "gender": "Kids'",   "size": 4,    "color": "Blue",    "price": 55.00,  "quantity": 18},
        # Adidas — Men's
        {"name": "Stan Smith",       "brand": "Adidas",      "gender": "Men's",   "size": 10,   "color": "White",   "price": 85.00,  "quantity": 18},
        {"name": "Ultraboost 22",    "brand": "Adidas",      "gender": "Men's",   "size": 10,   "color": "Black",   "price": 190.00, "quantity": 12},
        {"name": "Forum Low",        "brand": "Adidas",      "gender": "Men's",   "size": 11,   "color": "White",   "price": 100.00, "quantity": 10},
        # Adidas — Women's
        {"name": "Superstar",        "brand": "Adidas",      "gender": "Women's", "size": 7.5,  "color": "White",   "price": 90.00,  "quantity": 25},
        {"name": "Gazelle",          "brand": "Adidas",      "gender": "Women's", "size": 8,    "color": "Pink",    "price": 100.00, "quantity": 13},
        # Adidas — Kids'
        {"name": "Racer TR21",       "brand": "Adidas",      "gender": "Kids'",   "size": 3,    "color": "Black",   "price": 45.00,  "quantity": 20},
        # Converse
        {"name": "Chuck Taylor",     "brand": "Converse",    "gender": "Men's",   "size": 9,    "color": "Black",   "price": 65.00,  "quantity": 22},
        {"name": "Chuck 70",         "brand": "Converse",    "gender": "Women's", "size": 7,    "color": "White",   "price": 85.00,  "quantity": 16},
        {"name": "Chuck Taylor Low", "brand": "Converse",    "gender": "Kids'",   "size": 2,    "color": "Red",     "price": 40.00,  "quantity": 15},
        # Vans
        {"name": "Old Skool",        "brand": "Vans",        "gender": "Men's",   "size": 11,   "color": "Black",   "price": 70.00,  "quantity": 30},
        {"name": "Sk8-Hi",           "brand": "Vans",        "gender": "Men's",   "size": 10,   "color": "Black",   "price": 80.00,  "quantity": 11},
        {"name": "Slip-On",          "brand": "Vans",        "gender": "Women's", "size": 8,    "color": "Grey",    "price": 60.00,  "quantity": 3},
        {"name": "Era",              "brand": "Vans",        "gender": "Kids'",   "size": 3.5,  "color": "Navy",    "price": 50.00,  "quantity": 17},
        # New Balance
        {"name": "990v5",            "brand": "New Balance", "gender": "Men's",   "size": 10,   "color": "Grey",    "price": 175.00, "quantity": 10},
        {"name": "574",              "brand": "New Balance", "gender": "Men's",   "size": 13,   "color": "Navy",    "price": 90.00,  "quantity": 19},
        {"name": "Fresh Foam 1080",  "brand": "New Balance", "gender": "Women's", "size": 8.5,  "color": "White",   "price": 165.00, "quantity": 6},
        # ASICS
        {"name": "Gel-Nimbus 25",    "brand": "ASICS",       "gender": "Men's",   "size": 9,    "color": "Blue",    "price": 160.00, "quantity": 8},
        {"name": "Gel-Kayano 30",    "brand": "ASICS",       "gender": "Women's", "size": 7.5,  "color": "Black",   "price": 160.00, "quantity": 4},
        # Puma
        {"name": "Suede Classic",    "brand": "Puma",        "gender": "Men's",   "size": 10,   "color": "Black",   "price": 75.00,  "quantity": 13},
        {"name": "RS-X",             "brand": "Puma",        "gender": "Women's", "size": 8,    "color": "White",   "price": 110.00, "quantity": 8},
        # Reebok
        {"name": "Classic Leather",  "brand": "Reebok",      "gender": "Men's",   "size": 10,   "color": "White",   "price": 80.00,  "quantity": 17},
        {"name": "Club C 85",        "brand": "Reebok",      "gender": "Women's", "size": 7,    "color": "White",   "price": 75.00,  "quantity": 21},
        # Hoka
        {"name": "Clifton 9",        "brand": "Hoka",        "gender": "Men's",   "size": 11,   "color": "Blue",    "price": 145.00, "quantity": 5},
        {"name": "Bondi 8",          "brand": "Hoka",        "gender": "Women's", "size": 8.5,  "color": "Black",   "price": 165.00, "quantity": 9},
        # Saucony
        {"name": "Jazz Original",    "brand": "Saucony",     "gender": "Men's",   "size": 10,   "color": "Blue",    "price": 80.00,  "quantity": 12},
        {"name": "Ride 16",          "brand": "Saucony",     "gender": "Women's", "size": 8,    "color": "Grey",    "price": 130.00, "quantity": 7},
    ]
    used_ids = set()
    for item in sample:
        item["image"] = fetch_shoe_image(item["name"], item["brand"], item.get("color"), used_ids)
    inventory.insert_many(sample)
    return jsonify({"seeded": len(sample)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
