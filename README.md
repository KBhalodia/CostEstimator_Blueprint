# 🌱 Is It Worth Fixing? — Backend API

A RESTful API built with Python + Flask + SQLite that estimates whether it's cheaper to repair or replace a broken item.

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install flask
```

### 2. Run the app
```bash
python app.py
```

The server runs at: `http://127.0.0.1:5000`

---

## 📡 API Endpoints

### `POST /estimate`
Submit a broken item and get a repair vs. replace verdict.

**Request Body (JSON):**
```json
{
  "item": "laptop",
  "condition": "poor",
  "zip": "07936"
}
```
> `condition` options: `good`, `fair`, `poor`

**Response:**
```json
{
  "item": "laptop",
  "condition": "poor",
  "zip": "07936",
  "estimated_repair_cost": "$195.0",
  "estimated_replace_cost": "$700",
  "verdict": "Fix It ✅ — Repair is clearly worth it!"
}
```

---

### `GET /history`
Returns all past searches saved in the database.

**Response:**
```json
[
  {
    "id": 1,
    "item": "laptop",
    "condition": "poor",
    "zip": "07936",
    "estimated_repair_cost": "$195.0",
    "estimated_replace_cost": "$700",
    "verdict": "Fix It ✅ — Repair is clearly worth it!",
    "searched_at": "2026-04-05 12:00:00"
  }
]
```

---

### `DELETE /history/<id>`
Delete a specific search by its ID.

**Example:** `DELETE /history/1`

**Response:**
```json
{
  "message": "Search #1 deleted successfully."
}
```

---

### `GET /items`
See all supported items you can search for.

**Response:**
```json
{
  "supported_items": ["air conditioner", "bag", "bed frame", "bike", ...],
  "total": 34
}
```

---

## 🗄️ Database

SQLite database (`repair_app.db`) is auto-created on first run.

**Table: `searches`**
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-incremented primary key |
| item | TEXT | Item name |
| condition | TEXT | good / fair / poor |
| zip | TEXT | User's zip code |
| repair_cost | REAL | Estimated repair cost |
| replace_cost | REAL | Estimated replacement cost |
| verdict | TEXT | Fix it or replace it |
| created_at | DATETIME | Timestamp of search |

---

## 🧠 How Estimates Work

- Each item has a baseline repair and replacement cost stored in `estimator.py`
- Condition adjusts the repair cost:
  - `good` → 0.7x (minor damage)
  - `fair` → 1.0x (baseline)
  - `poor` → 1.3x (heavy damage)
- Verdict logic:
  - Repair ≤ 50% of replace → **Fix It ✅**
  - Repair ≤ 75% of replace → **Probably Fix It 🤔**
  - Repair > 75% of replace → **Replace It ❌**
