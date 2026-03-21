
import os
import urllib.request

# Configuration
ASSETS_DIR = "assets"
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
# TODO: Replace with your actual GitHub username and repo name after uploading
GITHUB_USER = "YukieChen" 
REPO_NAME = "python-course-assets"
BRANCH = "main"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/assets/images"

# List of files to download (required)
IMAGE_FILES = [
    "egg.png",
    "happy.png",
    "sad.png",
    "normal.png",
    "poop.png",
    "pet_lib_book.png",
]

# Optional dedicated growth art (v1.1+). If missing on CDN, pet_lib uses mood/egg fallback.
OPTIONAL_GROWTH_IMAGES = [
    "growth_egg.png",
    "growth_hatchling.png",
    "growth_juvenile.png",
    "growth_tween.png",
    "growth_partner.png",
    # 選用插圖（非 show_growth_stage stage 檔名）
    "growth_duo_scene.png",
]


def _download_one(url, filepath, optional=False):
    if "YOUR_GITHUB_USER" in url:
        print(f"\n   ⚠️ SKIPPING: You must update 'GITHUB_USER' in setup.py first!")
        return
    try:
        urllib.request.urlretrieve(url, filepath)
        print(" Done!")
    except Exception as e:
        if optional:
            print(f" skip (optional): {e}")
        else:
            print(f" Error: {e}")


def install_assets():
    """Derived from the 'summoning spell'. Downloads necessary images."""
    print("🔮 Summoning digital spirits... (Downloading assets)")

    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"📦 Created {IMAGES_DIR} directory.")

    for filename in IMAGE_FILES:
        url = f"{BASE_URL}/{filename}"
        filepath = os.path.join(IMAGES_DIR, filename)
        if not os.path.exists(filepath):
            print(f"   ⬇️ Downloading {filename}...", end="")
            _download_one(url, filepath, optional=False)
        else:
            print(f"   ✨ {filename} already exists.")

    for filename in OPTIONAL_GROWTH_IMAGES:
        url = f"{BASE_URL}/{filename}"
        filepath = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(filepath):
            print(f"   ✨ {filename} already exists.")
            continue
        print(f"   ⬇️ Downloading (optional) {filename}...", end="")
        _download_one(url, filepath, optional=True)

    print("\n✅ Setup Complete! Your world is ready.")

if __name__ == "__main__":
    install_assets()
