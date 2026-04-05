import json
import urllib.request

# ----------------------------
# Paste your OpenRouter API key here
# ----------------------------
OPENROUTER_API_KEY = "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"

REPAIR_DATA = {
    # Electronics
    "laptop":               {"repair_cost": 150, "replace_cost": 700},
    "macbook":              {"repair_cost": 200, "replace_cost": 1200},
    "phone":                {"repair_cost": 100, "replace_cost": 500},
    "iphone":               {"repair_cost": 120, "replace_cost": 800},
    "android phone":        {"repair_cost": 90,  "replace_cost": 500},
    "tablet":               {"repair_cost": 120, "replace_cost": 400},
    "ipad":                 {"repair_cost": 120, "replace_cost": 450},
    "ipad air":             {"repair_cost": 130, "replace_cost": 600},
    "ipad mini":            {"repair_cost": 110, "replace_cost": 500},
    "ipad pro":             {"repair_cost": 200, "replace_cost": 1000},
    "monitor":              {"repair_cost": 80,  "replace_cost": 250},
    "keyboard":             {"repair_cost": 30,  "replace_cost": 80},
    "mouse":                {"repair_cost": 20,  "replace_cost": 40},
    "headphones":           {"repair_cost": 40,  "replace_cost": 150},
    "airpods":              {"repair_cost": 60,  "replace_cost": 180},
    "earbuds":              {"repair_cost": 30,  "replace_cost": 80},
    "smartwatch":           {"repair_cost": 90,  "replace_cost": 300},
    "apple watch":          {"repair_cost": 120, "replace_cost": 400},
    "tv":                   {"repair_cost": 200, "replace_cost": 600},
    "smart tv":             {"repair_cost": 200, "replace_cost": 700},
    "desktop":              {"repair_cost": 180, "replace_cost": 800},
    "camera":               {"repair_cost": 130, "replace_cost": 500},
    "dslr camera":          {"repair_cost": 200, "replace_cost": 800},
    "gopro":                {"repair_cost": 80,  "replace_cost": 300},
    "printer":              {"repair_cost": 70,  "replace_cost": 150},
    "router":               {"repair_cost": 40,  "replace_cost": 100},
    "speaker":              {"repair_cost": 50,  "replace_cost": 150},
    "bluetooth speaker":    {"repair_cost": 40,  "replace_cost": 80},
    "nintendo switch":      {"repair_cost": 100, "replace_cost": 300},
    "ps5":                  {"repair_cost": 150, "replace_cost": 500},
    "ps4":                  {"repair_cost": 100, "replace_cost": 200},
    "xbox":                 {"repair_cost": 120, "replace_cost": 400},
    "game controller":      {"repair_cost": 40,  "replace_cost": 70},
    "projector":            {"repair_cost": 150, "replace_cost": 400},
    "drone":                {"repair_cost": 100, "replace_cost": 400},
    "electric toothbrush":  {"repair_cost": 20,  "replace_cost": 50},
    "hair dryer":           {"repair_cost": 25,  "replace_cost": 40},
    "electric razor":       {"repair_cost": 30,  "replace_cost": 60},
    "calculator":           {"repair_cost": 15,  "replace_cost": 20},
 
    # Appliances
    "washing machine":      {"repair_cost": 180, "replace_cost": 600},
    "dryer":                {"repair_cost": 150, "replace_cost": 500},
    "refrigerator":         {"repair_cost": 200, "replace_cost": 900},
    "mini fridge":          {"repair_cost": 80,  "replace_cost": 150},
    "dishwasher":           {"repair_cost": 160, "replace_cost": 500},
    "microwave":            {"repair_cost": 70,  "replace_cost": 150},
    "oven":                 {"repair_cost": 200, "replace_cost": 700},
    "stove":                {"repair_cost": 150, "replace_cost": 600},
    "air conditioner":      {"repair_cost": 250, "replace_cost": 600},
    "portable ac":          {"repair_cost": 100, "replace_cost": 300},
    "vacuum":               {"repair_cost": 60,  "replace_cost": 200},
    "robot vacuum":         {"repair_cost": 100, "replace_cost": 300},
    "coffee maker":         {"repair_cost": 40,  "replace_cost": 100},
    "espresso machine":     {"repair_cost": 150, "replace_cost": 400},
    "toaster":              {"repair_cost": 20,  "replace_cost": 30},
    "toaster oven":         {"repair_cost": 40,  "replace_cost": 80},
    "blender":              {"repair_cost": 35,  "replace_cost": 80},
    "food processor":       {"repair_cost": 50,  "replace_cost": 120},
    "air fryer":            {"repair_cost": 45,  "replace_cost": 100},
    "instant pot":          {"repair_cost": 50,  "replace_cost": 100},
    "rice cooker":          {"repair_cost": 30,  "replace_cost": 50},
    "kettle":               {"repair_cost": 20,  "replace_cost": 30},
    "stand mixer":          {"repair_cost": 80,  "replace_cost": 300},
    "dehumidifier":         {"repair_cost": 100, "replace_cost": 200},
    "humidifier":           {"repair_cost": 40,  "replace_cost": 80},
    "fan":                  {"repair_cost": 30,  "replace_cost": 50},
    "space heater":         {"repair_cost": 40,  "replace_cost": 60},
    "iron":                 {"repair_cost": 25,  "replace_cost": 40},
    "sewing machine":       {"repair_cost": 80,  "replace_cost": 200},
    "freezer":              {"repair_cost": 150, "replace_cost": 400},
    "water heater":         {"repair_cost": 300, "replace_cost": 700},
 
    # Bikes & Vehicles
    "bike":                 {"repair_cost": 80,  "replace_cost": 400},
    "electric bike":        {"repair_cost": 200, "replace_cost": 1200},
    "scooter":              {"repair_cost": 150, "replace_cost": 500},
    "electric scooter":     {"repair_cost": 120, "replace_cost": 400},
    "skateboard":           {"repair_cost": 30,  "replace_cost": 100},
    "electric skateboard":  {"repair_cost": 150, "replace_cost": 500},
    "hoverboard":           {"repair_cost": 80,  "replace_cost": 200},
    "longboard":            {"repair_cost": 30,  "replace_cost": 100},
    "car":                  {"repair_cost": 500, "replace_cost": 20000},
    "motorcycle":           {"repair_cost": 400, "replace_cost": 8000},
    "treadmill":            {"repair_cost": 150, "replace_cost": 600},
    "exercise bike":        {"repair_cost": 100, "replace_cost": 300},
 
    # Furniture
    "chair":                {"repair_cost": 60,  "replace_cost": 200},
    "gaming chair":         {"repair_cost": 80,  "replace_cost": 300},
    "office chair":         {"repair_cost": 70,  "replace_cost": 250},
    "couch":                {"repair_cost": 150, "replace_cost": 700},
    "sofa":                 {"repair_cost": 150, "replace_cost": 800},
    "desk":                 {"repair_cost": 80,  "replace_cost": 300},
    "standing desk":        {"repair_cost": 100, "replace_cost": 400},
    "bed frame":            {"repair_cost": 100, "replace_cost": 400},
    "mattress":             {"repair_cost": 50,  "replace_cost": 500},
    "bookshelf":            {"repair_cost": 40,  "replace_cost": 100},
    "dresser":              {"repair_cost": 80,  "replace_cost": 200},
    "table":                {"repair_cost": 70,  "replace_cost": 200},
    "lamp":                 {"repair_cost": 20,  "replace_cost": 40},
 
    # Clothing / Accessories
    "jacket":               {"repair_cost": 30,  "replace_cost": 100},
    "winter coat":          {"repair_cost": 40,  "replace_cost": 150},
    "shoes":                {"repair_cost": 25,  "replace_cost": 80},
    "sneakers":             {"repair_cost": 30,  "replace_cost": 100},
    "boots":                {"repair_cost": 40,  "replace_cost": 120},
    "bag":                  {"repair_cost": 20,  "replace_cost": 60},
    "backpack":             {"repair_cost": 25,  "replace_cost": 70},
    "purse":                {"repair_cost": 30,  "replace_cost": 100},
    "watch":                {"repair_cost": 50,  "replace_cost": 200},
    "sunglasses":           {"repair_cost": 20,  "replace_cost": 80},
    "glasses":              {"repair_cost": 50,  "replace_cost": 200},
 
    # Musical Instruments
    "guitar":               {"repair_cost": 80,  "replace_cost": 300},
    "electric guitar":      {"repair_cost": 100, "replace_cost": 500},
    "piano":                {"repair_cost": 200, "replace_cost": 2000},
    "keyboard instrument":  {"repair_cost": 100, "replace_cost": 400},
    "violin":               {"repair_cost": 100, "replace_cost": 500},
    "drum kit":             {"repair_cost": 150, "replace_cost": 600},
    "headset":              {"repair_cost": 40,  "replace_cost": 100},
 
    # Sports & Outdoor
    "tent":                 {"repair_cost": 30,  "replace_cost": 150},
    "kayak":                {"repair_cost": 80,  "replace_cost": 500},
    "surfboard":            {"repair_cost": 60,  "replace_cost": 400},
    "golf clubs":           {"repair_cost": 50,  "replace_cost": 300},
    "tennis racket":        {"repair_cost": 20,  "replace_cost": 80},
}
 
CONDITION_MULTIPLIERS = {
    "poor": 1.3,
    "fair": 1.0,
    "good": 0.7,
}
 
def ask_ai(item: str, condition: str):
    """Fallback to OpenRouter AI for truly unknown items."""
    prompt = f"""You are a repair cost estimator. A user has a broken '{item}' in '{condition}' condition.
Estimate the average repair cost and replacement cost in USD.
Respond ONLY with a valid JSON object like this, no explanation, no markdown:
{{"repair_cost": 120, "replace_cost": 500}}"""
 
    url = "https://openrouter.ai/api/v1/chat/completions"
    body = json.dumps({
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")
 
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    })
 
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            text = result["choices"][0]["message"]["content"]
            text = text.strip().replace("```json", "").replace("```", "").strip()
            parsed = json.loads(text)
            return {
                "repair_cost": float(parsed["repair_cost"]),
                "replace_cost": float(parsed["replace_cost"])
            }
    except Exception as e:
        print(f"AI error: {e}")
        return None
 
 
def get_estimate(item: str, condition: str):
    if condition not in CONDITION_MULTIPLIERS:
        condition = "fair"
 
    multiplier = CONDITION_MULTIPLIERS[condition]
 
    if item in REPAIR_DATA:
        data = REPAIR_DATA[item]
        return {
            "repair_cost": round(data["repair_cost"] * multiplier, 2),
            "replace_cost": data["replace_cost"],
            "source": "database"
        }
 
    print(f"'{item}' not in database — asking AI...")
    ai_result = ask_ai(item, condition)
 
    if ai_result:
        return {
            "repair_cost": round(ai_result["repair_cost"] * multiplier, 2),
            "replace_cost": ai_result["replace_cost"],
            "source": "ai"
        }
 
    return None