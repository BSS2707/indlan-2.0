#!/usr/bin/env python3
"""
IndLan 2.0 Desktop IDE
A modern, dark-themed GUI IDE with bilingual Hindi+English syntax highlighting,
line numbers, multi-tab editing, live output console, and code templates.
"""

import sys
import os
import io
import re
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font, simpledialog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import tokenize, LexError, HINDI_ALIASES, KEYWORDS
from ind_parser import parse, ParseError
from interpreter import Interpreter, IndLanRuntimeError
from py_bridge import IndLanImportError, HINDI_METHOD_ALIASES

APP_TITLE = "IndLan 2.0 IDE - Hindi + English Python Ecosystem"
VERSION = "2.0.1"

# Dark Theme Colors
THEME = {
    "bg_dark": "#1e1e2e",
    "bg_editor": "#181825",
    "bg_sidebar": "#11111b",
    "bg_terminal": "#11111b",
    "fg_text": "#cdd6f4",
    "fg_muted": "#6c7086",
    "line_num_bg": "#181825",
    "line_num_fg": "#585b70",
    "cursor_color": "#f5e0dc",
    "select_bg": "#45475a",
    "accent_cyan": "#89dceb",
    "accent_blue": "#89b4fa",
    "accent_green": "#a6e3a1",
    "accent_yellow": "#f9e2af",
    "accent_peach": "#fab387",
    "accent_red": "#f38ba8",
    "accent_purple": "#cba6f7",
    "accent_pink": "#f5c2e7",
    "border": "#313244",
}

# Snippet Templates
TEMPLATES = {
    "Data Science (Hindi)": """aayat pandas ke_roop_mein pd
aayat numpy ke_roop_mein np
aayat matplotlib.pyplot ke_roop_mein plt

se sklearn.model_selection aayat train_test_split
se sklearn.ensemble aayat RandomForestClassifier
se sklearn.metrics aayat satikta_ank

chhap("=== IndLan Data Science Pipeline ===")

maano X = np.sarni([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
maano y = np.sarni([0, 0, 0, 0, 1, 1, 1, 1])

maano X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

maano model = RandomForestClassifier(random_state=42)
model.sikhao(X_train, y_train)

maano prediction = model.bhavishyavani(X_test)
chhap("Predictions:", prediction)
chhap("Accuracy:", satikta_ank(y_test, prediction))

plt.rekha(prediction)
plt.sheershak("Prediction Results")
plt.jaal(true)
plt.dikhao()
""",

    "English Python Pipeline": """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("=== English Data Science Pipeline ===")

X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

prediction = model.predict(X_test)
print("Prediction:", prediction)
print("Accuracy:", accuracy_score(y_test, prediction))

plt.plot(prediction)
plt.title("Prediction Results")
plt.grid(true)
plt.show()
""",

    "Native CSV & JSON": """maano students = [
    {"name": "Aarav", "score": 95},
    {"name": "Diya", "score": 98},
    {"name": "Kabir", "score": 88}
]

csv_likho("students_sample.csv", students)
maano loaded_csv = csv_padho("students_sample.csv")
chhap("CSV Loaded:", loaded_csv)

maano config = {"version": "2.0.0", "language": "IndLan", "active": true}
json_likho("config_sample.json", config)
maano loaded_json = json_padho("config_sample.json")
chhap("JSON Loaded:", loaded_json)
""",

    "Classes & Functions": """varg Student {
    kaam init(naam, roll) {
        yeh.naam = naam
        yeh.roll = roll
    }

    kaam parichay() {
        chhap("Namaste, mera naam", yeh.naam, "hai aur Roll No:", yeh.roll)
    }
}

maano s1 = naya Student("Rohan", 101)
s1.parichay()
"""
}


class LineNumbers(tk.Canvas):
    """Line numbers gutter for the text editor."""
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, bg=THEME["line_num_bg"], highlightthickness=0, **kwargs)
        self.text_widget = text_widget
        self.width = 45
        self.config(width=self.width)

    def redraw(self, *args):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                self.width - 8,
                y,
                anchor="ne",
                text=linenum,
                fill=THEME["line_num_fg"],
                font=self.text_widget.cget("font"),
            )
            i = self.text_widget.index(f"{i}+1line")


class CodeEditorTab(ttk.Frame):
    """Single file editor tab with syntax highlighting and line numbers."""
    def __init__(self, parent, file_path=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.file_path = file_path
        self.is_modified = False

        self.font_size = 13
        self.code_font = font.Font(family="Consolas" if sys.platform == "win32" else "Courier", size=self.font_size)

        # Editor container
        editor_frame = tk.Frame(self, bg=THEME["bg_editor"])
        editor_frame.pack(fill="both", expand=True)

        self.text = tk.Text(
            editor_frame,
            wrap="none",
            bg=THEME["bg_editor"],
            fg=THEME["fg_text"],
            insertbackground=THEME["cursor_color"],
            selectbackground=THEME["select_bg"],
            font=self.code_font,
            undo=True,
            borderwidth=0,
            padx=8,
            pady=6,
        )

        self.line_numbers = LineNumbers(editor_frame, self.text)
        self.line_numbers.pack(side="left", fill="y")

        # Scrollbars
        v_scroll = ttk.Scrollbar(editor_frame, orient="vertical", command=self._on_vscroll)
        h_scroll = ttk.Scrollbar(self, orient="horizontal", command=self.text.xview)
        self.text.configure(xscrollcommand=h_scroll.set, yscrollcommand=self._on_text_scroll(v_scroll))

        v_scroll.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        h_scroll.pack(side="bottom", fill="x")

        # Setup syntax tags
        self._setup_tags()

        # Bind events
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<MouseWheel>", lambda e: self.line_numbers.redraw())
        self.text.bind("<Button-1>", lambda e: self.after(10, self.line_numbers.redraw))
        self.text.bind("<Tab>", self._on_tab)

        if file_path and os.path.exists(file_path):
            self.load_file(file_path)
        else:
            self.set_content(TEMPLATES["Data Science (Hindi)"])

    def _on_vscroll(self, *args):
        self.text.yview(*args)
        self.line_numbers.redraw()

    def _on_text_scroll(self, scrollbar):
        def handler(*args):
            scrollbar.set(*args)
            self.line_numbers.redraw()
        return handler

    def _on_tab(self, event):
        self.text.insert("insert", "    ")
        return "break"

    def _on_key_release(self, event=None):
        self.line_numbers.redraw()
        self.highlight_syntax()

    def _setup_tags(self):
        self.text.tag_configure("keyword_en", foreground=THEME["accent_purple"], font=self.code_font)
        self.text.tag_configure("keyword_hi", foreground=THEME["accent_pink"], font=self.code_font)
        self.text.tag_configure("method_alias", foreground=THEME["accent_cyan"], font=self.code_font)
        self.text.tag_configure("string", foreground=THEME["accent_green"])
        self.text.tag_configure("number", foreground=THEME["accent_peach"])
        self.text.tag_configure("comment", foreground=THEME["fg_muted"], font=(self.code_font.actual("family"), self.font_size, "italic"))
        self.text.tag_configure("builtin", foreground=THEME["accent_blue"])

    def highlight_syntax(self):
        content = self.text.get("1.0", "end-1c")
        for tag in ["keyword_en", "keyword_hi", "method_alias", "string", "number", "comment", "builtin"]:
            self.text.tag_remove(tag, "1.0", "end")

        # Comments
        for m in re.finditer(r"//.*$", content, re.MULTILINE):
            self.text.tag_add("comment", f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")
        for m in re.finditer(r"/\*[\s\S]*?\*/", content):
            self.text.tag_add("comment", f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")

        # Strings
        for m in re.finditer(r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', content):
            self.text.tag_add("string", f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")

        # Numbers
        for m in re.finditer(r"\b\d+(\.\d+)?\b", content):
            self.text.tag_add("number", f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")

        # English Keywords
        en_pattern = r"\b(" + "|".join(re.escape(k) for k in KEYWORDS) + r")\b"
        for m in re.finditer(en_pattern, content):
            self.text.tag_add("keyword_en", f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")

        # Hindi Keywords
        hi_pattern = r"\b(" + "|".join(re.escape(k) for k in HINDI_ALIASES.keys()) + r")\b"
        for m in re.finditer(hi_pattern, content):
            self.text.tag_add("keyword_hi", f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")

        # Method Aliases (e.g. sikhao, bhavishyavani, sarni, rekha, csv_padho)
        alias_pattern = r"\b(" + "|".join(re.escape(k) for k in HINDI_METHOD_ALIASES.keys()) + r")\b"
        for m in re.finditer(alias_pattern, content):
            self.text.tag_add("method_alias", f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")

        # Builtins
        builtins = [
            "print", "chhap", "len", "range", "str", "int", "float", "input", "aalao",
            "input_int", "number_dalao", "input_float", "decimal_dalao",
            "input_bool", "haan_na", "type", "append", "pop", "keys", "values",
            "csv_padho", "csv_likho", "csv_jodo", "csv_badlo", "csv_chhano",
            "json_padho", "json_likho", "excel_padho", "excel_likho"
        ]
        bi_pattern = r"\b(" + "|".join(re.escape(k) for k in builtins) + r")\b"
        for m in re.finditer(bi_pattern, content):
            self.text.tag_add("builtin", f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")

    def get_content(self):
        return self.text.get("1.0", "end-1c")

    def set_content(self, content):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.line_numbers.redraw()
        self.highlight_syntax()

    def load_file(self, file_path):
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.set_content(f.read())


class IndLanIDE(tk.Tk):
    """Main IndLan 2.0 IDE Window."""
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x760")
        self.configure(bg=THEME["bg_dark"])

        # Window Icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "indlan_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.current_proc = None

        self._setup_styles()
        self._build_menu()
        self._build_toolbar()
        self._build_main_layout()
        self._build_statusbar()

        self.bind("<F5>", lambda e: self.run_code())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Notebook tabs styling
        style.configure(
            "TNotebook",
            background=THEME["bg_sidebar"],
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background=THEME["bg_sidebar"],
            foreground=THEME["fg_text"],
            padding=[12, 6],
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", THEME["bg_editor"])],
            foreground=[("selected", THEME["accent_blue"])]
        )

    def _build_menu(self):
        menubar = tk.Menu(self, bg=THEME["bg_sidebar"], fg=THEME["fg_text"], activebackground=THEME["select_bg"], activeforeground=THEME["fg_text"], borderwidth=0)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=THEME["bg_sidebar"], fg=THEME["fg_text"], activebackground=THEME["select_bg"])
        file_menu.add_command(label="New File (Ctrl+N)", command=self.new_file)
        file_menu.add_command(label="Open File (Ctrl+O)", command=self.open_file)
        file_menu.add_command(label="Save File (Ctrl+S)", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Run Menu
        run_menu = tk.Menu(menubar, tearoff=0, bg=THEME["bg_sidebar"], fg=THEME["fg_text"], activebackground=THEME["select_bg"])
        run_menu.add_command(label="Run IndLan Program (F5)", command=self.run_code)
        run_menu.add_command(label="Clear Terminal", command=self.clear_terminal)
        menubar.add_cascade(label="Run", menu=run_menu)

        # Templates Menu
        tmpl_menu = tk.Menu(menubar, tearoff=0, bg=THEME["bg_sidebar"], fg=THEME["fg_text"], activebackground=THEME["select_bg"])
        for name in TEMPLATES.keys():
            tmpl_menu.add_command(label=name, command=lambda n=name: self.insert_template(n))
        menubar.add_cascade(label="Templates", menu=tmpl_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=THEME["bg_sidebar"], fg=THEME["fg_text"], activebackground=THEME["select_bg"])
        help_menu.add_command(label="IndLan Docs & CheatSheet", command=self.show_docs)
        help_menu.add_command(label="About IndLan 2.0", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _build_toolbar(self):
        toolbar = tk.Frame(self, bg=THEME["bg_sidebar"], height=38, padx=8, pady=4)
        toolbar.pack(side="top", fill="x")

        # Run Button
        run_btn = tk.Button(
            toolbar,
            text="▶ Run (F5)",
            command=self.run_code,
            bg="#2e7d32",
            fg="white",
            activebackground="#388e3c",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=2,
            cursor="hand2",
        )
        run_btn.pack(side="left", padx=4)

        # Clear Terminal
        clear_btn = tk.Button(
            toolbar,
            text="🧹 Clear Output",
            command=self.clear_terminal,
            bg=THEME["border"],
            fg=THEME["fg_text"],
            activebackground=THEME["select_bg"],
            activeforeground=THEME["fg_text"],
            relief="flat",
            font=("Segoe UI", 9),
            padx=8,
            pady=2,
            cursor="hand2",
        )
        clear_btn.pack(side="left", padx=4)

        # Template quick dropdown
        tmpl_label = tk.Label(toolbar, text="Sample Snippets:", bg=THEME["bg_sidebar"], fg=THEME["fg_muted"], font=("Segoe UI", 9))
        tmpl_label.pack(side="left", padx=(16, 4))

        self.tmpl_var = tk.StringVar(value="Load Template...")
        tmpl_dropdown = ttk.Combobox(toolbar, textvariable=self.tmpl_var, values=list(TEMPLATES.keys()), state="readonly", width=22)
        tmpl_dropdown.bind("<<ComboboxSelected>>", lambda e: self.insert_template(self.tmpl_var.get()))
        tmpl_dropdown.pack(side="left", padx=4)

        # Header Badge
        badge = tk.Label(toolbar, text="IndLan v2.0 Python Bridge Active", bg=THEME["bg_sidebar"], fg=THEME["accent_green"], font=("Segoe UI", 9, "bold"))
        badge.pack(side="right", padx=8)

    def _build_main_layout(self):
        # Vertical PanedWindow: Top = Editor Tabs, Bottom = Terminal Output
        self.paned = ttk.PanedWindow(self, orient="vertical")
        self.paned.pack(fill="both", expand=True)

        # Top Frame: Notebook for Tabs
        self.notebook = ttk.Notebook(self.paned)
        self.paned.add(self.notebook, weight=3)

        # Initial Tab
        self.add_tab("untitled.ind")

        # Bottom Frame: Terminal Console
        term_frame = tk.Frame(self.paned, bg=THEME["bg_terminal"])
        self.paned.add(term_frame, weight=1)

        term_header = tk.Frame(term_frame, bg=THEME["border"], height=24)
        term_header.pack(fill="x")
        term_title = tk.Label(term_header, text="  Terminal Output (Standard I/O)", bg=THEME["border"], fg=THEME["fg_text"], font=("Segoe UI", 9, "bold"))
        term_title.pack(side="left")

        term_content = tk.Frame(term_frame, bg=THEME["bg_terminal"])
        term_content.pack(fill="both", expand=True)

        self.terminal = tk.Text(
            term_content,
            bg=THEME["bg_terminal"],
            fg=THEME["fg_text"],
            insertbackground=THEME["cursor_color"],
            font=("Consolas" if sys.platform == "win32" else "Courier", 11),
            borderwidth=0,
            padx=8,
            pady=6,
        )
        term_scroll = ttk.Scrollbar(term_content, orient="vertical", command=self.terminal.yview)
        self.terminal.configure(yscrollcommand=term_scroll.set)

        term_scroll.pack(side="right", fill="y")
        self.terminal.pack(side="left", fill="both", expand=True)

        # Terminal text tags
        self.terminal.tag_configure("stdout", foreground=THEME["fg_text"])
        self.terminal.tag_configure("stderr", foreground=THEME["accent_red"])
        self.terminal.tag_configure("info", foreground=THEME["accent_cyan"], font=("Segoe UI", 10, "bold"))
        self.terminal.tag_configure("success", foreground=THEME["accent_green"], font=("Segoe UI", 10, "bold"))

        self.log_terminal("[IndLan 2.0 Engine Ready] Hindi + English Python ecosystem active.\n", "info")

    def _build_statusbar(self):
        self.statusbar = tk.Label(
            self,
            text=f"IndLan v{VERSION} | Ready",
            bg=THEME["bg_sidebar"],
            fg=THEME["fg_muted"],
            anchor="w",
            padx=8,
            pady=3,
            font=("Segoe UI", 9),
        )
        self.statusbar.pack(side="bottom", fill="x")

    def get_current_editor(self):
        current_tab = self.notebook.select()
        if current_tab:
            for tab in self.notebook.winfo_children():
                if str(tab) == current_tab:
                    return tab
        return None

    def add_tab(self, name, file_path=None):
        tab = CodeEditorTab(self.notebook, file_path=file_path)
        self.notebook.add(tab, text=f"  {name}  ")
        self.notebook.select(tab)
        return tab

    def new_file(self):
        self.add_tab("untitled.ind")

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("IndLan Files", "*.ind"), ("All Files", "*.*")]
        )
        if path:
            name = os.path.basename(path)
            self.add_tab(name, file_path=path)

    def save_file(self):
        editor = self.get_current_editor()
        if not editor:
            return
        if editor.file_path:
            with open(editor.file_path, "w", encoding="utf-8") as f:
                f.write(editor.get_content())
            self.statusbar.config(text=f"Saved: {editor.file_path}")
        else:
            self.save_file_as()

    def save_file_as(self):
        editor = self.get_current_editor()
        if not editor:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".ind",
            filetypes=[("IndLan Files", "*.ind"), ("All Files", "*.*")]
        )
        if path:
            editor.file_path = path
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.get_content())
            idx = self.notebook.index("current")
            self.notebook.tab(idx, text=f"  {os.path.basename(path)}  ")
            self.statusbar.config(text=f"Saved: {path}")

    def insert_template(self, tmpl_name):
        if tmpl_name in TEMPLATES:
            editor = self.get_current_editor()
            if editor:
                editor.set_content(TEMPLATES[tmpl_name])
                self.statusbar.config(text=f"Loaded template: {tmpl_name}")

    def clear_terminal(self):
        self.terminal.delete("1.0", "end")

    def log_terminal(self, text, tag="stdout"):
        self.terminal.insert("end", text, tag)
        self.terminal.see("end")

    def run_code(self):
        editor = self.get_current_editor()
        if not editor:
            return

        source = editor.get_content()
        self.statusbar.config(text="Running IndLan code...")
        self.log_terminal(f"\n--- Running IndLan Program ---\n", "info")

        def worker():
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            out_buf = io.StringIO()
            err_buf = io.StringIO()
            sys.stdout = out_buf
            sys.stderr = err_buf
            success = False

            def ide_input(prompt=""):
                # Flush existing stdout buffer to terminal UI first
                curr_out = out_buf.getvalue()
                if curr_out:
                    self.after(0, lambda t=curr_out: self.log_terminal(t, "stdout"))
                    out_buf.seek(0)
                    out_buf.truncate(0)

                res = [None]
                evt = threading.Event()

                def ask():
                    try:
                        p_text = prompt if prompt else "IndLan Input:"
                        val = simpledialog.askstring("IndLan Input", p_text, parent=self)
                        res[0] = val if val is not None else ""
                        self.log_terminal(f"{prompt}{res[0]}\n", "stdout")
                    finally:
                        evt.set()

                self.after(0, ask)
                evt.wait()
                return res[0]
            try:
                tokens = tokenize(source)
                program = parse(tokens)
                interp = Interpreter(debug=True, input_func=ide_input)
                interp.run(program)
                success = True
            except LexError as e:
                err_buf.write(str(e) + "\n")
            except ParseError as e:
                err_buf.write(str(e) + "\n")
            except IndLanImportError as e:
                err_buf.write(str(e) + "\n")
            except IndLanRuntimeError as e:
                err_buf.write(str(e) + "\n")
            except Exception as e:
                err_buf.write(f"[IndLan Runtime Error] {e}\n")
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

            output_text = out_buf.getvalue()
            error_text = err_buf.getvalue()

            def update_ui():
                if output_text:
                    self.log_terminal(output_text, "stdout")
                if error_text:
                    self.log_terminal(error_text, "stderr")
                if success:
                    self.log_terminal("✔ Execution completed successfully.\n", "success")
                    self.statusbar.config(text="Execution Finished (Success)")
                else:
                    self.log_terminal("✖ Program exited with error.\n", "stderr")
                    self.statusbar.config(text="Execution Finished (With Errors)")

            self.after(0, update_ui)

        threading.Thread(target=worker, daemon=True).start()

    def show_docs(self):
        docs_msg = (
            "IndLan 2.0 CheatSheet:\n\n"
            "Keywords (Hindi / English):\n"
            "• aayat / import  (e.g. aayat pandas ke_roop_mein pd)\n"
            "• se / from      (e.g. se sklearn.ensemble aayat RandomForestClassifier)\n"
            "• maano / let    (e.g. maano data = pd.csv_padho('file.csv'))\n"
            "• kaam / fun     (e.g. kaam jodo(a, b) { vapas a + b })\n"
            "• agar / if, nahito / else, jabtak / while, pratyek / for\n\n"
            "User-Input Functions:\n"
            "• aalao(prompt) / input(prompt)         -> string\n"
            "• number_dalao(prompt) / input_int(prompt) -> integer\n"
            "• decimal_dalao(prompt) / input_float(prompt) -> float\n"
            "• haan_na(prompt) / input_bool(prompt)   -> bool (sahi/galat)\n\n"
            "Universal ML Aliases:\n"
            "• model.sikhao(X, y)          -> fit\n"
            "• model.bhavishyavani(X)      -> predict\n"
            "• np.sarni([1, 2, 3])         -> array\n"
            "• pd.csv_padho('data.csv')    -> read_csv\n"
            "• plt.rekha(x, y), plt.dikhao() -> plot, show\n"
        )
        messagebox.showinfo("IndLan 2.0 Documentation", docs_msg)

    def show_about(self):
        about_msg = (
            "IndLan 2.0 IDE\n"
            "Hindi + English Programming Interface for Python Ecosystem\n\n"
            "Author: Bhavya S Solanki\n"
            "Version: 2.0.0\n"
            "License: MIT\n"
        )
        messagebox.showinfo("About IndLan 2.0", about_msg)


def main():
    app = IndLanIDE()
    app.mainloop()


if __name__ == "__main__":
    main()
