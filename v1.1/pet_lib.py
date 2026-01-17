"""
Cyber-Pet Library - 視覺化電子雞工具庫 (v1.1)

這是 Cyber-Pet 課程的核心視覺化工具庫（重構版）。
保持所有功能向後相容，但改善了內部結構與說明文件。

主要功能：
- 圖片顯示與動畫
- 狀態條與數值視覺化
- 對話氣泡與互動元件

Changelog:
- v1.1.0 (L15): Refactored structure, improved documentation
- v1.0.0 (L01-L14): Initial release
"""

__version__ = "1.1.0"
__author__ = "Cyber-Pet Course Team"
__description__ = "視覺化電子雞工具庫 (Refactored)"

import os
import base64
from typing import Optional, Union

# 嘗試匯入 IPython 環境 (Jupyter Support)
try:
    from IPython.display import display, HTML, Image
    MODE = "JUPYTER"
except ImportError:
    MODE = "TERMINAL"
    print("⚠️ IPython not found. Running in TERMINAL mode (Text only).")
    # Mock classes for Terminal fallback
    def display(obj): pass 
    class HTML:
        def __init__(self, data): self.data = data
    class Image:
        def __init__(self, filename, width=None): self.filename = filename

# Constants
ASSETS_DIR = os.path.join("assets", "images")

# ==========================================
# Utility Functions (工具函式)
# ==========================================

def get_version() -> str:
    """取得當前 pet_lib 版本"""
    return __version__

def check_compatibility(required_version: str) -> bool:
    """檢查版本相容性"""
    try:
        current = tuple(map(int, __version__.split('.')))
        required = tuple(map(int, required_version.split('.')))
        return current >= required
    except:
        return False

def _get_img_path(filename: str) -> Optional[str]:
    """Helper to get full path and verify existence."""
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        print(f"⚠️ Warning: Image {filename} not found. Did you run setup.py?")
        return None
    return path

def _render_html(html_content: str):
    """Internal helper to render HTML content safely."""
    if MODE == "JUPYTER":
        display(HTML(html_content))
    else:
        # In terminal mode, we might want to strip HTML or just ignore
        pass

def _get_bar_color(value: int) -> str:
    """決定狀態條的顏色 (Refactored Logic)"""
    if value < 20: return "#ff4444" # Red (Critical)
    if value < 50: return "#ffbb33" # Orange (Warning)
    return "#00C851" # Green (Good)

# ==========================================
# Core Functions (核心功能)
# ==========================================

def show_image(filename: str, width: int = 200):
    """顯示原始圖片檔案"""
    if MODE == "TERMINAL":
        print(f"[IMAGE] {filename}")
        return

    path = _get_img_path(filename)
    if not path:
        return

    # Check if we need to embed as base64 (for Colab HTML support)
    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        img_src = f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Use HTML for better control over sizing
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: {width}px; height: {width}px; overflow: hidden;">
        <img src="{img_src}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
    </div>
    """
    _render_html(html)

def show_egg():
    """Lesson 1: 顯示神秘蛋"""
    if MODE == "TERMINAL":
        print("(O) [Mystery Egg]")
        return
        
    print("Mystery Egg found!")
    show_image("egg.png")

# Alias for backward compatibility
summon = show_egg

def show_pet(mood: str = "normal"):
    """顯示寵物表情 (happy, sad, normal)"""
    if MODE == "TERMINAL":
        print(f"(^.{mood}.^) [Pet is {mood}]")
        return

    filename = f"{mood}.png"
    show_image(filename)

def show_stats(name: str, hp: int, hunger: int, happiness: Optional[int] = None):
    """
    Render a beautiful HTML stat bar.
    Refactored in v1.1 to use _render_html helper.
    """
    if MODE == "TERMINAL":
        print(f"--- {name} ---")
        print(f"HP:       [{'#' * (hp//10):<10}] {hp}/100")
        print(f"Hunger:   [{'#' * (hunger//10):<10}] {hunger}/100")
        if happiness is not None:
            print(f"Happy:    [{'#' * (happiness//10):<10}] {happiness}/100")
        print("----------------")
        return
    
    # Internal helper for bar HTML generation (New in v1.1)
    def _create_bar_html(label, value):
        color = _get_bar_color(value)
        return f"""
        <div style="margin-bottom: 5px;">
            <strong>{label}:</strong> {value}/100
            <div style="background-color: #ddd; border-radius: 5px; height: 10px; width: 100%;">
                <div style="
                    background-color: {color}; 
                    width: {min(value, 100)}%; 
                    height: 100%; 
                    border-radius: 5px;
                    transition: width 0.5s;">
                </div>
            </div>
        </div>
        """

    content_html = f"""<h3 style="margin: 0 0 10px 0; text-align: center;">🍱 {name}</h3>"""
    content_html += _create_bar_html("HP", hp)
    content_html += _create_bar_html("Hunger", hunger)
    
    if happiness is not None:
        content_html += _create_bar_html("Happiness", happiness)

    container_html = f"""
    <div style="
        border: 2px solid #333; 
        border-radius: 10px; 
        padding: 10px; 
        width: 300px; 
        background-color: #f0f0f0; 
        font-family: Arial, sans-serif;">
        {content_html}
    </div>
    """
    
    _render_html(container_html)

def say(name: str, message: str):
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
    _render_html(html)

def set_label(name: str):
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
    _render_html(html)
