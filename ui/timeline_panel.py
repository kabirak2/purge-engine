import tkinter as tk
import uuid

from core.validator import validate_action
from core.event_logger import log_event


class TimelinePanel(tk.Frame):
    def __init__(self, master, canon):
        super().__init__(master)
        self.canon = canon

        tk.Label(self, text="TIMELINE / EVENTS", font=("Arial", 12)).pack(pady=5)

        form = tk.Frame(self)
        form.pack(pady=5)

        tk.Label(form, text="Event Name").grid(row=0, column=0)
        self.name = tk.Entry(form, width=30)
        self.name.grid(row=0, column=1)

        tk.Label(form, text="Description").grid(row=1, column=0)
        self.desc = tk.Entry(form, width=30)
        self.desc.grid(row=1, column=1)

        tk.Label(form, text="Act").grid(row=2, column=0)
        self.act = tk.Entry(form, width=10)
        self.act.grid(row=2, column=1)

        tk.Label(form, text="Tags (comma separated)").grid(row=3, column=0)
        self.tags = tk.Entry(form, width=30)
        self.tags.grid(row=3, column=1)

        tk.Button(self, text="Add Event", command=self.add_event).pack(pady=5)

        self.listbox = tk.Listbox(self, width=90)
        self.listbox.pack(pady=5)

    # -------------------------------------------------

    def add_event(self):
        name = self.name.get().strip()
        desc = self.desc.get().strip()
        act = self.act.get().strip()

        if not name or not act.isdigit():
            return

        event = {
            "id": f"event_{uuid.uuid4().hex[:6]}",
            "name": name,
            "description": desc,
            "act": int(act),
            "tags": [t.strip() for t in self.tags.get().split(",") if t.strip()]
        }

        action = {"type": "event", "value": name}
        context = {"act": event["act"]}

        # ---------- VALIDATION ----------
        result = validate_action(action, self.canon, context)

        # Normalize validator output
        if isinstance(result, dict):
            blocked_rules = result.get("blocked", [])
            warned_rules = result.get("warned", [])
        else:
            blocked_rules = result or []
            warned_rules = []

        # Normalize rule data
        blocked_by = []
        for r in blocked_rules:
            if isinstance(r, dict):
                blocked_by.append({
                    "rule_id": r.get("id"),
                    "reason": r.get("reason")
                })
            else:
                blocked_by.append({
                    "rule_id": str(r),
                    "reason": "Blocked by rule"
                })

        # Determine status
        if blocked_rules:
            status = "blocked"
        elif warned_rules:
            status = "warned"
        else:
            status = "allowed"

        # ---------- LOGGING ----------
        log_event(
            canon=self.canon,
            entry_type="event_attempt",
            source="human",
            action=action,
            payload=event,
            context=context,
            validation={
                "status": status,
                "blocked_by": blocked_by
            },
            commit={"written_to_canon": status == "allowed"}
        )

        # ---------- CANON COMMIT ----------
        if status == "allowed":
            self.canon.add_event(event)
            status_label = "✅ ALLOWED"
        elif status == "warned":
            self.canon.add_event(event)
            status_label = "⚠️ WARNED"
        else:
            status_label = "❌ BLOCKED"

        # ---------- UI UPDATE ----------
        self.listbox.insert(
            tk.END,
            f"{status_label} | Act {event['act']} | {event['name']} — {event['description']}"
        )

        # Clear inputs
        self.name.delete(0, tk.END)
        self.desc.delete(0, tk.END)
        self.act.delete(0, tk.END)
        self.tags.delete(0, tk.END)
