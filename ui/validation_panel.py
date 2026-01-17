import tkinter as tk
from core.validator import validate_action
from core.event_logger import log_event
from ui.helpers import alert

class ValidationPanel(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon

        tk.Label(self, text="VALIDATION CONSOLE", font=("Arial", 12)).pack(pady=5)

        form = tk.Frame(self)
        form.pack()

        tk.Label(form, text="Test Event").grid(row=0, column=0)
        self.event = tk.Entry(form)
        self.event.grid(row=0, column=1)

        tk.Label(form, text="Context: Act").grid(row=1, column=0)
        self.act = tk.Entry(form)
        self.act.grid(row=1, column=1)

        tk.Button(self, text="Run Validation", command=self.run).pack(pady=5)

        self.output = tk.Text(self, height=6, width=60)
        self.output.pack(pady=5)

    def run(self):
        self.output.delete("1.0", tk.END)

        event = self.event.get().strip()
        act = self.act.get().strip()

        if not event or not act.isdigit():
            alert("Please provide event and numeric act")
            return

        action = {"type": "event", "value": event}
        context = {"act": int(act)}

        blocked = validate_action(action, self.canon, context)

        # 🔥 LOG VALIDATION CHECK
        log_event(
            canon=self.canon,
            entry_type="validation_check",
            source="human",
            action=action,
            context=context,
            validation={
                "status": "blocked" if blocked else "allowed",
                "blocked_by": [
                    {"rule_id": r["id"], "reason": r["reason"]}
                    for r in blocked
                ]
            }
        )

        if not blocked:
            self.output.insert(tk.END, "✅ ALLOWED\n")
        else:
            self.output.insert(tk.END, "❌ BLOCKED\n\n")
            for rule in blocked:
                self.output.insert(
                    tk.END,
                    f"Rule: {rule['id']}\nReason: {rule['reason']}\n\n"
                )
