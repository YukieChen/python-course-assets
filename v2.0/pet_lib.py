"""
Cyber-Pet Library - 視覺化電子雞工具庫 (v2.0)

這是 Cyber-Pet 課程的核心視覺化工具庫 (Dictionary 支援版)。
新增了支援從 Dictionary 讀取資料的功能，並保留向後相容。

主要功能：
- show_pet_dict: 支援傳入字典
- show_stats: 支援全參數 (為了相容性)
- save_pet/load_pet: 檔案存取功能 (L19)

Changelog:
- v2.0.0 (L16-L20): Added Dict support, Save/Load functions
- v1.1.0 (L15): Refactored structure
- v1.0.0 (L01-L14): Initial release
"""

__version__ = "2.0.0"
__author__ = "Cyber-Pet Course Team"

import os
import math
import base64
from html import escape as _html_escape
import json
from typing import Optional, Union, Dict, Any

Number = Union[int, float]

# 嘗試匯入 IPython 環境 (Jupyter Support)
try:
    from IPython.display import display, HTML, Image  # type: ignore
    MODE = "JUPYTER"
except ImportError:
    MODE = "TERMINAL"
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

def _get_img_path(filename: str) -> Optional[str]:
    """Helper to get full path and verify existence."""
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        # Fallback for when current directory is not root
        path = os.path.join("..", "..", ASSETS_DIR, filename) 
        if not os.path.exists(path):
            return None
    return path

def _render_html(html_content: str):
    """Internal helper to render HTML content safely."""
    if MODE == "JUPYTER":
        display(HTML(html_content))
    else:
        pass

def _validate_stat(value: Any, name: str = "value") -> float:
    """Validate and convert a stat value to a finite float."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number (int or float), got {type(value).__name__}")
    num = float(value)
    if math.isnan(num) or math.isinf(num):
        raise ValueError(f"{name} must be a finite number")
    return num

def _format_stat(value: Number, name: str = "value") -> str:
    """Format a stat number for clean display (max 2 decimal places, no trailing zeros)."""
    num = _validate_stat(value, name)
    rounded = round(num, 2)
    if rounded == 0:
        return "0"
    if rounded == int(rounded):
        return str(int(rounded))
    return f"{rounded:.2f}".rstrip("0").rstrip(".")

def _clamp_percent(value: Number, max_value: Number = 100.0, name: str = "value") -> float:
    """Calculate percentage and clamp between 0.0 and 100.0."""
    num = _validate_stat(value, name)
    max_num = _validate_stat(max_value, "max_value")
    if max_num <= 0:
        return 0.0
    pct = (num / max_num) * 100.0
    return round(max(0.0, min(100.0, pct)), 2)

def _terminal_bar(value: Number, max_value: Number = 100.0, width: int = 10, name: str = "value") -> str:
    """Render a fixed-width ASCII progress bar for terminal mode."""
    pct = _clamp_percent(value, max_value, name)
    filled = int(pct // (100.0 / width))
    filled = max(0, min(width, filled))
    return "#" * filled + " " * (width - filled)

def _get_bar_color(value: Number) -> str:
    """決定狀態條的顏色"""
    if value < 20: return "#ff4444" # Red
    if value < 50: return "#ffbb33" # Orange
    return "#00C851" # Green

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

    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        img_src = f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    mood_alts = {
        "normal.png": "電子雞目前表情：平常",
        "happy.png": "電子雞目前表情：開心",
        "sad.png": "電子雞目前表情：難過",
    }
    alt_text = _html_escape(mood_alts.get(filename, f"圖片：{filename}"), quote=True)
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: {width}px; height: {width}px; overflow: hidden;">
        <img src="{img_src}" alt="{alt_text}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
    </div>
    """
    _render_html(html)

def show_book():
    """顯示魔法書 (The Grimoire)"""
    if MODE == "TERMINAL":
        print("(B) [Grimoire: pet_lib]")
        return
    print("✨ 魔法陣啟動！獲得魔法書：pet_lib ✨")
    show_image("pet_lib_book.png")

def show_pet(mood: str = "normal"):
    """顯示寵物表情 (happy, sad, normal)"""
    if MODE == "TERMINAL":
        print(f"(^.{mood}.^) [Pet is {mood}]")
        return
    filename = f"{mood}.png"
    show_image(filename)

def show_stats(name: str, hp: Number, hunger: Number, happiness: Optional[Number] = None):
    """(v1.0 Compatible) Render a beautiful HTML stat bar."""
    hp_val = _validate_stat(hp, "hp")
    hunger_val = _validate_stat(hunger, "hunger")
    happy_val = _validate_stat(happiness, "happiness") if happiness is not None else None

    if MODE == "TERMINAL":
        print(f"--- {name} ---")
        print(f"HP:       [{_terminal_bar(hp_val)}] {_format_stat(hp_val)}/100")
        print(f"Hunger:   [{_terminal_bar(hunger_val)}] {_format_stat(hunger_val)}/100")
        if happy_val is not None:
            print(f"Happy:    [{_terminal_bar(happy_val)}] {_format_stat(happy_val)}/100")
        print("----------------")
        return
    
    def _create_bar_html(label: str, value: float, reverse_color: bool = False) -> str:
        # For hunger: higher value = more hungry = red (reverse logic)
        color_value = (100 - value) if reverse_color else value
        color = _get_bar_color(color_value)
        return f"""
        <div style="margin-bottom: 5px;">
            <strong>{label}:</strong> {_format_stat(value)}/100
            <div style="background-color: #ddd; border-radius: 5px; height: 10px; width: 100%; overflow: hidden;">
                <div style="background-color: {color}; width: {_clamp_percent(value)}%; height: 100%; border-radius: 5px;"></div>
            </div>
        </div>
        """

    content_html = f"""<h3 style="margin: 0 0 10px 0; text-align: center; color: inherit;">🍱 {_html_escape(str(name))}</h3>"""
    content_html += _create_bar_html("HP", hp_val)
    content_html += _create_bar_html("Hunger", hunger_val, reverse_color=True)
    
    if happy_val is not None:
        content_html += _create_bar_html("Happiness", happy_val)

    container_html = f"""
    <div style="border: 2px solid #333; border-radius: 10px; padding: 10px; width: 324px; max-width: 100%; box-sizing: border-box; background-color: #f0f0f0; color: #333; font-family: Arial, sans-serif;">
        {content_html}
    </div>
    """
    _render_html(container_html)

def say(name: str, message: str):
    """Render a speech bubble."""
    if MODE == "TERMINAL":
        print(f"{name}: {message}")
        return

    html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <div style="font-weight: bold; margin-right: 10px; flex-shrink: 0; max-width: 40%; overflow-wrap: anywhere; text-wrap: balance;">{_html_escape(str(name))}:</div>
        <div style="background-color: #fff; color: #333; border: 2px solid #333; border-radius: 15px; padding: 8px 15px; min-width: 0; overflow-wrap: anywhere; text-wrap: balance; word-break: keep-all;">
            {_html_escape(str(message))}
        </div>
    </div>
    """
    _render_html(html)

def set_label(name: str):
    """Visualizes a name tag."""
    if MODE == "TERMINAL":
        print(f"[LABEL] Assigned Name: {name}")
        return
    html = f"""
    <div style="background-color: #FFEB3B; padding: 5px 15px; border-radius: 15px; border: 3px solid #FBC02D; display: inline-block; font-weight: bold;">
        Hello, my name is {name}
    </div>
    """
    _render_html(html)

# ==========================================
# New Features v2.0 (Dictionaries)
# ==========================================

def create_pet(name: str, hp: Number = 100, hunger: Number = 50, mood: str = "normal", **kwargs) -> Dict[str, Any]:
    """
    (v2.0 New) 創建寵物字典的便捷函式。
    
    Args:
        name: 寵物名字
        hp: 生命值 (預設 100)
        hunger: 飢餓值 (預設 50)
        mood: 心情 (預設 "normal")
        **kwargs: 其他自訂屬性 (如 happiness, attack, defense 等)
    
    Returns:
        包含寵物資料的字典
    """
    pet_data = {
        "name": name,
        "hp": hp,
        "hunger": hunger,
        "mood": mood
    }
    # 加入額外的屬性
    pet_data.update(kwargs)
    return pet_data

def show_pet_dict(pet_data: Dict[str, Any]):
    """
    (v2.0 New) 顯示寵物狀態，支援傳入 Dictionary。
    自動從字典中提取 'name', 'hp', 'hunger', 'happiness', 'mood' 等欄位。
    """
    name = pet_data.get('name', 'Unknown')
    hp = pet_data.get('hp', 0)
    hunger = pet_data.get('hunger', 0)
    happiness = pet_data.get('happiness', None) # Optional
    mood = pet_data.get('mood', 'normal')

    # 1. 顯示表情
    show_pet(mood)

    # 2. 顯示數值
    show_stats(name, hp, hunger, happiness)

def save_pet(pet_data: Dict[str, Any], filename: str = "save.json"):
    """
    (v2.0 New) 將寵物字典儲存為 JSON 檔案。
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(pet_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 寵物資料已儲存到 {filename}")
    except Exception as e:
        print(f"❌ 儲存失敗: {e}")

def load_pet(filename: str = "save.json") -> Optional[Dict[str, Any]]:
    """
    (v2.0 New) 從 JSON 檔案讀取寵物資料。
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 成功讀取 {filename}")
        return data
    except FileNotFoundError:
        print(f"⚠️ 找不到存檔 {filename}")
        return None
    except Exception as e:
        print(f"❌ 讀取失敗: {e}")
        return None
