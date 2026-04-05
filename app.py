from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, get_db
from estimator import get_estimate
from nearby import get_nearby_repair_shops
import sqlite3

app = Flask(__name__)
CORS(app)


# Initialize the database when app starts
init_db()

# ----------------------------
# POST /estimate
# Submit an item to get repair vs replace verdict
# ----------------------------
@app.route("/estimate", methods=["POST"])
def estimate():
    data = request.get_json()

    # Validate required fields
    required = ["item", "condition", "zip"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    item = data["item"].lower().strip()
    condition = data["condition"].lower().strip()
    zip_code = data["zip"].strip()

    # Get repair vs replace estimate
    result = get_estimate(item, condition)
    if not result:
        return jsonify({"error": f"Item '{item}' not recognized. Try a common item like 'laptop', 'phone', or 'bike'."}), 404

    repair_cost = result["repair_cost"]
    replace_cost = result["replace_cost"]

    # Verdict logic
    if repair_cost <= replace_cost * 0.5:
        verdict = "Fix It ✅ — Repair is clearly worth it!"
    elif repair_cost <= replace_cost * 0.75:
        verdict = "Probably Fix It 🤔 — Repair is still cheaper."
    else:
        verdict = "Replace It ❌ — Not worth the repair cost."

    # Save to database
    db = get_db()
    db.execute(
        "INSERT INTO searches (item, condition, zip, repair_cost, replace_cost, verdict) VALUES (?, ?, ?, ?, ?, ?)",
        (item, condition, zip_code, repair_cost, replace_cost, verdict)
    )
    db.commit()
    db.close()

    return jsonify({
        "item": item,
        "condition": condition,
        "zip": zip_code,
        "estimated_repair_cost": f"${repair_cost}",
        "estimated_replace_cost": f"${replace_cost}",
        "verdict": verdict
    }), 201


# ----------------------------
# GET /history
# Get all past searches
# ----------------------------
@app.route("/history", methods=["GET"])
def history():
    db = get_db()
    rows = db.execute("SELECT * FROM searches ORDER BY created_at DESC").fetchall()
    db.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "item": row["item"],
            "condition": row["condition"],
            "zip": row["zip"],
            "estimated_repair_cost": f"${row['repair_cost']}",
            "estimated_replace_cost": f"${row['replace_cost']}",
            "verdict": row["verdict"],
            "searched_at": row["created_at"]
        })

    return jsonify(results), 200


# ----------------------------
# DELETE /history/<id>
# Delete a specific search by ID
# ----------------------------
@app.route("/history/<int:search_id>", methods=["DELETE"])
def delete_search(search_id):
    db = get_db()
    row = db.execute("SELECT * FROM searches WHERE id = ?", (search_id,)).fetchone()

    if not row:
        db.close()
        return jsonify({"error": f"No search found with id {search_id}"}), 404

    db.execute("DELETE FROM searches WHERE id = ?", (search_id,))
    db.commit()
    db.close()

    return jsonify({"message": f"Search #{search_id} deleted successfully."}), 200


# ----------------------------
# GET /items
# See all supported items
# ----------------------------
@app.route("/items", methods=["GET"])
def list_items():
    from estimator import REPAIR_DATA
    items = sorted(REPAIR_DATA.keys())
    return jsonify({"supported_items": items, "total": len(items)}), 200


# ----------------------------
# GET /nearby-shops
# Find nearby repair shops based on zip code and item
# Example: /nearby-shops?zip=07936&item=laptop
# ----------------------------
@app.route("/nearby-shops", methods=["GET"])
def nearby_shops():
    zip_code = request.args.get("zip", "").strip()
    item = request.args.get("item", "").strip().lower()

    if not zip_code:
        return jsonify({"error": "Missing required parameter: zip"}), 400
    if not item:
        return jsonify({"error": "Missing required parameter: item"}), 400

    shops = get_nearby_repair_shops(zip_code, item)

    if shops is None:
        return jsonify({"error": "Could not find nearby shops. Check your zip code or API key."}), 500

    if len(shops) == 0:
        return jsonify({"message": "No repair shops found nearby.", "shops": []}), 200

    return jsonify({
        "item": item,
        "zip": zip_code,
        "total_found": len(shops),
        "shops": shops
    }), 200


if __name__ == "__main__":
    app.run(debug=True)