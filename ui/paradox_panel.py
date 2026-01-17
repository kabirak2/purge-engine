import tkinter as tk
from core.paradox import detect_paradoxes

class ParadoxPanel(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon

        tk.Label(self, text="PARADOX DETECTOR", font=("Arial", 12)).pack(pady=5)

        self.listbox = tk.Listbox(self, width=100)
        self.listbox.pack(pady=5)

        tk.Button(self, text="Scan for Paradoxes", command=self.scan).pack(pady=5)

    def scan(self):
        self.listbox
