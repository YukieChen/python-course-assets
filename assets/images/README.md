# `assets/images`（本機）

- **egg.png / happy.png / normal.png / sad.png**（情緒圖）：與成長圖同一 JRPG 角色系譜；來源見 `assets/mood_jrpg_sources/mood_src_*.png`（滿版 `#5C6B6A`），以 `tools/remove_bg.py` 轉透明後覆寫本目錄。**`egg.png` 為完整未裂開的蛋**（情緒／一般展示用）。
- **growth_*.png**：Issue [#2](https://github.com/YukieChen/course/issues/2) **JRPG 像素風**；來源為 **#5C6B6A 純色底**（見 [04_cyber-pet-chroma-key-source.md](../design/04_cyber-pet-chroma-key-source.md)），`tools/finalize_jrpg_growth_png.py` **色鍵 + 邊緣剝離**；輸出為 **alpha 緊裁切** 後尺寸（**不**固定 800×800），與 `pet_lib.show_growth_stage()` 檔名一致。**`growth_egg.png` 為有裂紋、即將孵化之蛋**（成長敘事 L01），與 `egg.png` 不同。
- **growth_duo_scene.png**（選用）：**雙人並立**插圖——**兩隻皆為 tween 神獸型態**（左薄荷主色、右咖啡色變體，僅配色差異）；**非** `show_growth_stage` 階段檔名，來源為 `assets/growth_jrpg_sources/growth_src_duo_scene.png`，以 `tools/remove_bg.py` 轉透明。
- 課程執行時若無本機檔，仍由 `pet_setup.py` 自 CDN 下載；上課環境以 **python-course-assets** 為準。

預覽說明：[docs/design/02_growth-stages-preview.md](../../docs/design/02_growth-stages-preview.md)  
色鍵與轉檔：[docs/design/04_cyber-pet-chroma-key-source.md](../../docs/design/04_cyber-pet-chroma-key-source.md)（`tools/finalize_jrpg_growth_png.py`）；簡易去背可選 `tools/remove_bg.py`。
