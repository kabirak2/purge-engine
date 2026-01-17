import tkinter as tk
from core.analytics import narrative_analytics

class AnalyticsPanel(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon

        tk.Label(self, text="NARRATIVE ANALYTICS", font=("Arial", 12)).pack(pady=5)

        self.output = tk.Text(self, width=80, height=20)
        self.output.pack(pady=5)

        tk.Button(self, text="Refresh Analytics", command=self.refresh).pack(pady=5)

    def refresh(self):
        self.output.delete("1.0", tk.END)
        data = narrative_analytics(self.canon)
        for k, v in data.items():
            self.output.insert(tk.END, f"{k}: {v}\n")
