import tkinter as tk

class ProjectPanel(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon

        tk.Label(self, text="PROJECT SETTINGS", font=("Arial", 12)).pack(pady=5)

        tk.Label(self, text="Title").pack()
        self.title = tk.Entry(self, width=40)
        self.title.pack()

        tk.Label(self, text="Author").pack()
        self.author = tk.Entry(self, width=40)
        self.author.pack()

        tk.Label(self, text="Version").pack()
        self.version = tk.Entry(self, width=40)
        self.version.insert(0, "0.1")
        self.version.pack()

        tk.Button(self, text="Apply Metadata", command=self.apply).pack(pady=5)

    def apply(self):
        self.canon.meta["title"] = self.title.get()
        self.canon.meta["author"] = self.author.get()
        self.canon.meta["version"] = self.version.get()
