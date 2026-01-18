import streamlit as st
from core.canon import get_canon, save_current_canon
from core.rule_decay import list_rules, update_rule

def render():
    st.markdown("### Rules")
    st.caption("Narrative constraints and invariants")

    canon = get_canon()

    # ---------------- CREATE NEW RULE ----------------
    with st.expander("➕ Add new rule", expanded=True):
        rule_id = st.text_input("Rule ID", placeholder="e.g. no_time_travel")
        rule_text = st.text_area(
            "Rule description",
            placeholder="Describe the constraint in plain language",
            height=100
        )

        severity = st.selectbox("Severity", ["hard", "soft"])

        if st.button("Add Rule"):
            if not rule_id or not rule_text:
                st.warning("Rule ID and description are required.")
            else:
                canon.add_rule({
                    "id": rule_id,
                    "text": rule_text,
                    "severity": severity,
                    "conditions": {"all": []},
                    "constraint": {},
                })
                save_current_canon()
                st.success("Rule added to canon.")

    st.divider()

    # ---------------- EDIT EXISTING RULES ----------------
    rules = list_rules(canon)

    if not rules:
        st.info("No rules defined yet.")
        return

    st.markdown("#### Existing rules")

    rule_ids = [r.get("id") for r in rules]
    selected = st.selectbox("Select rule", rule_ids)

    rule = next(r for r in rules if r.get("id") == selected)

    new_text = st.text_area(
        "Edit rule description",
        value=rule.get("text", ""),
        height=100
    )

    if st.button("Update Rule"):
        update_rule(selected, new_text, canon)
        save_current_canon()
        st.success("Rule updated.")
