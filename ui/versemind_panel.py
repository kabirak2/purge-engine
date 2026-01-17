import tkinter as tk
import uuid
from core.versemind import propose
from core.event_logger import log_event
from ui.helpers import alert

class VerseMindPanel(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon
        self.current_proposal = None

        tk.Label(self, text="VERSEMIND", font=("Arial", 12)).pack(pady=5)

        tk.Label(self, text="Describe what you want to add or fix:").pack()
        self.input = tk.Entry(self, width=60)
        self.input.pack(pady=2)

        tk.Button(self, text="Ask VerseMind", command=self.ask).pack(pady=5)

        self.output = tk.Text(self, height=8, width=80)
        self.output.pack(pady=5)

        tk.Button(self, text="Approve Proposal", command=self.approve).pack(pady=2)

    def ask(self):
        text = self.input.get().strip()
        if not text:
            alert("Please describe your intent.")
            return

        self.current_proposal = propose(self.canon, text)

        # 🔥 LOG PROPOSAL GENERATION
        log_event(
            canon=self.canon,
            entry_type="proposal_generated",
            source="versemind",
            action={"type": self.current_proposal["type"], "value": "proposal"},
            payload=self.current_proposal
        )

        self.output.delete("1.0", tk.END)
        self.output.insert(
            tk.END,
            f"TYPE: {self.current_proposal['type']}\n"
            f"CONFIDENCE: {self.current_proposal['confidence']}\n\n"
            f"EXPLANATION:\n{self.current_proposal['explanation']}\n\n"
            f"PAYLOAD:\n{self.current_proposal['payload']}"
        )

    def approve(self):
        if not self.current_proposal:
            alert("No proposal to approve.")
            return

        p = self.current_proposal

        # 🔥 LOG APPROVAL
        log_event(
            canon=self.canon,
            entry_type="proposal_approved",
            source="human",
            action={"type": p["type"], "value": "approval"},
            payload=p,
            commit={"written_to_canon": True}
        )

        if p["type"] == "event":
            event = {
                "id": f"event_{uuid.uuid4().hex[:6]}",
                **p["payload"]
            }
            self.canon.add_event(event)
            alert("Event added to canon.")

        elif p["type"] == "rule":
            rule = {
                "id": f"rule_{uuid.uuid4().hex[:6]}",
                "scope": "global",
                "conditions": {"all": []},
                "constraint": p["payload"]["constraint"],
                "reason": p["payload"]["reason"],
                "metadata": {
                    "created_by": "versemind",
                    "confidence": p["confidence"]
                }
            }
            self.canon.add_rule(rule)
            alert("Rule added to canon.")

        else:
            alert("Suggestion noted (no canon change).")

        self.current_proposal = None
        self.output.delete("1.0", tk.END)
        self.input.delete(0, tk.END)
