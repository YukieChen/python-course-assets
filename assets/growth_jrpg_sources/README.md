# 成長圖來源（`growth_src_*.png`）

美術在 **Aseprite／Photoshop 等**手繪五階段，**整張背景僅** `#5C6B6A`（見 [docs/design/04_cyber-pet-chroma-key-source.md](../../docs/design/04_cyber-pet-chroma-key-source.md)）；**勿**用本 repo 已移除的程式自動生圖。

## 檔名

| 檔名 | 對應 stage |
|------|------------|
| `growth_src_egg.png` | `egg` |
| `growth_src_hatchling.png` | `hatchling` |
| `growth_src_juvenile.png` | `juvenile` |
| `growth_src_tween.png` | `tween` |
| `growth_src_partner.png` | `partner` |
| `growth_src_duo_scene.png` | （選用，非 stage）雙人並立：**皆 tween 型態**（非 tween+juvenile 混階） |

## 轉成課程用透明 PNG

於 Cyber-Pet 根目錄：

```bash
python3 tools/finalize_jrpg_growth_png.py
```

輸出至 `assets/images/growth_*.png`（緊裁切、透明底）。預設為**邊緣 flood 色鍵**（只刪與畫布邊界連通的背景），避免主體內與底色相近的陰影被誤刪。參數見 `finalize_jrpg_growth_png.py --help`。

雙人並立（選用）：

```bash
python3 tools/remove_bg.py assets/growth_jrpg_sources/growth_src_duo_scene.png -o assets/images/growth_duo_scene.png
```

若邊緣需額外清理，可視情況使用 `tools/remove_bg.py`（與 finalize 同邏輯；複雜去背請在美術軟體完成）。
