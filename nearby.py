import urllib.request
import urllib.parse
import json

# ----------------------------
# Paste your Google Places API key here
# ----------------------------
GOOGLE_API_KEY = "YOUR API KEY"

def zip_to_coords(zip_code: str):
    """Convert a zip code to lat/lng using Google Geocoding API."""
    encoded = urllib.parse.quote(zip_code)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded}&key={GOOGLE_API_KEY}"

    try:
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read())
            if data["status"] == "OK":
                loc = data["results"][0]["geometry"]["location"]
                return loc["lat"], loc["lng"]
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None


def get_nearby_repair_shops(zip_code: str, item: str):
    """
    Find nearby repair shops for a given item and zip code.
    Returns a list of shops with name, address, rating, and maps link.
    """
    lat, lng = zip_to_coords(zip_code)
    if not lat:
        return None

    # Build search query based on item type
    if any(x in item for x in ["phone", "iphone", "android", "ipad", "tablet"]):
        query = "phone repair shop"
    elif any(x in item for x in ["laptop", "macbook", "desktop", "computer", "pc"]):
        query = "computer repair shop"
    elif any(x in item for x in ["bike", "electric bike", "scooter", "skateboard"]):
        query = "bike repair shop"
    elif any(x in item for x in ["washing machine", "dryer", "refrigerator", "dishwasher", "oven", "appliance"]):
        query = "appliance repair shop"
    elif any(x in item for x in ["tv", "monitor", "smart tv"]):
        query = "electronics repair shop"
    else:
        query = "repair shop"

    encoded_query = urllib.parse.quote(query)
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}"
        f"&radius=8000"
        f"&type=store"
        f"&keyword={encoded_query}"
        f"&key={GOOGLE_API_KEY}"
    )

    try:
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read())

            shops = []
            for place in data.get("results", [])[:5]:
                shop = {
                    "name": place.get("name"),
                    "address": place.get("vicinity"),
                    "rating": place.get("rating", "N/A"),
                    "total_ratings": place.get("user_ratings_total", 0),
                    "open_now": place.get("opening_hours", {}).get("open_now", None),
                    "maps_link": f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
                }
                shops.append(shop)

            return shops

    except Exception as e:
        print(f"Places API error: {e}")
        return None
