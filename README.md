# 🚀 Pyxel Text

**Pyxel Text** is a specialized, standalone editor designed for **GB Studio** developers. It provides a fast, distraction-free way to edit game dialogue, menus, and choice events across multiple scenes simultaneously without needing to open the full GB Studio engine.

### Why use Pyxel Text?
Writing dialogue in GB Studio can be slow when jumping between many scenes. Pyxel Text extracts all text-related events into a clean list, letting you focus on the writing and localization.

---

## ✨ Features

* **Zero Setup:** No Python or GB Studio installation required. Just run the `.exe`.
* **Multi-Scene Sessions:** Edit Scene A, switch to Scene B, and your changes in Scene A are saved in memory until you export.
* **Deep Text Extraction:**
    * **Dialogue:** Edit all standard text boxes.
    * **Menus:** Modify option labels (e.g., "Yes/No", "Buy/Sell").
    * **Choices:** Update True/False choice prompts.
* **Non-Destructive:** The tool never overwrites your original source files. It creates a "modified clone" of your project folder.

---

## 🛠️ How to Use

1.  **Scene Folder:** Click the button and select your project's `assets/scenes` folder.
2.  **Output Folder:** Select where you want the modified version of your project to be saved (e.g., your Desktop).
3.  **Edit:** Select a scene from the left sidebar. All dialogues and menus will appear on the right.
4.  **Export:** Hit **🚀 EXPORT ALL**. The app will create a copy of your scenes folder with all your new text injected into the `.gbsres` files.
5.    replace your previous scene folder with the exported one
---

## ⚠️ Important Note (Windows Defender)

Because this is an independent executable not signed by a major publisher, Windows may show a blue popup saying **"Windows protected your PC."**

**To run the app:**
1. Click **More Info**.
2. Click **Run Anyway**.

---

Additional warning: do NOT have GB studio on when you replace the scene files; FIRST replace the scene folder, THEN turn on GBStudio.

## 📦 Download
Check the **Releases** section on the right to download the latest `PyxelText.zip`.
