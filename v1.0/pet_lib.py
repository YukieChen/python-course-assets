"""
Cyber-Pet Library - 視覺化電子雞工具庫

這是 Cyber-Pet 課程的核心視覺化工具庫，提供豐富的 HTML/CSS 介面元件，
讓學生能在 Jupyter Notebook 中創造互動式的電子雞遊戲。

主要功能：
- 圖片顯示與動畫
- 狀態條與數值視覺化
- 對話氣泡與互動元件
- 檔案儲存與讀取（v2.0+）
- UI 儀表板（v3.0+）
- 對話記憶系統（v4.0+）

Changelog:
- v1.0.0 (L01-L14): Initial release
  * show_egg() / summon() - 顯示神秘蛋
  * set_label(name) - 設定寵物名牌
  * show_pet(mood) - 顯示寵物表情
  * show_stats(name, hp, hunger, happiness) - 顯示狀態條
  * say(name, message) - 對話氣泡
  * show_image(filename, width) - 通用圖片顯示
"""

__version__ = "1.0.0"
__author__ = "Cyber-Pet Course Team"
__description__ = "視覺化電子雞工具庫"

import os
import base64
try:
    from IPython.display import display, HTML, Image
    MODE = "JUPYTER"
except ImportError:
    MODE = "TERMINAL"
    print("⚠️ IPython not found. Running in TERMINAL mode (Text only).")
    # Mock classes to prevent NameError
    def display(obj): pass 
    class HTML:
        def __init__(self, data): self.data = data
    class Image:
        def __init__(self, filename, width=None): self.filename = filename

# Constants
ASSETS_DIR = os.path.join("assets", "images")

# ==========================================
# Utility Functions (版本管理)
# ==========================================

def get_version():
    """取得當前 pet_lib 版本
    
    Returns:
        str: 版本號，例如 "1.0.0"
    
    Example:
        >>> import pet_lib as pet
        >>> print(pet.get_version())
        1.0.0
    """
    return __version__

def check_compatibility(required_version):
    """檢查版本相容性
    
    Args:
        required_version (str): 需要的最低版本，例如 "1.0.0"
    
    Returns:
        bool: True 表示相容，False 表示版本過舊
    
    Example:
        >>> import pet_lib as pet
        >>> if pet.check_compatibility("1.0.0"):
        >>>     print("版本相容！")
    """
    try:
        current = tuple(map(int, __version__.split('.')))
        required = tuple(map(int, required_version.split('.')))
        return current >= required
    except:
        return False

# ==========================================
# Core Functions (核心功能)
# ==========================================

def _get_img_path(filename):
    """Helper to get full path and verify existence."""
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        print(f"⚠️ Warning: Image {filename} not found. Did you run setup.py?")
        return None
    return path

def show_image(filename, width=200):
    """Display a raw image file."""
    if MODE == "TERMINAL":
        print(f"[IMAGE] {filename}")
        return

    path = _get_img_path(filename)
    if path:
        # Check if we need to embed as base64 (for Colab HTML support)
        try:
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            img_src = f"data:image/png;base64,{encoded}"
        except Exception as e:
            print(f"Error loading image: {e}")
            return

        # Use HTML for better control over sizing (maintain aspect ratio within box)
        html = f"""
        <div style="display: flex; justify-content: center; align-items: center; width: {width}px; height: {width}px; overflow: hidden;">
            <img src="{img_src}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
        </div>
        """
        display(HTML(html))

def show_egg():
    """Lesson 1: Show the Egg."""
    if MODE == "TERMINAL":
        print("(O) [Mystery Egg]")
        return
        
    print("Mystery Egg found!")
    show_image("egg.png")

# Alias for Lesson 1 Narrative
summon = show_egg

def show_pet(mood="normal"):
    """Show the pet with a specific mood (happy, sad, normal)."""
    if MODE == "TERMINAL":
        print(f"(^.{mood}.^) [Pet is {mood}]")
        return

    filename = f"{mood}.png"
    show_image(filename)

def show_stats(name, hp, hunger, happiness=None):
    """
    Render a beautiful HTML stat bar.
    Progress bars change color based on value.
    """
    if MODE == "TERMINAL":
        print(f"--- {name} ---")
        print(f"HP:       [{'#' * (hp//10):<10}] {hp}/100")
        print(f"Hunger:   [{'#' * (hunger//10):<10}] {hunger}/100")
        if happiness is not None:
            print(f"Happy:    [{'#' * (happiness//10):<10}] {happiness}/100")
        print("----------------")
        return
    
    def _bar_color(value):
        if value < 20: return "#ff4444" # Red
        if value < 50: return "#ffbb33" # Orange
        return "#00C851" # Green

    html = f"""
    <div style="
        border: 2px solid #333; 
        border-radius: 10px; 
        padding: 10px; 
        width: 300px; 
        background-color: #f0f0f0; 
        font-family: Arial, sans-serif;">
        
        <h3 style="margin: 0 0 10px 0; text-align: center;">🍱 {name}</h3>
        
        <!-- HP Bar -->
        <div style="margin-bottom: 5px;">
            <strong>HP:</strong> {hp}/100
            <div style="background-color: #ddd; border-radius: 5px; height: 10px; width: 100%;">
                <div style="
                    background-color: {_bar_color(hp)}; 
                    width: {min(hp, 100)}%; 
                    height: 100%; 
                    border-radius: 5px;
                    transition: width 0.5s;">
                </div>
            </div>
        </div>

        <!-- Hunger Bar -->
        <div style="margin-bottom: 5px;">
            <strong>Hunger:</strong> {hunger}/100
            <div style="background-color: #ddd; border-radius: 5px; height: 10px; width: 100%;">
                <div style="
                    background-color: {_bar_color(hunger)}; 
                    width: {min(hunger, 100)}%; 
                    height: 100%; 
                    border-radius: 5px;">
                </div>
            </div>
        </div>
    """
    
    if happiness is not None:
        html += f"""
        <!-- Happiness Bar -->
        <div>
            <strong>Happiness:</strong> {happiness}/100
            <div style="background-color: #ddd; border-radius: 5px; height: 10px; width: 100%;">
                <div style="
                    background-color: {_bar_color(happiness)}; 
                    width: {min(happiness, 100)}%; 
                    height: 100%; 
                    border-radius: 5px;">
                </div>
            </div>
        </div>
        """

    html += "</div>"
    display(HTML(html))

def say(name, message):
    """Render a speech bubble next to the name."""
    if MODE == "TERMINAL":
        print(f"{name}: {message}")
        return

    html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <div style="font-weight: bold; margin-right: 10px;">{name}:</div>
        <div style="
            background-color: #fff; 
            border: 2px solid #333; 
            color: #333;
            border-radius: 15px; 
            padding: 8px 15px; 
            position: relative;
            display: inline-block;">
            {message}
            <div style="
                content: '';
                position: absolute;
                left: -6px;
                top: 50%;
                width: 10px;
                height: 10px;
                background-color: #fff;
                border-left: 2px solid #333;
                border-bottom: 2px solid #333;
                transform: translateY(-50%) rotate(45deg);">
            </div>
        </div>
    </div>
    """
    display(HTML(html))

def set_label(name):
    """
    Lesson 2: Set the label (name) of the pet.
    Visualizes a name tag above the pet.
    """
    if MODE == "TERMINAL":
        print(f"[LABEL] Assigned Name: {name}")
        return

    html = f"""
    <div style="
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
        background-color: #FFEB3B; 
        color: #333; 
        padding: 5px 15px; 
        border-radius: 15px; 
        border: 3px solid #FBC02D;
        display: inline-block;
        font-weight: bold;
        font-size: 1.2em;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        margin-bottom: 10px;
        transform: rotate(-2deg);">
        Hello, my name is {name}
    </div>
    """
    display(HTML(html))
