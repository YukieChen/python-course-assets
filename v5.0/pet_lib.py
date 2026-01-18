"""
Cyber-Pet Library - 視覺化電子雞工具庫 (v5.0)

這是 Cyber-Pet 課程的核心視覺化工具庫 (The Ascension Edition)。
最終版本，準備打包成 PyPI package。

主要功能：
- celebrate: (v5.0) 慶祝動畫
- show_credits: (v5.0) 顯示工作人員名單
- show_chat_bubble: (v4.0) 顯示對話氣泡
- show_thinking: (v4.0) 模擬 AI 思考
- simulate_api: (v4.0) 模擬 API 呼叫
- set_mindset: (v4.0) 設定系統人格
- show_dashboard: (v3.0) 整合顯示玩家、敵人、戰鬥紀錄
- render_hud: (v3.0) 顯示精美 HUD
- show_animation: (v3.0) 播放動畫
- play_sound: (v3.0) 播放音效
- show_battle_log: (v3.0) 顯示戰鬥日誌
- create_pet: (v2.0) 創建寵物字典
- show_pet_dict: (v2.0) 顯示寵物
- save_pet/load_pet: (v2.0) 檔案存取

Changelog:
- v5.0.0 (L36-L40): Added celebrate() and show_credits() for the grand finale
- v4.0.0 (L31-L35): Added AI features (Chat Bubbles, Thinking, API Simulation, Mindset)
- v3.0.0 (L26-L30): Added Rich UI (Dashboard), Animation, Sound support
- v2.0.0 (L16-L25): Added Dict support, Save/Load functions, create_pet
- v1.1.0 (L15): Refactored structure
- v1.0.0 (L01-L14): Initial release
"""

__version__ = "5.0.0"
__author__ = "Cyber-Pet Course Team"

import os
import base64
import json
import time
from typing import Optional, Union, Dict, Any, List

# 嘗試匯入 IPython 環境 (Jupyter Support)
try:
    from IPython.display import display, HTML, clear_output, Audio
    MODE = "JUPYTER"
except ImportError:
    MODE = "TERMINAL"
    # Mock classes for Terminal fallback
    def display(obj): pass 
    def clear_output(wait=False): pass
    class HTML:
        def __init__(self, data): self.data = data
    class Audio:
        def __init__(self, *args, **kwargs): pass

# Constants
ASSETS_DIR = os.path.join("assets", "images")

# Sound URLs (預設音效庫)
SOUND_LIBRARY = {
    "attack": "https://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg",
    "hit": "https://commondatastorage.googleapis.com/codeskulptor-assets/week7-brrring.m4a",
    "level_up": "https://commondatastorage.googleapis.com/codeskulptor-demos/riceracer_assets/fx/win.ogg",
    "game_over": "https://commondatastorage.googleapis.com/codeskulptor-assets/Evillaugh.ogg",
    "bgm": "https://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/ateapill.ogg",
    "heal": "https://commondatastorage.googleapis.com/codeskulptor-demos/riceracer_assets/fx/engine-1.ogg"
}

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

def _get_bar_color(value: int) -> str:
    """決定狀態條的顏色"""
    if value < 20: return "#ff4444" # Red
    if value < 50: return "#ffbb33" # Orange
    return "#00C851" # Green

# ==========================================
# Core Functions (v1.0)
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

    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: {width}px; height: {width}px; overflow: hidden;">
        <img src="{img_src}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
    </div>
    """
    _render_html(html)

def show_pet(mood: str = "normal"):
    """顯示寵物表情 (happy, sad, normal)"""
    if MODE == "TERMINAL":
        print(f"(^.{mood}.^) [Pet is {mood}]")
        return
    filename = f"{mood}.png"
    show_image(filename)

def show_stats(name: str, hp: int, hunger: int, happiness: Optional[int] = None):
    """(v1.0 Compatible) Render a beautiful HTML stat bar."""
    if MODE == "TERMINAL":
        print(f"--- {name} ---")
        print(f"HP: {hp}/100")
        print(f"Hunger: {hunger}/100")
        if happiness is not None:
            print(f"Happy: {happiness}/100")
        return
    
    def _create_bar_html(label, value):
        color = _get_bar_color(value)
        return f"""
        <div style="margin-bottom: 5px;">
            <strong>{label}:</strong> {value}/100
            <div style="background-color: #ddd; border-radius: 5px; height: 10px; width: 100%;">
                <div style="background-color: {color}; width: {min(value, 100)}%; height: 100%; border-radius: 5px;"></div>
            </div>
        </div>
        """

    content_html = f"""<h3 style="margin: 0 0 10px 0; text-align: center;">🍱 {name}</h3>"""
    content_html += _create_bar_html("HP", hp)
    content_html += _create_bar_html("Hunger", hunger)
    
    if happiness is not None:
        content_html += _create_bar_html("Happiness", happiness)

    container_html = f"""
    <div style="border: 2px solid #333; border-radius: 10px; padding: 10px; width: 300px; background-color: #f0f0f0; font-family: Arial, sans-serif;">
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
        <div style="font-weight: bold; margin-right: 10px;">{name}:</div>
        <div style="background-color: #fff; border: 2px solid #333; border-radius: 15px; padding: 8px 15px;">
            {message}
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
# v2.0 Features (Dictionaries)
# ==========================================

def create_pet(name: str, hp: int = 100, hunger: int = 50, mood: str = "normal", **kwargs) -> Dict[str, Any]:
    """
    (v2.0) 創建寵物字典的便捷函式。
    
    Args:
        name: 寵物名字
        hp: 生命值 (預設 100)
        hunger: 飢餓值 (預設 50)
        mood: 心情 (預設 "normal")
        **kwargs: 其他自訂屬性 (如 happiness, attack, defense, max_hp 等)
    
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
    (v2.0) 顯示寵物狀態，支援傳入 Dictionary。
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
    (v2.0) 將寵物字典儲存為 JSON 檔案。
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(pet_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 寵物資料已儲存到 {filename}")
    except Exception as e:
        print(f"❌ 儲存失敗: {e}")

def load_pet(filename: str = "save.json") -> Optional[Dict[str, Any]]:
    """
    (v2.0) 從 JSON 檔案讀取寵物資料。
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

# ==========================================
# v3.0 Features (Rich UI, Animation, Sound)
# ==========================================

def render_hud(player: Dict[str, Any]):
    """
    (v3.0) 顯示精簡的 HUD (Heads-Up Display)。
    """
    if MODE == "TERMINAL":
        print(f"--- HUD ---")
        print(f"{player.get('name', 'Player')} | HP: {player.get('hp', 0)}/{player.get('max_hp', 100)} | Gold: {player.get('gold', 0)}")
        return
        
    name = player.get('name', 'Player')
    hp = player.get('hp', 100)
    max_hp = player.get('max_hp', 100)
    gold = player.get('gold', 0)
    
    hp_percent = min(100, max(0, int(hp / max_hp * 100)))
    hp_color = "#00C851" if hp_percent > 50 else "#ff4444"

    html = f"""
    <div style="background: rgba(0,0,0,0.8); color: white; padding: 10px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 600px;">
        <div style="font-weight: bold; font-size: 1.2em;">👤 {name}</div>
        <div style="flex-grow: 1; margin: 0 20px;">
            <div style="background: #333; height: 15px; border-radius: 10px; overflow: hidden;">
                <div style="background: {hp_color}; width: {hp_percent}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.8em; text-align: center;">HP: {hp}/{max_hp}</div>
        </div>
        <div style="color: gold;">💰 {gold} G</div>
    </div>
    """
    _render_html(html)

def show_dashboard(player: Dict[str, Any], enemy: Optional[Dict[str, Any]] = None, logs: List[str] = []):
    """
    (v3.0) 顯示完整的戰鬥儀表板。
    包含：左側玩家狀態，右側敵人狀態 (如果有)，下方戰鬥紀錄。
    """
    if MODE == "TERMINAL":
        print(f"--- DASHBOARD ---")
        print(f"Player: {player.get('name')} | HP: {player.get('hp')}")
        if enemy:
            print(f"Enemy: {enemy.get('name')} | HP: {enemy.get('hp')}")
        print("--- LOGS ---")
        for log in logs[-3:]:
            print(f"> {log}")
        return

    # Helper to create stat card HTML
    def _create_card(entity, is_enemy=False):
        if not entity: return ""
        name = entity.get('name', 'Unknown')
        hp = entity.get('hp', 100)
        max_hp = entity.get('max_hp', 100)
        mood = entity.get('mood', 'normal')
        
        # Determine image
        img_filename = f"{mood}.png"
        img_path = _get_img_path(img_filename)
        
        img_tag = ""
        if img_path:
            with open(img_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            img_tag = f'<img src="data:image/png;base64,{b64}" style="height: 80px; width: 80px; object-fit: contain;">'
        else:
             img_tag = f'<div style="height: 80px; width: 80px; background: #ccc; display: flex; align-items: center; justify-content: center;">{mood}</div>'

        hp_percent = int(hp / max_hp * 100) if max_hp > 0 else 0
        hp_color = "#ff4444" if is_enemy else "#00C851"

        border = "2px solid #ff4444" if is_enemy else "2px solid #00C851"
        bg = "rgba(50, 0, 0, 0.1)" if is_enemy else "rgba(0, 50, 0, 0.1)"

        return f"""
        <div style="border: {border}; background: {bg}; border-radius: 10px; padding: 10px; width: 45%; display: flex; align-items: center;">
            <div style="margin-right: 15px;">{img_tag}</div>
            <div style="width: 100%;">
                <div style="font-weight: bold; font-size: 1.1em; margin-bottom: 5px;">{name}</div>
                <div style="background: #444; height: 10px; border-radius: 5px; width: 100%;">
                    <div style="background: {hp_color}; width: {hp_percent}%; height: 100%; border-radius: 5px;"></div>
                </div>
                <div style="font-size: 0.8em; margin-top: 2px;">HP: {hp}/{max_hp}</div>
            </div>
        </div>
        """

    player_card = _create_card(player, is_enemy=False)
    enemy_card = _create_card(enemy, is_enemy=True) if enemy else '<div style="width: 45%;"></div>'

    # Logs Area
    log_html = ""
    for msg in reversed(logs[-5:]): # Show last 5, newest on top
        log_html += f'<div style="border-bottom: 1px solid #eee; padding: 4px;">{msg}</div>'

    dashboard = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; border: 1px solid #ccc; padding: 10px; border-radius: 10px; background: #fff;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            {player_card}
            {enemy_card}
        </div>
        <div style="background: #f9f9f9; padding: 10px; border-radius: 5px; height: 120px; overflow-y: auto; font-size: 0.9em;">
            <strong>📜 Battle Log</strong>
            {log_html}
        </div>
    </div>
    """
    
    _render_html(dashboard)

def show_battle_log(messages: List[str]):
    """
    (v3.0) 顯示戰鬥日誌視窗。
    """
    if MODE == "TERMINAL":
        print("--- BATTLE LOG ---")
        for msg in messages[-5:]:
            print(f"> {msg}")
        return
    
    log_html = ""
    for msg in reversed(messages[-10:]):  # Show last 10, newest on top
        log_html += f'<div style="border-bottom: 1px solid #eee; padding: 4px;">{msg}</div>'
    
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; border: 2px solid #333; padding: 10px; border-radius: 10px; background: #f9f9f9;">
        <div style="font-weight: bold; margin-bottom: 10px;">📜 Battle Log</div>
        <div style="background: #fff; padding: 10px; border-radius: 5px; height: 150px; overflow-y: auto; font-size: 0.9em;">
            {log_html}
        </div>
    </div>
    """
    _render_html(html)

def show_animation(frames: List[str], delay: float = 0.5):
    """
    (v3.0) 播放動畫序列。
    
    Args:
        frames: 動畫影格列表（可以是文字或圖片檔名）
        delay: 每個影格之間的延遲時間（秒）
    """
    if MODE == "TERMINAL":
        for frame in frames:
            print(frame)
            time.sleep(delay)
        return
    
    for frame in frames:
        clear_output(wait=True)
        # 判斷是圖片還是文字
        if frame.endswith('.png') or frame.endswith('.jpg'):
            show_image(frame)
        else:
            print(frame)
        time.sleep(delay)

def play_sound(sound_name: str):
    """
    (v3.0) 播放音效。
    
    Args:
        sound_name: 音效名稱 (attack, hit, level_up, game_over, bgm, heal)
    """
    if MODE == "TERMINAL":
        print(f"[SOUND] Playing: {sound_name}")
        return
    
    if sound_name not in SOUND_LIBRARY:
        print(f"⚠️ Unknown sound: {sound_name}")
        print(f"Available sounds: {', '.join(SOUND_LIBRARY.keys())}")
        return
    
    url = SOUND_LIBRARY[sound_name]
    try:
        display(Audio(url=url, autoplay=True))
    except Exception as e:
        print(f"❌ Failed to play sound: {e}")

# ==========================================
# v4.0 Features (AI & Chat)
# ==========================================

def show_chat_bubble(speaker: str, message: str, is_user: bool = False, style: str = "normal"):
    """
    (v4.0 New) 顯示聊天氣泡。
    
    Args:
        speaker: 說話者名字
        message: 訊息內容
        is_user: True 表示是使用者 (靠右對齊)，False 表示是 AI (靠左對齊)
        style: 氣泡風格 ("normal", "cute", "tech", "evil")
    """
    if MODE == "TERMINAL":
        prefix = "You" if is_user else speaker
        print(f"[{prefix}]: {message}")
        return

    align = "right" if is_user else "left"
    
    # 根據風格選擇顏色
    if is_user:
        bg_color = "#DCF8C6"  # WhatsApp green for user
    else:
        if style == "cute":
            bg_color = "#FFE5F0"  # Pink
        elif style == "tech":
            bg_color = "#E3F2FD"  # Light blue
        elif style == "evil":
            bg_color = "#FFEBEE"  # Light red
        else:
            bg_color = "#E8E8E8"  # Gray (normal)
    
    margin_left = "auto" if is_user else "0"
    margin_right = "0" if is_user else "auto"

    html = f"""
    <div style="display: flex; flex-direction: column; align-items: {f'flex-end' if is_user else 'flex-start'}; margin-bottom: 10px;">
        <div style="font-size: 0.8em; color: #666; margin-bottom: 2px; margin-{align}: 5px;">{speaker}</div>
        <div style="
            background-color: {bg_color}; 
            padding: 8px 12px; 
            border-radius: 15px; 
            max-width: 70%; 
            box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            margin-left: {margin_left};
            margin-right: {margin_right};
            position: relative;
        ">
            {message}
        </div>
    </div>
    """
    _render_html(html)

def show_thinking(prompt: str, thinking_time: float = 2.0):
    """
    (v4.0 New) 模擬 AI 思考過程。
    
    Args:
        prompt: 思考提示訊息
        thinking_time: 模擬思考秒數
    """
    if MODE == "TERMINAL":
        print(f"Thinking about: '{prompt}'...")
        time.sleep(thinking_time)
        return

    # Visualizing "Thinking"
    html_thinking = f"""
    <div style="display: flex; align-items: center; color: #888; margin-bottom: 10px;">
        <span style="margin-right: 10px;">🧠 {prompt}</span>
        <div style="
            width: 10px; height: 10px; background: #888; border-radius: 50%; 
            animation: pulse 1s infinite;"></div>
    </div>
    <style>
    @keyframes pulse {{
        0%, 100% {{ opacity: 0.3; }}
        50% {{ opacity: 1; }}
    }}
    </style>
    """
    _render_html(html_thinking)
    time.sleep(thinking_time)
    clear_output(wait=True) # Remove thinking indicator

def simulate_api(endpoint: str, data: Dict[str, Any], latency: float = 1.0):
    """
    (v4.0 New) 模擬 API 呼叫過程。
    
    Args:
        endpoint: API 端點 URL
        data: 要傳送的資料
        latency: 模擬延遲秒數
    """
    if MODE == "TERMINAL":
        print(f"POST {endpoint}")
        print(f"Data: {data}")
        time.sleep(latency)
        print("Response: 200 OK")
        return

    # Packet animation (Simplified)
    print(f"📡 Sending data to {endpoint}...")
    display(HTML(f"<div style='font-family: monospace; color: blue;'>Payload: {json.dumps(data)}</div>"))
    time.sleep(latency / 2)
    print("☁️ Processing in Cloud...")
    time.sleep(latency / 2)
    print("✅ Response received (200 OK)")

def set_mindset(personality_text: str):
    """
    (v4.0 New) 視覺化設定 System Prompt。
    
    Args:
        personality_text: 系統人格描述
    """
    if MODE == "TERMINAL":
        print(f"[SYSTEM] Updating Mindset: {personality_text[:20]}...")
        return
    
    html = f"""
    <div style="
        border: 2px dashed #9C27B0; 
        background: #F3E5F5; 
        padding: 10px; 
        border-radius: 8px; 
        color: #4A148C; 
        margin-bottom: 10px;
    ">
        <strong>🧠 System Mindset Loaded:</strong><br>
        <em>"{personality_text}"</em>
    </div>
    """
    _render_html(html)

# ==========================================
# v5.0 Features (The Ascension)
# ==========================================

def celebrate():
    """
    (v5.0 New) 播放慶祝動畫和音效。
    用於遊戲勝利、升級、或課程完成時。
    """
    if MODE == "TERMINAL":
        print("🎉 CONGRATULATIONS! 🎉")
        print("      '._==_==_=_.'     ")
        print("      .-\\:      /-.    ")
        print("     | (|:.     |) |    ")
        print("      '-|:.     |-'     ")
        print("        \\::.    /      ")
        print("         '::. .'        ")
        print("           ) (          ")
        print("         _.' '._        ")
        print("[SOUND] Playing level_up sound.")
        return
    
    # 顯示慶祝動畫
    celebration_html = """
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; font-family: Arial, sans-serif;">
        <div style="font-size: 3em; margin-bottom: 10px;">🎉</div>
        <div style="font-size: 2em; font-weight: bold; margin-bottom: 10px;">CONGRATULATIONS!</div>
        <div style="font-size: 1.2em;">You did it! 🎊</div>
        <div style="margin-top: 20px; font-size: 4em;">
            🏆
        </div>
    </div>
    """
    _render_html(celebration_html)
    
    # 播放音效
    play_sound("level_up")

def show_credits(author_name: str = "Unknown"):
    """
    (v5.0 New) 顯示遊戲工作人員名單。
    
    Args:
        author_name: 作者/導演名字
    """
    if MODE == "TERMINAL":
        lines = [
            "=== CREDITS ===",
            f"Director: {author_name}",
            "Art: Ys the Cat",
            "Engine: Python 3",
            "Library: pet_lib v5.0",
            "Based on: Cyber-Pet Course",
            "THANK YOU FOR PLAYING!"
        ]
        print("\n".join(lines))
        print("[SOUND] Playing heal sound.")
        return
    
    # 製作捲動字幕效果
    credits_html = f"""
    <div style="
        background: linear-gradient(to bottom, #1a1a2e, #16213e); 
        color: #eee; 
        padding: 30px; 
        border-radius: 10px; 
        font-family: 'Courier New', monospace;
        text-align: center;
        max-width: 500px;
        margin: 0 auto;
    ">
        <div style="font-size: 2em; margin-bottom: 20px; color: #ffd700;">✨ CREDITS ✨</div>
        <div style="font-size: 1.2em; line-height: 2em;">
            <div style="margin: 10px 0;"><strong>Director:</strong> {author_name}</div>
            <div style="margin: 10px 0;"><strong>Art:</strong> Ys the Cat 🐱</div>
            <div style="margin: 10px 0;"><strong>Engine:</strong> Python 3 🐍</div>
            <div style="margin: 10px 0;"><strong>Library:</strong> pet_lib v5.0</div>
            <div style="margin: 10px 0;"><strong>Based on:</strong> Cyber-Pet Course</div>
        </div>
        <div style="margin-top: 30px; font-size: 1.5em; color: #ffd700;">
            THANK YOU FOR PLAYING!
        </div>
        <div style="margin-top: 20px; font-size: 2em;">
            🎮 🎯 🎨
        </div>
    </div>
    """
    _render_html(credits_html)
    
    # 播放音效
    play_sound("heal")
