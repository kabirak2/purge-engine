import tkinter as tk

from core.canon import Canon
from core.filesystem import save_project
from core.hotreload import HotReloadManager

from ui.project_panel import ProjectPanel
from ui.canon_panel import CanonPanel
from ui.rule_editor import RuleEditor
from ui.validation_panel import ValidationPanel
from ui.timeline_panel import TimelinePanel
from ui.versemind_panel import VerseMindPanel
from ui.debugger_panel import DebuggerPanel
from ui.analytics_panel import AnalyticsPanel
from ui.paradox_panel import ParadoxPanel
from ui.helpers import alert


# ================= THEME =================
BG_MAIN = "#0f0f12"
BG_SIDEBAR = "#15151a"
BG_TOPBAR = "#1b1b22"
BG_PANEL = "#1e1e26"

ACCENT = "#c1121f"
ACCENT_HOVER = "#e11d2e"

TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#b0b0b0"


def run_app():
    root = tk.Tk()
    root.title("PURGE Engine")
    root.state("zoomed")
    root.configure(bg=BG_MAIN)

    canon = Canon()
    hot_reload = HotReloadManager(canon)

    # ================= ROOT GRID =================
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # ================= TOP BAR =================
    topbar = tk.Frame(root, height=50, bg=BG_TOPBAR)
    topbar.grid(row=0, column=0, columnspan=2, sticky="ew")

    tk.Label(
        topbar,
        text="PURGE",
        fg=ACCENT,
        bg=BG_TOPBAR,
        font=("Segoe UI", 16, "bold")
    ).pack(side="left", padx=20)

    tk.Label(
        topbar,
        text="Procedural Universe Realtime Game Engine",
        fg=TEXT_MUTED,
        bg=BG_TOPBAR,
        font=("Segoe UI", 10)
    ).pack(side="left", padx=10)

    def save():
        title = canon.meta.get("title")
        if not title:
            alert("Project title is required before saving.")
            return

        try:
            path, status = save_project(canon.to_dict())
        except Exception as e:
            alert(f"Save failed:\n{e}")
            return

        if status == "created":
            msg = f"Project created at:\n{path}"
        elif status == "overwritten":
            msg = f"Project overwritten at:\n{path}"
        else:  # forked
            msg = f"Project forked to:\n{path}"

        alert(msg)

    tk.Button(
        topbar,
        text="SAVE PROJECT",
        command=save,
        bg=ACCENT,
        fg=TEXT_PRIMARY,
        activebackground=ACCENT_HOVER,
        activeforeground=TEXT_PRIMARY,
        relief="flat",
        padx=18,
        pady=6,
        font=("Segoe UI", 10, "bold")
    ).pack(side="right", padx=20)

    # ================= SIDEBAR =================
    sidebar = tk.Frame(root, width=240, bg=BG_SIDEBAR)
    sidebar.grid(row=1, column=0, sticky="ns")
    sidebar.pack_propagate(False)

    tk.Label(
        sidebar,
        text="WORKSPACE",
        fg=TEXT_MUTED,
        bg=BG_SIDEBAR,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=20, pady=(20, 10))

    # ================= CONTENT =================
    content = tk.Frame(root, bg=BG_MAIN)
    content.grid(row=1, column=1, sticky="nsew")
    content.grid_rowconfigure(0, weight=1)
    content.grid_columnconfigure(0, weight=1)

    # ================= PANELS =================
    panels = {
        "Project": ProjectPanel(content, canon),
        "Canon": CanonPanel(content, canon),
        "Rules": RuleEditor(content, canon),
        "Timeline": TimelinePanel(content, canon),
        "Validate": ValidationPanel(content, canon),
        "VerseMind": VerseMindPanel(content, canon),
        "Debugger": DebuggerPanel(content, canon),
        "Analytics": AnalyticsPanel(content, canon),
        "Paradox": ParadoxPanel(content, canon),
    }

    for panel in panels.values():
        panel.configure(bg=BG_PANEL)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.grid_remove()

    def show_panel(name):
        for p in panels.values():
            p.grid_remove()
        panels[name].grid()

    # ================= NAV BUTTONS =================
    def nav_button(label):
        return tk.Button(
            sidebar,
            text=label.upper(),
            anchor="w",
            command=lambda: show_panel(label),
            bg=BG_SIDEBAR,
            fg=TEXT_PRIMARY,
            activebackground=ACCENT,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=20,
            pady=10,
            font=("Segoe UI", 11)
        )

    for name in panels:
        nav_button(name).pack(fill="x")

    show_panel("Project")

    # ================= HOT RELOAD LOOP =================
    def poll_hot_reload():
        hot_reload.scan()
        root.after(1000, poll_hot_reload)

    poll_hot_reload()
    root.mainloop()
