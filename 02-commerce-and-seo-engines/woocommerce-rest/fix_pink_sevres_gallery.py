import os
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://thechapmancollection.com"
AUTH = HTTPBasicAuth("neverrender-labs", os.getenv("WP_REST_APP_PASSWORD", ""))

# 1. Fetch current Pink Sevres product by slug
r = requests.get(
    f"{BASE_URL}/wp-json/wc/v3/products",
    auth=AUTH,
    params={"slug": "antique-pink-sevres-porcelain-curiosity-chest-with-pastoral-scene"}
)
r.raise_for_status()
products = r.json()
assert len(products) == 1, f"Expected 1 product, got {len(products)}"
prod = products[0]
pid = prod["id"]
print(f"Found Product ID {pid}: {prod['name']}")
print("Current images:")
for idx, im in enumerate(prod["images"]):
    print(f"  [{idx}] ID={im['id']} | name={im['name']} | src={im['src']}")

# 2. Check if the Octagonal Lid View is already in WP Media Library, or upload the user's top-down lid photo
lid_photo_path = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2\.user_uploaded\media_1793206502617_4ff00187.jpg"
filename = "antique-pink-sevres-porcelain-curiosity-chest-pastoral-lid-closeup.jpg"
with open(lid_photo_path, "rb") as f:
    img_bytes = f.read()

headers = {
    "Content-Disposition": f'attachment; filename="{filename}"',
    "Content-Type": "image/jpeg",
}
r_up = requests.post(f"{BASE_URL}/wp-json/wp/v2/media", auth=AUTH, headers=headers, data=img_bytes)
r_up.raise_for_status()
lid_media_id = r_up.json()["id"]

title = "Antique Pink Sèvres Porcelain Curiosity Chest with Pastoral Scene - Octagonal Lid Close-Up"
alt_text = "Close-up of octagonal lid on antique Sèvres style pink porcelain curiosity chest showing hand painted romantic pastoral courtship scene and gilt lattice border"
caption = "Octagonal hinged lid featuring a finely painted romantic pastoral courtship scene framed by gilt scrollwork and lattice decoration."

requests.post(
    f"{BASE_URL}/wp-json/wp/v2/media/{lid_media_id}",
    auth=AUTH,
    json={
        "title": title,
        "alt_text": alt_text,
        "caption": caption,
        "description": caption,
    },
).raise_for_status()
print(f"Uploaded Lid Close-Up Media ID: {lid_media_id}")

# Keep Image 0 (Main front view) and Image 1 (Open interior view), and replace the duplicate Image 2 with the Lid Close-Up!
# Or put Lid Close-Up right after Main front view: [Front View, Lid Close-Up, Open Interior View]
curr_imgs = prod["images"]
front_id = curr_imgs[0]["id"]
open_id = curr_imgs[1]["id"]

new_images = [
    {"id": front_id},
    {"id": lid_media_id},
    {"id": open_id},
]

r_upd = requests.put(
    f"{BASE_URL}/wp-json/wc/v3/products/{pid}",
    auth=AUTH,
    json={"images": new_images}
)
r_upd.raise_for_status()
updated = r_upd.json()
print("Updated Product Images:")
for idx, im in enumerate(updated["images"]):
    print(f"  [{idx}] ID={im['id']} | name={im['name']} | src={im['src']}")
