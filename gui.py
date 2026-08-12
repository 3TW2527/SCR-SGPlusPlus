import logging
import sys
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import keyboard
import tomli_w

COMMON_SCANCODES = {
    2: "1", 3: "2", 4: "3", 5: "4", 6: "5", 7: "6", 8: "7", 9: "8", 10: "9", 11: "0",
    16: "Q", 17: "W", 18: "E", 19: "R", 20: "T", 21: "Y", 22: "U", 23: "I", 24: "O", 25: "P",
    30: "A", 31: "S", 32: "D", 33: "F", 34: "G", 35: "H", 36: "J", 37: "K", 38: "L",
    44: "Z", 45: "X", 46: "C", 47: "V", 48: "B", 49: "N", 50: "M",
    59: "F1", 60: "F2", 61: "F3", 62: "F4", 63: "F5", 64: "F6", 65: "F7", 66: "F8", 67: "F9", 68: "F10", 87: "F11", 88: "F12",
    71: "Numpad 7", 72: "Numpad 8", 73: "Numpad 9",
    75: "Numpad 4", 76: "Numpad 5", 77: "Numpad 6",
    79: "Numpad 1", 80: "Numpad 2", 81: "Numpad 3", 74: "Numpad 0",
    28: "Enter", 57: "Space", 1: "Esc", 14: "Backspace", 15: "Tab",
}


def get_key_friendly_name(key_val) -> str:
    """Return a human-readable string representation of a keybind or scancode."""
    if isinstance(key_val, int) or (isinstance(key_val, str) and key_val.isdigit()):
        sc = int(key_val)
        if sc in COMMON_SCANCODES:
            return f"{COMMON_SCANCODES[sc]} (Scancode {sc})"
        return f"Scancode {sc}"
    return str(key_val)


class KeyCaptureButton(ttk.Button):
    def __init__(self, parent, entry_widget, label_widget=None, **kwargs):
        super().__init__(parent, text="Press Key", command=self.start_capture, **kwargs)
        self.entry_widget = entry_widget
        self.label_widget = label_widget
        self.is_capturing = False

    def start_capture(self):
        if self.is_capturing:
            return
        self.is_capturing = True
        self.config(text="Listening...")

        def _capture_thread():
            try:
                while True:
                    event = keyboard.read_event(suppress=False)
                    if event.event_type == keyboard.KEY_DOWN:
                        scancode = event.scan_code
                        key_name = event.name

                        if scancode and scancode > 0:
                            new_val = str(scancode)
                        else:
                            new_val = key_name

                        def _update_ui():
                            self.entry_widget.delete(0, tk.END)
                            self.entry_widget.insert(0, new_val)
                            if self.label_widget:
                                self.label_widget.config(text=get_key_friendly_name(new_val))
                            self.config(text="Press Key")
                            self.is_capturing = False

                        self.entry_widget.after(0, _update_ui)
                        break
            except Exception as e:
                logging.error(f"Key capture error: {e}")
                def _reset_ui():
                    self.config(text="Press Key")
                    self.is_capturing = False
                self.entry_widget.after(0, _reset_ui)

        threading.Thread(target=_capture_thread, daemon=True).start()


class ShortcutDialog(tk.Toplevel):
    def __init__(self, parent, title="Shortcut Message", description="", keybind="", message=""):
        super().__init__(parent)
        self.title(title)
        self.geometry("520x320")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = None

        ttk.Label(self, text="Description:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.desc_entry = ttk.Entry(self, width=30)
        self.desc_entry.insert(0, description)
        self.desc_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(self, text="Keybind:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        key_frame = ttk.Frame(self)
        key_frame.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.key_entry = ttk.Entry(key_frame, width=15)
        self.key_entry.insert(0, str(keybind))
        self.key_entry.pack(side="left", padx=(0, 5))

        self.info_label = ttk.Label(key_frame, text=get_key_friendly_name(keybind), foreground="blue")
        self.info_label.pack(side="left", padx=5)

        self.cap_btn = KeyCaptureButton(key_frame, self.key_entry, self.info_label)
        self.cap_btn.pack(side="left", padx=5)

        ttk.Label(self, text="Message to Copy:").grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        self.msg_text = tk.Text(self, width=35, height=6, wrap="word")
        self.msg_text.insert("1.0", message)
        self.msg_text.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Save", command=self.on_save).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", padx=10)

        self.key_entry.bind("<KeyRelease>", self.update_key_name)
        self.center_window(parent)

    def update_key_name(self, event=None):
        val = self.key_entry.get().strip()
        self.info_label.config(text=get_key_friendly_name(val))

    def center_window(self, parent):
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        w = self.winfo_width()
        h = self.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{x}+{y}")

    def on_save(self):
        desc = self.desc_entry.get().strip()
        keybind_raw = self.key_entry.get().strip()
        msg = self.msg_text.get("1.0", tk.END).strip()

        if not desc or not keybind_raw or not msg:
            messagebox.showerror("Error", "All fields are required!", parent=self)
            return

        if keybind_raw.isdigit():
            keybind = int(keybind_raw)
        else:
            keybind = keybind_raw

        self.result = {
            "description": desc,
            "keybind": keybind,
            "message": msg,
        }
        self.destroy()


class ConfigGUI:
    def __init__(self, root, config_data, on_save_callback=None):
        self.root = root
        self.config_data = dict(config_data)
        self.on_save_callback = on_save_callback

        self.root.title("SG+ Configuration Manager")
        self.root.geometry("680x580")
        self.root.resizable(True, True)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_general_tab()
        self.create_keybinds_tab()
        self.create_shortcuts_tab()

        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=10)

        exit_app_btn = ttk.Button(bottom_frame, text="Exit Entire App", command=self.quit_entire_app)
        exit_app_btn.pack(side="left", padx=5)

        save_btn = ttk.Button(bottom_frame, text="Save & Apply Config", command=self.save_config)
        save_btn.pack(side="right", padx=5)

        close_btn = ttk.Button(bottom_frame, text="Close Settings", command=self.root.destroy)
        close_btn.pack(side="right", padx=5)

    def quit_entire_app(self):
        if messagebox.askyesno("Exit SG+", "Are you sure you want to quit SG+ entirely?"):
            sys.exit(0)

    def create_general_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="General Settings")

        self.vars = {}

        ttk.Label(tab, text="Average FPS:").grid(row=0, column=0, sticky="w", padx=15, pady=10)
        self.vars["average_fps"] = tk.IntVar(value=self.config_data.get("average_fps", 30))
        fps_spin = ttk.Spinbox(tab, from_=1, to=240, textvariable=self.vars["average_fps"], width=10)
        fps_spin.grid(row=0, column=1, sticky="w", padx=15, pady=10)

        bool_settings = [
            ("enable_status_indicator", "Enable Status Indicator Overlay (SG+ / SG-)"),
            ("auto_disable_on_chat", "Auto Disable Macro when Chat Opening Key Pressed"),
            ("auto_enable_on_enter", "Auto Enable Macro when Enter Pressed"),
            ("enable_update_checker", "Enable Automatic Update Checker"),
            ("debug_mode_enabled", "Enable Debug Logging"),
            ("onboard_msg", "Display Onboarding Welcome Message on Startup"),
        ]

        row = 1
        for key, text in bool_settings:
            val = self.config_data.get(key, True)
            self.vars[key] = tk.BooleanVar(value=val)
            cb = ttk.Checkbutton(tab, text=text, variable=self.vars[key])
            cb.grid(row=row, column=0, columnspan=2, sticky="w", padx=15, pady=5)
            row += 1

    def create_keybinds_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Keybinds")

        keybinds = self.config_data.get("keybinds", {})

        bind_fields = [
            ("set_signal_danger", "Set Danger Aspect:"),
            ("set_signal_caution", "Set Caution Aspect:"),
            ("set_signal_proceed", "Set Proceed Aspect:"),
            ("toggle_signal_camera", "Toggle Signal Camera:"),
            ("quit_camera_view", "Quit Camera View:"),
            ("toggle_macro", "Toggle Macro On/Off:"),
            ("toggle_signal_rollback", "Toggle Signal Rollback:"),
            ("toggle_signal_sidemenu", "Toggle Signal Sidemenu:"),
        ]

        self.keybind_entries = {}
        self.keybind_labels = {}
        row = 0
        for key, label_text in bind_fields:
            ttk.Label(tab, text=label_text).grid(row=row, column=0, sticky="w", padx=15, pady=5)

            f = ttk.Frame(tab)
            f.grid(row=row, column=1, sticky="w", padx=15, pady=5)

            val = keybinds.get(key, "")
            entry = ttk.Entry(f, width=12)
            entry.insert(0, str(val))
            entry.pack(side="left", padx=(0, 5))

            name_lbl = ttk.Label(f, text=get_key_friendly_name(val), foreground="blue")
            name_lbl.pack(side="left", padx=5)

            btn = KeyCaptureButton(f, entry, name_lbl)
            btn.pack(side="left", padx=5)

            entry.bind("<KeyRelease>", lambda e, en=entry, nl=name_lbl: nl.config(text=get_key_friendly_name(en.get().strip())))

            self.keybind_entries[key] = entry
            self.keybind_labels[key] = name_lbl
            row += 1

        ttk.Label(tab, text="Warning Keys (comma-separated):").grid(row=row, column=0, sticky="w", padx=15, pady=5)
        warn_keys = keybinds.get("warning_keys", ["/", "'", "`"])
        warn_str = ", ".join(str(k) for k in warn_keys)
        self.warn_entry = ttk.Entry(tab, width=30)
        self.warn_entry.insert(0, warn_str)
        self.warn_entry.grid(row=row, column=1, sticky="w", padx=15, pady=5)

    def create_shortcuts_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Shortcut Messages (Zones & Custom)")

        top_info = ttk.Label(
            tab,
            text="Manage shortcut messages to copy to clipboard on keybind press. Click 'Press Key' when editing to record any key press automatically.",
            wraplength=600,
        )
        top_info.pack(fill="x", padx=10, pady=5)

        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("description", "keybind", "message")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("description", text="Description")
        self.tree.heading("keybind", text="Keybind")
        self.tree.heading("message", text="Message to Copy")

        self.tree.column("description", width=140)
        self.tree.column("keybind", width=160)
        self.tree.column("message", width=280)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.shortcuts = list(self.config_data.get("shortcut_messages", []))
        self.populate_shortcuts_tree()

        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add_shortcut).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit", command=self.edit_shortcut).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_shortcut).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Move Up", command=self.move_up).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Move Down", command=self.move_down).pack(side="left", padx=5)

    def populate_shortcuts_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, sc in enumerate(self.shortcuts):
            kb_display = get_key_friendly_name(sc.get("keybind", ""))
            self.tree.insert(
                "",
                "end",
                iid=str(idx),
                values=(sc.get("description", ""), kb_display, sc.get("message", "")),
            )

    def add_shortcut(self):
        dlg = ShortcutDialog(self.root, title="Add Shortcut Message")
        self.root.wait_window(dlg)
        if dlg.result:
            self.shortcuts.append(dlg.result)
            self.populate_shortcuts_tree()

    def edit_shortcut(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a shortcut message to edit.")
            return
        idx = int(selected[0])
        item = self.shortcuts[idx]
        dlg = ShortcutDialog(
            self.root,
            title="Edit Shortcut Message",
            description=item.get("description", ""),
            keybind=item.get("keybind", ""),
            message=item.get("message", ""),
        )
        self.root.wait_window(dlg)
        if dlg.result:
            self.shortcuts[idx] = dlg.result
            self.populate_shortcuts_tree()

    def delete_shortcut(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a shortcut message to delete.")
            return
        idx = int(selected[0])
        if messagebox.askyesno("Confirm Delete", f"Delete shortcut '{self.shortcuts[idx].get('description')}'?"):
            del self.shortcuts[idx]
            self.populate_shortcuts_tree()

    def move_up(self):
        selected = self.tree.selection()
        if not selected:
            return
        idx = int(selected[0])
        if idx > 0:
            self.shortcuts[idx - 1], self.shortcuts[idx] = self.shortcuts[idx], self.shortcuts[idx - 1]
            self.populate_shortcuts_tree()
            self.tree.selection_set(str(idx - 1))

    def move_down(self):
        selected = self.tree.selection()
        if not selected:
            return
        idx = int(selected[0])
        if idx < len(self.shortcuts) - 1:
            self.shortcuts[idx + 1], self.shortcuts[idx] = self.shortcuts[idx], self.shortcuts[idx + 1]
            self.populate_shortcuts_tree()
            self.tree.selection_set(str(idx + 1))

    def save_config(self):
        for key in self.vars:
            self.config_data[key] = self.vars[key].get()

        if "keybinds" not in self.config_data:
            self.config_data["keybinds"] = {}

        for key, entry in self.keybind_entries.items():
            val_str = entry.get().strip()
            if val_str.isdigit():
                self.config_data["keybinds"][key] = int(val_str)
            else:
                self.config_data["keybinds"][key] = val_str

        warn_str = self.warn_entry.get().strip()
        warn_list = [w.strip() for w in warn_str.split(",") if w.strip()]
        self.config_data["keybinds"]["warning_keys"] = warn_list

        self.config_data["shortcut_messages"] = self.shortcuts

        try:
            with open("config.toml", "wb") as f:
                tomli_w.dump(self.config_data, f)
            logging.info("Configuration saved to config.toml")
            messagebox.showinfo("Success", "Configuration saved successfully!")
            if self.on_save_callback:
                self.on_save_callback(self.config_data)
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")


def open_config_window(parent_root, config_data, on_save_callback=None):
    win = tk.Toplevel(parent_root)
    ConfigGUI(win, config_data, on_save_callback)
    return win
