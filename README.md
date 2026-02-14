# 🚀 Pyxel Text

**Pyxel Text** is a specialized, lightweight dialogue and menu editor designed specifically for **GB Studio** projects. It allows developers to quickly modify text, choice events, and menu labels across multiple scenes without opening the GB Studio engine.



## ✨ Key Features

* **Multi-Scene Editing:** Load entire scene folders and jump between them. Edits are cached in a Master Registry until you are ready to export.
* **Comprehensive Event Support:**
    * `EVENT_TEXT`: Edit dialogue pages.
    * `EVENT_MENU`: Modify menu option labels (supports modern and legacy GB Studio structures).
    * `EVENT_CHOICE`: Quickly update True/False choice strings.
* **Safe Exporting:** Creates a twin of your project folder in a designated output directory, ensuring your original source files remain untouched.
* **Branded Interface:** Optimized dark-mode UI with a clean, focused editor workspace.

## 🛠️ How to Use

1.  **Select Scene Folder:** Point the app to your GB Studio project's `assets/scenes` folder.
2.  **Set Output Folder:** Choose where you want the modified version of your project to be saved.
3.  **Edit Text:** Select a scene from the left sidebar and modify the text in the right-hand editor.
4.  **Export All:** Click **🚀 EXPORT ALL** to generate the new project structure with your updated text.

## 📦 Requirements (For Source)

If running from source, you will need:
* Python 3.x
* Pillow (`pip install pillow`)

## 🏗️ Building the Executable

To bundle the application yourself, use the following PyInstaller command:

```bash
pyinstaller --noconfirm --onefile --windowed --icon "mylogo.ico" --add-data "mylogo.png;." --add-data "mylogo.ico;." --name "PyxelText" "Pyxel_Text.py"
