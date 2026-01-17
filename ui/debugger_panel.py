import tkinter as tk
from ui.helpers import alert
from core.replay import replay_until
from core.loader import reload_project

class DebuggerPanel(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon

        tk.Label(self, text="NARRATIVE DEBUGGER", font=("Arial", 12)).pack(pady=5)

        self.listbox = tk.Listbox(self, width=100)
        self.listbox.pack(pady=5)

        self.refresh()

        tk.Button(self, text="Rewind To Selected", command=self.rewind).pack(pady=4)
        tk.Button(self, text="Reload Canon From Disk", command=self.reload_disk).pack(pady=4)
        tk.Button(self, text="Refresh Logs", command=self.refresh).pack(pady=4)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for log in self.canon.event_log:
            self.listbox.insert(
                tk.END,
                f"{log.get('log_id','?')} | {log.get('entry_type')} | {log.get('source')}"
            )

    def rewind(self):
        sel = self.listbox.curselection()
        if not sel:
            alert("Select a log entry")
            return

        log_id = self.listbox.get(sel[0]).split(" | ")[0]
        replay_until(self.canon, log_id)
        alert(f"Replayed canon until {log_id}")

    def reload_disk(self):
        title = self.canon.meta.get("title")
        if not title:
            alert("No project title set")
            return

        ok = reload_project(self.canon, title)
        if ok:
            alert("Canon hot-reloaded from disk")
            self.refresh()
        else:
            alert("Saved project not found")
