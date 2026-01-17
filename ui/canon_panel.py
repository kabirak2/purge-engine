import tkinter as tk
from ui.helpers import alert

class CanonPanel(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon

        tk.Label(self, text="CANON TRUTHS", font=("Arial", 12)).pack(pady=5)

        form = tk.Frame(self)
        form.pack()

        tk.Label(form, text="Key").grid(row=0, column=0)
        self.key = tk.Entry(form, width=20)
        self.key.grid(row=0, column=1)

        tk.Label(form, text="Value").grid(row=1, column=0)
        self.value = tk.Entry(form, width=20)
        self.value.grid(row=1, column=1)

        tk.Button(self, text="Add Truth", command=self.add).pack(pady=5)

        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack(pady=5)

    def add(self):
        k = self.key.get().strip()
        v = self.value.get().strip()

        if not k:
            alert("Truth key cannot be empty")
            return

        self.canon.truths[k] = v
        self.listbox.insert(tk.END, f"{k} = {v}")

        self.key.delete(0, tk.END)
        self.value.delete(0, tk.END)
