
import os
import urllib.request

# Configuration
ASSETS_DIR = "assets"
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
# TODO: Replace with your actual GitHub username and repo name after uploading
GITHUB_USER = "YukieChen" 
REPO_NAME = "python-course-assets"
BRANCH = "main"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/assets"

# List of files to download
IMAGE_FILES = [
    "egg.png",
    "happy.png",
    "sad.png",
    "normal.png",
    "poop.png"
]

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
            try:
                print(f"   ⬇️ Downloading {filename}...", end="")
                
                # Check if user forgot to update URL
                if "YOUR_GITHUB_USER" in url:
                    print(f"\n   ⚠️ SKIPPING: You must update 'GITHUB_USER' in setup.py first!")
                    continue

                urllib.request.urlretrieve(url, filepath)
                print(" Done!")
            except Exception as e:
                print(f" Error: {e}")
        else:
            print(f"   ✨ {filename} already exists.")
            
    print("\n✅ Setup Complete! Your world is ready.")

if __name__ == "__main__":
    install_assets()
