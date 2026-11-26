import streamlit as st

st.set_page_config(page_title="C172 Checklist", layout="centered")

# Replace or expand this dictionary with your exact C172 checklist
CHECKLIST = {
    "Preflight Inspection (Cabin)": [
        ("Control Wheel Lock", "REMOVE"),
        ("Ignition Switch", "OFF"),
        ("Avionics Switch", "OFF"),
        ("Master Switch", "ON"),
        ("Fuel Quantity Indicators", "CHECK QUANTITY"),
        ("Flaps", "EXTEND"),
        ("Master Switch", "OFF"),
    ],
    "Before Starting Engine": [
        ("Preflight Inspection", "COMPLETE"),
        ("Seats, Seat Belts, Shoulder Harnesses", "ADJUST and LOCK"),
        ("Brakes", "TEST and SET"),
        ("Fuel Selector Valve", "BOTH"),
    ],
}

def reset_checklist():
    for key in list(st.session_state.keys()):
        if key.startswith("chk_"):
            st.session_state[key] = False

st.title("Cessna 172 Checklist")
st.button("Reset All", on_click=reset_checklist)

for section, items in CHECKLIST.items():
    st.subheader(section)
    completed = 0

    for idx, (item, action) in enumerate(items):
        key = f"chk_{section}_{idx}"
        col1, col2, col3 = st.columns([5, 3, 1], vertical_alignment="center")

        with col1:
            st.markdown(f"**{item}**")
        with col2:
            st.markdown(f"`{action}`")
        with col3:
            checked = st.checkbox("Done", key=key, label_visibility="collapsed")
            if checked:
                completed += 1

    if completed == len(items):
        st.success(f"{section} — COMPLETE")
    st.divider()
