import streamlit as st

st.set_page_config(page_title="C172R&S G1000 Checklist", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.recall-marker) {
        border: 3px solid #000000 !important;
        border-radius: 2px;
        padding: 10px 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

CHECKLIST_PARTS = {
    "PART A - GROUND-BASED CHECKLISTS": [
        {
            "title": "A1.0 INITIAL INSPECTION",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Aircraft Position", "NO OBSTRUCTIONS"),
                        ("2.", "Fuel Quantity", "SUFFICIENT"),
                        ("3.", "Fuel Drain", "COMPLETE"),
                        ("4.", "Fuel Leaks", "NIL"),
                        ("5.", "Oil Quantity", "SUFFICIENT"),
                        ("6.", "Oil Leaks", "NIL"),
                        ("7.", "Windows", "CLEAN"),
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
                        ("1.", "Rudder Gust Lock", "REMOVED"),
                        ("2.", "Pitot Tube Cover", "REMOVED"),
                        ("3.", "Baggage Compartment Door", "SECURE"),
                        ("4.", "POH, GCRG, QRH", "ON BOARD, CURRENT"),
                        ("5.", "Maps & Charts", "ON BOARD, CURRENT"),
                        ("6.", "STBY BATT", "OFF"),
                        ("7.", "MASTER Switch (ALT & BAT)", "OFF"),
                        ("8.", "AVIONICS Switch (BUS 1 & BUS 2)", "OFF"),
                        ("9.", "Cockpit Lighting", "OFF"),
                        ("10.", "External Lighting", "BEACON ON (Other Lights Off)"),
                        ("11.", "FUEL PUMP Switch", "OFF"),
                        ("12.", "PITOT HEAT Switch", "OFF"),
                        ("13.", "CABIN PWR 12V Switch", "OFF"),
                        ("14.", "MAGNETOS Switch", "OFF, KEY REMOVED"),
                        ("15.", "Circuit Breakers", "IN"),
                        ("16.", "ALT STATIC AIR Valve", "OFF"),
                        ("17.", "Throttle Control", "IDLE"),
                        ("18.", "Mixture Control", "IDLE CUT-OFF"),
                        ("19.", "Flaps", "UP"),
                        ("20.", "CABIN HEAT Control Knob", "OFF"),
                        ("21.", "CABIN AIR Control Knob", "ON"),
                        ("22.", "FUEL SELECTOR Valve", "BOTH"),
                        ("23.", "FUEL SHUT-OFF Valve", "ON"),
                        ("24.", "Fire Extinguisher", "SERVICEABLE"),
                        ("25.", "MASTER Switch (ALT & BAT)", "ON"),
                        ("26.", "Primary Flight Display (PFD)", "ON"),
                        ("27.", "Fuel QTY GAL", "SUFFICIENT"),
                        ("28.", "LOW FUEL L & R Annunciators", "EXTINGUISHED"),
                        ("29.", "OIL PRESSURE Annunciator", "ILLUMINATED"),
                        ("30.", "LOW VACUUM Annunciator", "ILLUMINATED"),
                        ("31.", "AVIONICS Switch (BUS 1)", "ON"),
                        ("32.", "Forward Avionics Fan", "AUDIBLE"),
                        ("33.", "AVIONICS Switch (BUS 1)", "OFF"),
                        ("34.", "AVIONICS Switch (BUS 2)", "ON"),
                        ("35.", "Aft Avionics Fan", "AUDIBLE"),
                        ("36.", "AVIONICS Switch (BUS 2)", "OFF"),
                        ("37.", "External Lighting & PITOT HEAT Switch", "ON"),
                        ("38.", "External Lighting & PITOT HEAT", "FUNCTIONAL (Check Externally)"),
                        ("39.", "External Lighting", "BEACON ON (Other Lights Off)"),
                        ("40.", "PITOT HEAT Switch", "OFF"),
                        ("41.", "Flaps", "FULL"),
                        ("42.", "MASTER Switch (ALT & BAT)", "OFF"),
                        ("43.", "Circuit Breakers", "IN"),
                        ("44.", "Control Wheel Lock", "REMOVED"),
                        ("45.", "Flight Controls", "FULL & FREE MOVEMENT"),
                        ("46.", "Elevator Trim Control", "FREE & SET FOR TAKEOFF"),
                    ],
                },
                {
                    "subtitle": "LEFT WING",
                    "items": [
                        ("1.", "Surface Condition", "NO ICE OR DAMAGE"),
                        ("2.", "COMM, GPS Antennas, & OAT Probe", "NO DAMAGE"),
                        ("3.", "Fuel Filler Cap", "SECURE & VENT CLEAR"),
                        ("4.", "CABIN AIR Inlets", "CLEAR"),
                        ("5.", "Wing Strut", "NO DAMAGE"),
                        ("6.", "Pitot Tube", "NO OBSTRUCTIONS"),
                        ("7.", "Fuel Tank Vent Opening", "CLEAR"),
                        ("8.", "Stall Warning Opening", "CLEAR & TESTED"),
                        ("9.", "LAND & TAXI Lights", "COVER SECURE"),
                        ("10.", "Leading Edge", "NO ICE OR DAMAGE"),
                        ("11.", "Wing Tip & Lights", "NO DAMAGE"),
                        ("12.", "Static Wicks (Two)", "NO DAMAGE"),
                        ("13.", "Aileron", "SECURE & FREE MOVEMENT"),
                        ("14.", "Flap", "SECURE & NO DAMAGE"),
                        ("15.", "Fuel Drain Valves", "NO LEAKS"),
                    ],
                },
                {
                    "subtitle": "LEFT MAIN GEAR",
                    "items": [
                        ("1.", "Main Gear Strut", "NO DAMAGE"),
                        ("2.", "Main Wheel Tyre", "SERVICEABLE"),
                        ("3.", "Main Wheel Brake Assembly", "NO DAMAGE OR LEAKS"),
                    ],
                },
                {
                    "subtitle": "LEFT FUSELAGE",
                    "items": [
                        ("1.", "Main Door & Window", "CLEAN & SECURE"),
                        ("2.", "Baggage Compartment Door", "CLOSED & LATCHED"),
                        ("3.", "Rear Window", "CLEAN"),
                    ],
                },
                {
                    "subtitle": "EMPENNAGE",
                    "items": [
                        ("1.", "Horizontal & Vertical Stabiliser", "NO ICE OR DAMAGE"),
                        ("2.", "Elevator & Trim Tab", "SECURE & FREE MOVEMENT"),
                        ("3.", "Rudder", "SECURE & FREE MOVEMENT"),
                        ("4.", "Static Wicks (Six)", "NO DAMAGE"),
                        ("5.", "Tie Down Ring", "NO DAMAGE"),
                        ("6.", "VOR & ILS Antennas", "NO DAMAGE"),
                    ],
                },
                {
                    "subtitle": "RIGHT FUSELAGE",
                    "items": [
                        ("1.", "Aircraft Belly & Antennas", "NO DAMAGE"),
                        ("2.", "ELT Antenna", "NO DAMAGE"),
                        ("3.", "Main Door & Window", "CLEAN & SECURE"),
                    ],
                },
                {
                    "subtitle": "RIGHT MAIN GEAR",
                    "items": [
                        ("1.", "Main Gear Strut", "NO DAMAGE"),
                        ("2.", "Main Wheel Tyre", "SERVICEABLE"),
                        ("3.", "Main Wheel Brake Assembly", "NO DAMAGE OR LEAKS"),
                    ],
                },
                {
                    "subtitle": "RIGHT WING",
                    "items": [
                        ("1.", "Fuel Drain Valves", "NO LEAKS"),
                        ("2.", "Flap", "SECURE & NO DAMAGE"),
                        ("3.", "Aileron", "SECURE & FREE MOVEMENT"),
                        ("4.", "Static Wicks (Two)", "NO DAMAGE"),
                        ("5.", "Wing Tip & Lights", "NO DAMAGE"),
                        ("6.", "Leading Edge", "NO ICE OR DAMAGE"),
                        ("7.", "LAND & TAXI Lights", "COVER SECURE"),
                        ("8.", "Wing Strut", "NO DAMAGE"),
                        ("9.", "CABIN AIR Inlets", "CLEAR"),
                        ("10.", "Fuel Filler Cap", "SECURE & VENT CLEAR"),
                        ("11.", "COMM, GPS Antennas, & OAT Probe", "NO DAMAGE"),
                        ("12.", "Surface Condition", "NO ICE OR DAMAGE"),
                    ],
                },
                {
                    "subtitle": "NOSE WHEEL",
                    "items": [
                        ("1.", "Fuel Drain Valves", "NO LEAKS"),
                        ("2.", "Nose Wheel Strut", "INFLATED"),
                        ("3.", "Torque Link", "NO DAMAGE"),
                        ("4.", "Shimmy Dampener", "NO DAMAGE OR LEAKS"),
                        ("5.", "Steering Arms", "SECURE"),
                        ("6.", "Nose Wheel Tyre", "SERVICEABLE"),
                        ("7.", "Nose Wheel Area", "NO LEAKS"),
                    ],
                },
                {
                    "subtitle": "NOSE",
                    "items": [
                        ("1.", "CABIN AIR Vent", "NO DAMAGE"),
                        ("2.", "Engine Cowling", "NO DAMAGE"),
                        ("3.", "Engine Oil Inspection", "DIPSTICK SECURE & NO LEAKS"),
                        ("4.", "Engine Cooling Air Inlets", "CLEAR"),
                        ("5.", "Alternator Belt", "NO DAMAGE & UNDER TENSION"),
                        ("6.", "Propeller & Spinner", "NO DAMAGE"),
                        ("7.", "Engine Air Intake Filter", "CLEAR"),
                        ("8.", "External Power Door", "SECURE"),
                        ("9.", "Static Source Opening", "CLEAR"),
                    ],
                },
            ],
            "post_note": "Prior to proceeding to A3.0 PRE-ENTRY INSPECTION, the pilot must perform A15.0 POST-FLIGHT INSPECTION if they intend to leave the aircraft unsupervised.",
            "footer
