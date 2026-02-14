import os
import sys
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

# HELPER: Directs the app to look inside the EXE's temporary folder for images
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PyxelText:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyxel Text")
        self.root.geometry("1150x850")
        self.root.configure(bg="#1e272e")

        # UPDATED: Path helper for icon
        try:
            self.root.iconbitmap(resource_path("mylogo.ico"))
        except:
            pass

        self.project_path = ""
        self.output_path = ""
        self.master_registry = {}
        self.active_rel_paths = []
        self.text_widgets = []

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#1e272e", pady=10)
        header.pack(side=tk.TOP, fill=tk.X)

        # UPDATED: Path helper for logo
        try:
            img_p = resource_path("mylogo.png")
            img = Image.open(img_p)
            img = img.resize((128, 128), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(header, image=self.logo_img, bg="#1e272e").pack(side=tk.LEFT, padx=20)
        except:
            tk.Label(header, text="[Logo]", fg="white", bg="#1e272e").pack(side=tk.LEFT, padx=20)

        btn_container = tk.Frame(header, bg="#1e272e")
        btn_container.pack(side=tk.LEFT, padx=10)
        tk.Label(btn_container, text="PYXEL TEXT", font=("Impact", 24), fg="#44bd32", bg="#1e272e").pack(anchor="w")

        row = tk.Frame(btn_container, bg="#1e272e")
        row.pack(fill=tk.X)
        tk.Button(row, text="📁 Scene Folder", command=self.load_project, bg="#353b48", fg="white", relief="flat").pack(
            side=tk.LEFT, padx=2)
        tk.Button(row, text="🎯 Output Folder", command=self.set_output_folder, bg="#353b48", fg="white",
                  relief="flat").pack(side=tk.LEFT, padx=2)
        self.export_btn = tk.Button(row, text="🚀 EXPORT ALL", state=tk.DISABLED, command=self.export_project,
                                    bg="#44bd32", fg="white", font=("Arial", 10, "bold"), relief="flat")
        self.export_btn.pack(side=tk.LEFT, padx=10)

        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#1e272e", sashwidth=4)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.paned, selectmode="browse")
        self.tree.bind("<<TreeviewSelect>>", self.on_scene_select)
        self.paned.add(self.tree)

        self.editor_frame = tk.Frame(self.paned, bg="#dcdde1")
        self.canvas = tk.Canvas(self.editor_frame, bg="#dcdde1", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.editor_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_content = tk.Frame(self.canvas, bg="#dcdde1")

        self.scrollable_content.bind("<Configure>",
                                     lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.paned.add(self.editor_frame)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

    def load_project(self):
        path = filedialog.askdirectory()
        if path:
            self.project_path = path
            self.master_registry = {}
            for i in self.tree.get_children(): self.tree.delete(i)
            for folder in sorted(os.listdir(self.project_path)):
                if os.path.isdir(os.path.join(self.project_path, folder)):
                    self.tree.insert("", "end", text=folder, values=(os.path.join(self.project_path, folder),))
            self.check_ready()

    def set_output_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path = path
            self.check_ready()

    def check_ready(self):
        if self.project_path and self.output_path: self.export_btn.config(state=tk.NORMAL)

    def sync_ui_to_registry(self):
        for item in self.text_widgets:
            content = item['widget'].get("1.0", "end-1c")
            if item['key'] is not None:
                item['data_ref'][item['key']] = content
            else:
                item['data_ref'][item['index']] = content

    def on_scene_select(self, event):
        if not self.tree.selection(): return
        self.sync_ui_to_registry()
        selected_item = self.tree.selection()[0]
        scene_root_path = self.tree.item(selected_item, "values")[0]
        self.active_rel_paths = []
        for root, _, files in os.walk(scene_root_path):
            for file in files:
                if file.endswith(".gbsres") and not file.endswith(".bak"):
                    rel_p = os.path.relpath(os.path.join(root, file), self.project_path)
                    self.active_rel_paths.append(rel_p)
                    if rel_p not in self.master_registry:
                        with open(os.path.join(self.project_path, rel_p), 'r', encoding='utf-8') as f:
                            self.master_registry[rel_p] = json.load(f)
        self.render_editor()

    def find_dialogues_recursive(self, data, dialogues_list):
        if isinstance(data, list):
            for item in data: self.find_dialogues_recursive(item, dialogues_list)
        elif isinstance(data, dict):
            cmd = data.get("command")
            if cmd in ["EVENT_TEXT", "EVENT_MENU", "EVENT_CHOICE"]:
                dialogues_list.append(data)
            for value in data.values():
                if isinstance(value, (dict, list)): self.find_dialogues_recursive(value, dialogues_list)

    def render_editor(self):
        for widget in self.scrollable_content.winfo_children(): widget.destroy()
        self.text_widgets = []

        for rel_p in self.active_rel_paths:
            data_obj = self.master_registry[rel_p]
            events = []
            self.find_dialogues_recursive(data_obj, events)
            if not events: continue

            tk.Label(self.scrollable_content, text=f"📄 {rel_p}", font=("Arial", 10, "bold"), bg="#dcdde1",
                     fg="#2f3640").pack(anchor="w", padx=20, pady=10)

            for event in events:
                cmd = event.get("command")
                args = event.get("args", {})
                frame = tk.Frame(self.scrollable_content, bg="white", padx=10, pady=10, highlightthickness=1,
                                 highlightbackground="#bdc3c7")
                frame.pack(fill=tk.X, padx=20, pady=5)

                tk.Label(frame, text=f"Type: {cmd.replace('EVENT_', '')}", font=("Arial", 8, "bold"), bg="white",
                         fg="#44bd32").pack(anchor="w")

                if cmd == "EVENT_TEXT":
                    text_array = args.get('text', [])
                    for i, snippet in enumerate(text_array):
                        self.add_text_box(frame, f"Dialogue Page {i + 1}", text_array, i)

                elif cmd == "EVENT_MENU":
                    num_items = args.get('items', 1)
                    for i in range(1, 9):
                        opt_key = f"option{i}"
                        if opt_key in args and (i <= num_items or args[opt_key] != ""):
                            self.add_text_box(frame, f"Menu Option {i}", args, None, key=opt_key)

                elif cmd == "EVENT_CHOICE":
                    self.add_text_box(frame, "Choice (True)", args, None, key='trueText')
                    self.add_text_box(frame, "Choice (False)", args, None, key='falseText')

    def add_text_box(self, parent, label, data_ref, index, key=None):
        tk.Label(parent, text=label, bg="white", font=("Arial", 7), fg="#7f8c8d").pack(anchor="w")
        txt = tk.Text(parent, height=2, font=("Consolas", 11), undo=True)
        val = data_ref[key] if key else data_ref[index]
        txt.insert("1.0", val)
        txt.pack(fill=tk.X, pady=(0, 5))
        self.text_widgets.append({'widget': txt, 'data_ref': data_ref, 'index': index, 'key': key})

    def export_project(self):
        self.sync_ui_to_registry()
        try:
            dest_root = os.path.join(self.output_path, os.path.basename(self.project_path))
            if os.path.exists(dest_root): shutil.rmtree(dest_root)
            shutil.copytree(self.project_path, dest_root)
            for rel_path, modified_data in self.master_registry.items():
                target_file = os.path.join(dest_root, rel_path)
                for p in [target_file, target_file + ".bak"]:
                    with open(p, 'w', encoding='utf-8') as f:
                        json.dump(modified_data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Pyxel Text", f"Export Complete!\nSaved to: {dest_root}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PyxelText(root)
    root.mainloop()