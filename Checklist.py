import streamlit as st

st.set_page_config(page_title="C172 Checklist", layout="centered")

CHECKLIST_PARTS = {
    "PART A - GROUND-BASED CHECKLISTS": [
        {
            "title": "A1.0 INITIAL INSPECTION",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("Aircraft Position", "NO OBSTRUCTIONS"),
                        ("Fuel Quantity", "SUFFICIENT"),
                        ("Fuel Drain", "COMPLETE"),
                        ("Fuel Leaks", "NIL"),
                        ("Oil Quantity", "SUFFICIENT"),
                        ("Oil Leaks", "NIL"),
                        ("Windows", "CLEAN"),
                    ],
                }
            ],
            "footer": "INITIAL INSPECTION checklist complete",
        },
        {
            "title": "A2.0 PRE-FLIGHT INSPECTION",
            "subsections": [
                {
                    "subtitle": "INITIAL CHECKS",
                    "items": [
                        ("Rudder Gust Lock", "REMOVED"),
                        ("Pitot Tube Cover", "REMOVED"),
                        ("Baggage Compartment Door", "SECURE"),
                        ("POH, GCRG, QRH", "ON BOARD, CURRENT"),
                        ("Maps & Charts", "ON BOARD, CURRENT"),
                        ("STBY BATT", "OFF"),
                        ("MASTER Switch (ALT & BAT)", "OFF"),
                        ("AVIONICS Switch (BUS 1 & BUS 2)", "OFF"),
                        ("Cockpit Lighting", "OFF"),
                        ("External Lighting", "BEACON ON (Other Lights Off)"),
                        ("FUEL PUMP Switch", "OFF"),
                        ("PITOT HEAT Switch", "OFF"),
                        ("CABIN PWR 12V Switch", "OFF"),
                        ("MAGNETOS Switch", "OFF, KEY REMOVED"),
                        ("Circuit Breakers", "IN"),
                        ("ALT STATIC AIR Valve", "OFF"),
                        ("Throttle Control", "IDLE"),
                        ("Mixture Control", "IDLE CUT-OFF"),
                        ("Flaps", "UP"),
                        ("CABIN HEAT Control Knob", "OFF"),
                        ("CABIN AIR Control Knob", "ON"),
                        ("FUEL SELECTOR Valve", "BOTH"),
                        ("FUEL SHUT-OFF Valve", "ON"),
                    ],
                }
            ],
            "footer": "PRE-FLIGHT INSPECTION checklist continued next page",
        },
    ]
}


def reset_checklist():
    for key in list(st.session_state.keys()):
        if key.startswith("chk_"):
            st.session_state[key] = False


st.title("Cessna 172 Checklist")
st.button("Reset All", on_click=reset_checklist)

for part_title, sections in CHECKLIST_PARTS.items():
    st.header(part_title)

    for s_idx, section in enumerate(sections):
        st.subheader(section["title"])
        total_items = 0
        completed_items = 0

        for sub_idx, subsection in enumerate(section["subsections"]):
            if subsection["subtitle"]:
                st.markdown(
                    f"**<u>{subsection['subtitle']}</u>**",
                    unsafe_allow_html=True,
                )

            for i_idx, (item, action) in enumerate(subsection["items"], start=1):
                total_items += 1
                key = f"chk_{s_idx}_{sub_idx}_{i_idx}"
                col1, col2, col3 = st.columns([5, 4, 1], vertical_alignment="center")

                with col1:
                    st.markdown(f"**{i_idx}. {item}**")
                with col2:
                    st.markdown(
                        f"<div style='text-align: right; font-weight: bold;'>{action}</div>",
                        unsafe_allow_html=True,
                    )
                with col3:
                    if st.checkbox("Done", key=key, label_visibility="collapsed"):
                        completed_items += 1

        if completed_items == total_items and total_items > 0:
            st.success(section["footer"])
        else:
            st.markdown(
                f"<div style='text-align: center; font-style: italic; margin-top: 8px;'>{section['footer']}</div>",
                unsafe_allow_html=True,
            )

        st.divider()
