import tkinter as tk
from core.axiom import new_rule, validate_rule
from ui.helpers import alert

class RuleEditor(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon
        self.rule = new_rule()

        tk.Label(self, text="RULE EDITOR", font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Rule Reason (Required)").pack()
        self.reason = tk.Entry(self, width=40)
        self.reason.pack()

        tk.Label(self, text="Constraint Type").pack()
        self.constraint_type = tk.StringVar(value="forbid")
        tk.OptionMenu(self, self.constraint_type, "forbid", "require", "limit").pack()

        tk.Label(self, text="Constraint Target").pack()
        self.target = tk.Entry(self)
        self.target.pack()

        tk.Button(self, text="Save Rule", command=self.save).pack(pady=10)

        self.rules_list = tk.Listbox(self, width=60)
        self.rules_list.pack(pady=5)

    def save(self):
        self.rule["reason"] = self.reason.get()
        self.rule["constraint"]["type"] = self.constraint_type.get()
        self.rule["constraint"]["value"] = self.target.get()

        try:
            validate_rule(self.rule)
        except Exception as e:
            alert(str(e))
            return

        self.canon.add_rule(self.rule)
        self.rules_list.insert(tk.END, f"{self.rule['id']} — {self.rule['reason']}")
        alert("Rule added to canon")
        self.rule = new_rule()
        self.reason.delete(0, tk.END)
        self.target.delete(0, tk.END)
