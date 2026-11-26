import asyncio
import base64
import json
import re
import time
import edge_tts
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="C172R&S G1000 Checklist", layout="centered")

VOICE_OPTIONS = {
    "Luna (Singapore Female)": "en-SG-LunaNeural",
    "Sonia (British Female)": "en-GB-SoniaNeural",
    "Natasha (Australian Female)": "en-AU-NatashaNeural",
    "Aria (US Female)": "en-US-AriaNeural",
}

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
            "footer": "PRE-FLIGHT INSPECTION checklist complete",
        },
        {
            "title": "A3.0 PRE-ENTRY INSPECTION",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Key", "WITHIN COCKPIT, ACCESSIBLE"),
                        ("2.", "Control Wheel Lock", "REMOVED"),
                        ("3.", "Parking Brake", "SET"),
                        ("4.", "Chocks (Three)", "REMOVED"),
                        ("5.", "Tie Down Ropes (Three)", "REMOVED"),
                        ("6.", "Pitot Tube Cover", "REMOVED"),
                        ("7.", "Rudder Gust Lock", "REMOVED"),
                        ("8.", "Baggage Compartment", "BAGGAGE UNDER CARGO NET, DOOR SECURE"),
                    ],
                }
            ],
            "footer": "PRE-ENTRY INSPECTION checklist complete",
        },
        {
            "title": "A4.0 BEFORE START",
            "note": "During cold weather starting, when performing the STBY BATT test (item 7), the lamp may not illuminate, and the E BUS volts (item 12) may be less than 24 VOLTS. If either of these events occur, after engine start verify the S BATT ammeter shows a positive charge at 1000 RPM or greater. Then prior to takeoff verify the S BATT ammeter shows a charge of less than 0.4 AMPS.",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Pre-Start Up Brief", "COMPLETE"),
                        ("2.", "Maintenance Release", "ON BOARD, SIGNED, & VALID"),
                        ("3.", "Passenger Briefing", "COMPLETE (If Required)"),
                        ("4.", "MASTER Switch (ALT & BAT)", "OFF"),
                        ("5.", "AVIONICS Switch (BUS 1 & BUS 2)", "OFF"),
                        ("6.", "External Lighting", "BEACON ON, NAV AS REQUIRED (Other Lights Off)"),
                        ("7.", "STBY BATT", "TESTED 10 SECONDS (See Note Above)"),
                        ("8.", "STBY BATT", "ARMED"),
                        ("9.", "Primary Flight Display", "ON"),
                        ("10.", "Engine Indicating System", "NO RED X ANNUNCIATIONS"),
                        ("11.", "M BUS", "1.5 VOLTS MAXIMUM"),
                        ("12.", "E BUS", "24 VOLTS MINIMUM (See Note Above)"),
                        ("13.", "S BATT", "DISCHARGING"),
                        ("14.", "Fuel GAL REM", "CHECKED & SET"),
                        ("15.", "STBY BATT Annunciator", "ILLUMINATED"),
                        ("16.", "Seats", "ADJUSTED"),
                        ("17.", "Seat Belts", "FASTENED"),
                        ("18.", "Doors", "CLOSED & LOCKED"),
                        ("19.", "Propeller Area", "CLEAR"),
                        ("20.", "MASTER Switch (ALT & BAT)", "ON"),
                        ("21.", "Cockpit Lights", "AS REQUIRED"),
                        ("22.", "Clearance (Circuits or Airways)", "OBTAINED (If Required)"),
                    ],
                }
            ],
            "footer": "BEFORE START checklist complete",
        },
        {
            "title": "A5.0 ENGINE START",
            "caution": "MAKE ONLY THREE START ATTEMPTS OF 10 SECONDS EACH WITH A 20 SECOND COOL DOWN PERIOD BETWEEN EACH ATTEMPT. IF THE ENGINE FAILS TO START, WAIT 10 MINUTES AND REPEAT THIS CYCLE. IF ENGINE STILL DOES NOT START, FIND THE CAUSE BEFORE ATTEMPTING ANOTHER START. NEVER RE-ENGAGE THE STARTER MOTOR UNTIL THE PROPELLER HAS COMPLETELY STOPPED.",
            "subsections": [
                {
                    "subtitle": "NORMAL START",
                    "subnote": "Oil temperature below the green range, or after a failed start",
                    "recall": True,
                    "items": [
                        ("1.", "Mixture Control", "IDLE CUT-OFF"),
                        ("2.", "Throttle Control", "OPEN 6mm (Approximately)"),
                        ("3.", "KEY", "INSERTED (Switched To OFF Position)"),
                        ("4.", "FUEL PUMP Switch", "ON"),
                        ("5.", "Mixture Control", "FULL RICH"),
                        ("6.", "FUEL FLOW", "STABLE (Maximum 3 Seconds)"),
                        ("7.", "Mixture Control", "IDLE CUT-OFF"),
                        ("8.", "FUEL PUMP Switch", "OFF"),
                        ("9.", "Propeller Area", "CLEAR"),
                        ("10.", "Brakes", "ON"),
                        ("11.", "MAGNETOS Switch", "START (Release Key When Engine Starts)"),
                        ("12.", "Mixture Control", "FULL RICH (Smoothly Increase As Engine Starts)"),
                        ("13.", "Throttle Control", "1000 RPM"),
                        ("14.", "Oil Pressure", "GREEN RANGE (Within 60 Seconds)"),
                    ],
                },
                {
                    "subtitle": "NORMAL START",
                    "subnote": "Oil temperature within the green range, and first start attempt",
                    "recall": True,
                    "items": [
                        ("1.", "Mixture Control", "IDLE CUT-OFF"),
                        ("2.", "Throttle Control", "OPEN 6mm (Approximately)"),
                        ("3.", "KEY", "INSERTED (Switched To OFF Position)"),
                        ("4.", "Propeller Area", "CLEAR"),
                        ("5.", "Brakes", "ON"),
                        ("6.", "MAGNETOS Switch", "START (Release Key When Engine Starts)"),
                        ("7.", "Mixture Control", "FULL RICH (Smoothly Increase As Engine Starts)"),
                        ("8.", "Throttle Control", "1000 RPM"),
                        ("9.", "Oil Pressure", "GREEN RANGE (Within 60 Seconds)"),
                    ],
                },
                {
                    "subtitle": "HOT START",
                    "note": "Starting the engine after it has been shut down for more than 30 minutes in warm or hot ambient outside air temperatures may cause the fuel in the fuel lines to vapourise resulting in starting difficulties. If vapour in the fuel lines is suspected, then complete the HOT START checklist.",
                    "items": [
                        ("1.", "Mixture Control", "IDLE CUT-OFF"),
                        ("2.", "Throttle Control", "OPEN 6mm"),
                        ("3.", "KEY", "INSERTED (Switched To OFF Position)"),
                        ("4.", "FUEL PUMP Switch", "ON"),
                        ("5.", "Mixture Control", "FULL RICH FOR 1-2 SECONDS"),
                        ("6.", "Mixture Control", "IDLE CUT-OFF"),
                        ("7.", "FUEL PUMP Switch", "OFF"),
                        ("8.", "Propeller Area", "CLEAR"),
                        ("9.", "Brakes", "ON"),
                        ("10.", "MAGNETOS Switch", "START (Release Key When Engine Starts)"),
                        ("11.", "Mixture Control", "ONE THIRD OPEN WHEN ENGINE STARTS THEN SMOOTHLY FULL RICH AS POWER DEVELOPS"),
                        ("12.", "Throttle Control", "1000 RPM"),
                        ("13.", "Oil Pressure", "GREEN RANGE (Within 60 Seconds)"),
                    ],
                },
                {
                    "subtitle": "FLOODED START",
                    "items": [
                        ("1.", "Mixture Control", "IDLE CUT-OFF"),
                        ("2.", "Throttle Control", "OPEN HALF TO FULL"),
                        ("3.", "KEY", "INSERTED (Switched To OFF Position)"),
                        ("4.", "Brakes", "ON"),
                        ("5.", "MAGNETOS Switch", "START (Release When Engine Starts)"),
                        ("6a.", "As Engine Starts — Mixture Control", "FULL RICH"),
                        ("6b.", "As Engine Starts — Throttle Control", "1000 RPM"),
                        ("7.", "Oil Pressure", "GREEN RANGE (Within 60 Seconds)"),
                    ],
                },
            ],
            "footer": "ENGINE START checklist complete",
        },
        {
            "title": "A6.0 AFTER START",
            "caution": "DO NOT EXCEED 1200 RPM UNTIL OIL TEMPERATURE IS IN THE GREEN RANGE OR UNTIL 8 MINUTES AFTER ENGINE START",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "M BATT & S BATT", "POSITIVE"),
                        ("2.", "LOW VOLTS Annunciator", "EXTINGUISHED"),
                        ("3.", "AVIONICS Switch (BUS 1 & BUS 2)", "ON"),
                        ("4.", "Flaps", "UP"),
                        ("5.", "GNSS Navigation Database", "CURRENT (Check, Then Press 'ENT')"),
                        ("6.", "Throttle Control", "1200 RPM"),
                        ("7.", "Mixture Control", "LEANED (Approximately 25mm)"),
                        ("8.", "Throttle Control", "1000 RPM"),
                        ("9.", "MFD Display Mode", "AS REQUIRED"),
                        ("10.", "AHRS", "ALIGNED"),
                        ("11.", "ATIS", "NOTED"),
                        ("12.", "AVIONICS", "CHECKED & SET"),
                        ("13.", "Taxi Clearance", "OBTAINED (Or Expected)"),
                        ("14.", "Taxi & Departure Brief", "COMPLETE"),
                        ("15.", "NAV & TAXI Light Switch", "ON"),
                    ],
                }
            ],
            "footer": "AFTER START checklist complete",
        },
        {
            "title": "A7.0 TAXI",
            "recall_box": True,
            "note": "To complete the TAXI checklist, items 2, 3, and 4 must each be checked twice. Once during a turn to the left, and again during a turn to the right.",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Brakes (For Each Crew Member In The Front Row)", "EFFECTIVE"),
                        ("2.", "Slip Indicator", "[LEFT OR RIGHT]"),
                        ("3.", "Compass & HSI", "[DECREASING OR INCREASING]"),
                        ("4.", "Attitude Indicators (PFD & STBY)", "ERECT & LEVEL"),
                    ],
                }
            ],
            "footer": "TAXI checklist complete",
        },
        {
            "title": "A8.0 ENGINE RUN-UP",
            "note": "When setting throttle to idle and checking the engine RPM (item 14), the pilot should hold the throttle control under tension by applying a consistent pulling pressure. If this is not performed, the engine may not idle within the limits of 600 - 800 RPM.",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Parking Brake", "SET"),
                        ("2.", "Throttle Control", "1000 RPM"),
                        ("3.", "FUEL SELECTOR Valve", "BOTH"),
                        ("4.", "OIL TEMP", "GREEN RANGE (Or 8 Minutes Elapsed)"),
                        ("5.", "Mixture Control", "FULL RICH"),
                        ("6.", "Cabin Windows", "CLOSED & LOCKED"),
                        ("7.", "Throttle Control", "1800 RPM"),
                        ("8.", "MAGNETOS Switch", "LEFT & RIGHT CHECKED"),
                        ("8a.", "Maximum Drop", "[150 RPM (C172R) OR 175 RPM (C172S/SP)]"),
                        ("8b.", "Maximum Difference", "50 RPM"),
                        ("9.", "Engine Indicators", "GREEN RANGE"),
                        ("10.", "VAC Indicator", "GREEN RANGE"),
                        ("11.", "M BUS & E BUS", "28 VOLTS MINIMUM"),
                        ("12.", "M BATT & S BATT", "NO DISCHARGE"),
                        ("13.", "Annunciators", "EXTINGUISHED"),
                        ("14.", "Throttle Control", "IDLE, WITHIN 600 - 800 RPM (See Note Above)"),
                        ("15.", "Throttle Control", "1000 RPM"),
                    ],
                }
            ],
            "footer": "ENGINE RUN-UP checklist complete",
        },
        {
            "title": "A9.0 BEFORE TAKEOFF",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Cabin Windows", "AS REQUIRED"),
                        ("2.", "FUEL SELECTOR Valve", "BOTH"),
                        ("3.", "Mixture Control", "FULL RICH"),
                        ("4.", "Throttle Control Friction Lock", "SET"),
                        ("5.", "Flaps", "SET FOR TAKEOFF"),
                        ("6.", "Engine Instruments", "GREEN RANGE"),
                        ("7.", "Fuel QTY GAL", "SUFFICIENT"),
                        ("8.", "Altimeters (PFD & STBY)", "QNH SET, ALTITUDE WITHIN TOLERANCE"),
                        ("9.", "AHRS", "ALIGNED"),
                        ("10.", "Standby Attitude Indicator", "PITCH SET"),
                        ("11.", "Alerts", "EXTINGUISHED OR CONSIDERED"),
                        ("12.", "Elevator Trim Control", "SET FOR TAKEOFF"),
                        ("13.", "Flight Controls", "FULL & FREE MOVEMENT"),
                        ("14.", "CABIN PWR 12V Switch", "OFF"),
                        ("15.", "MAGNETOS Switch", "BOTH"),
                        ("16.", "Seat Backs", "MOST UPRIGHT POSITION"),
                        ("17.", "Seat Belts", "FASTENED"),
                        ("18.", "Doors", "CLOSED & LOCKED"),
                        ("19.", "Fuel Log", "COMPLETE (If Required)"),
                    ],
                }
            ],
            "footer": "BEFORE TAKEOFF checklist complete",
        },
        {
            "title": "A10.0 BRIEFINGS",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Revised Taxi & Departure Brief", "COMPLETE (If Required)"),
                        ("2.", "Takeoff Safety Brief", "COMPLETE"),
                        ("3.", "PIC Brief", "COMPLETE"),
                    ],
                }
            ],
            "brief_recall": True,
            "brief_text": (
                '"This will be a [left or right]-hand seat takeoff.\n'
                "Minimum takeoff power is [2065 RPM or 2300 RPM] for the [C172R or C172S].\n"
                "Flaps are set to [flap setting].\n"
                "Speeds are [rotation speed] for rotation.\n"
                "Runway in use is [active runway].\n"
                "Call out any malfunction or warning.\n"
                'If a malfunction occurs before rotation, I will call "stop" or "go".\n'
                "If an engine failure or unsafe condition occurs before rotation, I will reject the takeoff.\n"
                "If an engine failure occurs after rotation, I will lower the nose, select a landing area within 30 degrees, "
                'extend flaps as required, perform the EFATO drill as required, and land."'
            ),
            "footer": "BRIEFINGS checklist complete",
        },
        {
            "title": "A11.0 HOLDING POINT",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Throttle Control", "1000 RPM"),
                        ("2.", "Cabin Windows", "CLOSED & LOCKED"),
                        ("3.", "Radio", "FREQUENCY SET"),
                        ("4.", "Transponder", "CODE SET"),
                        ("5.", "PITOT HEAT", "AS REQUIRED"),
                    ],
                }
            ],
            "footer": "HOLDING POINT checklist complete",
        },
        {
            "title": "A12.0 RUNWAY ENTRY",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Approach", "CLEAR"),
                        ("2.", "Runway", "CLEAR (Or Occupied)"),
                        ("3.", "Windsock", "CHECKED (Not Required For Runway Crossing)"),
                        ("4.", "STROBE & LAND Light Switch", "ON (STROBE Only For Runway Crossing)"),
                    ],
                }
            ],
            "footer": "RUNWAY ENTRY checklist complete",
        },
        {
            "title": "A13.0 AFTER LANDING",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Throttle Control", "1000 RPM"),
                        ("2.", "Radio", "FREQUENCY SET"),
                        ("3.", "STROBE & LAND Light Switch", "OFF"),
                        ("4.", "TAXI Light Switch", "ON"),
                        ("5.", "Elevator Trim Control", "SET FOR TAKEOFF"),
                        ("6.", "Flaps", "UP"),
                        ("7.", "Cabin Windows", "AS REQUIRED"),
                        ("8.", "Taxi Clearance", "OBTAINED"),
                    ],
                }
            ],
            "footer": "AFTER LANDING checklist complete",
        },
        {
            "title": "A14.0 SHUTDOWN",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Parking Brake", "SET"),
                        ("2.", "Throttle Control", "1000 RPM"),
                        ("3.", "MFD Display Mode", "NORMAL"),
                        ("4.", "CABIN PWR 12V Switch", "OFF"),
                        ("5.", "MAGNETOS Switch", "LEFT & RIGHT CHECKED (RPM Drops)"),
                        ("6.", "AVIONICS Switch (BUS 1 & BUS 2)", "OFF"),
                        ("7.", "Mixture Control", "IDLE CUT-OFF"),
                        ("8.", "Engine", "STOPPED"),
                        ("9.", "Throttle Control", "IDLE"),
                        ("10.", "MAGNETOS Switch", "OFF"),
                        ("11.", "Key", "REMOVED"),
                        ("12.", "External Lighting", "BEACON ON (Other Lights Off)"),
                        ("13.", "Cockpit Lights", "OFF"),
                        ("14.", "MASTER Switch (ALT & BAT)", "OFF"),
                        ("15.", "STBY BATT Switch", "OFF"),
                        ("16.", "Control Wheel Lock", "INSTALLED"),
                        ("17.", "Journey Log", "COMPLETE (Except Fuel)"),
                    ],
                }
            ],
            "footer": "SHUTDOWN checklist complete",
        },
        {
            "title": "A15.0 POST-FLIGHT INSPECTION",
            "note": "The Control Wheel Padlock (Internal Checks - Item 1) is required to be installed after the final sortie of each day, and the Rudder Gust Lock (External Checks - Item 4) is required to be installed after the final sortie of each day, as well as anytime the aircraft is parked in strong or gusting winds.",
            "subsections": [
                {
                    "subtitle": "INTERNAL CHECKS",
                    "items": [
                        ("1.", "Control Wheel Lock (Or Padlock)", "INSTALLED (See Note Above)"),
                        ("2.", "Flaps", "UP (May Require Power On)"),
                        ("3.", "MASTER Switch (ALT & BAT)", "OFF"),
                        ("4.", "Cabin", "CLEAN"),
                        ("5.", "Aircraft Documents", "STORED"),
                        ("6.", "Seatbelts", "UNFASTENED"),
                    ],
                },
                {
                    "subtitle": "EXTERNAL CHECKS",
                    "items": [
                        ("1.", "Pitot Tube Cover", "INSTALLED"),
                        ("2.", "Wheel Chocks (Three)", "INSTALLED"),
                        ("3.", "Tie Down Ropes (Three)", "INSTALLED"),
                        ("4.", "Rudder Gust Lock", "INSTALLED (If Required, See Note Above)"),
                        ("5.", "Parking Brake", "RELEASED"),
                        ("6.", "Fuel Quantity", "MEASURED & RECORDED (Via Dipstick)"),
                        ("7.", "Fluids", "NO LEAKS"),
                        ("8.", "External Surfaces", "NO DAMAGE"),
                        ("9.", "Tyres", "SERVICEABLE"),
                        ("10.", "Tail Tie Down Ring", "NO DAMAGE"),
                        ("11.", "Doors & Cabin Windows", "CLOSED"),
                        ("12.", "In-flight Issues or Defects", "REPORTED (If Required)"),
                    ],
                },
            ],
            "footer": "POST-FLIGHT INSPECTION checklist complete",
        },
    ],
    "PART B - AIRBORNE CHECKLISTS": [
        {
            "title": "B1.0 TAKEOFF",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Takeoff Clearance", "OBTAINED (If Required)"),
                        ("2.", "Takeoff Power", "SET"),
                        ("3.", "Engine Instruments", "GREEN"),
                        ("4.", "Speed", "INCREASING"),
                        ("5.", "[Rotation Speed]", "ROTATE"),
                    ],
                }
            ],
        },
        {
            "title": "B2.0 AFTER TAKEOFF (200' AGL)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Flaps", "UP"),
                        ("2.", "Engine Instruments", "GREEN"),
                        ("3.", "Centreline & Tracking", "MAINTAINED"),
                    ],
                }
            ],
        },
        {
            "title": "B3.0 DEPARTING CONTROLLED AIRSPACE (VFR)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Position", "CLEAR OF CONTROLLED AIRSPACE"),
                        ("2.", "Radio", "FREQUENCY SET"),
                        ("3.", "Transponder", "CODE SET"),
                    ],
                }
            ],
        },
        {
            "title": "B4.0 PRE-CLIMB & PRE-DESCENT",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Mixture", "FULL RICH"),
                        ("2.", "Engine Instruments", "GREEN"),
                    ],
                }
            ],
        },
        {
            "title": "B5.0 PRE-MANOEUVRE",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Reference Point", "SELECTED (If Visual)"),
                        ("2.", "Reference HDG", "SET (Unless Performing Circuits, PFL, Or Visual Circling)"),
                        ("3.", "Reference Altitude", "SET (Unless Performing Circuits, PFL, Or Visual Circling)"),
                    ],
                }
            ],
        },
        {
            "title": "B6.0 TOP OF CLIMB & BOTTOM OF DESCENT (NAVIGATION)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Power", "SET"),
                        ("2.", "Elevator Trim Control", "SET"),
                        ("3.", "Mixture", "LEANED (If Above 3000 Feet)"),
                        ("4.", "LAND Light", "OFF (If Above 3000 Feet)"),
                    ],
                }
            ],
        },
        {
            "title": "B7.0 VFR WAYPOINT (VFR NAVIGATION)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": "APPROACHING WAYPOINT",
                    "items": [
                        ("1.", "CRS", "SET"),
                        ("2.", "Altitude", "CONSIDERED"),
                        ("3.", "Time", "EXPECTED ATD NOTED"),
                    ],
                },
                {
                    "subtitle": "OVERHEAD WAYPOINT",
                    "items": [
                        ("1.", "Time", "ATD CHECKED"),
                        ("2.", "Turn", "HDG & AIRCRAFT"),
                        ("3.", "Transmit", "AS REQUIRED"),
                    ],
                },
            ],
        },
        {
            "title": "B8.0 PRE-STALL",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Height", "SUFFICIENT TO RECOVER BY 3000 FEET AGL"),
                        ("2.", "Airframe", "FLAPS UP"),
                        ("3.", "Security", "CABIN CONTENTS SECURE"),
                        ("4.", "Engine Instruments", "GREEN"),
                        ("5.", "Location", "CLEAR OF AIRFIELDS, BUILT UP AREAS, CLOUD, & CTA"),
                        ("6.", "Lookout", "COMPLETE (180° Or 2 x 90°)"),
                    ],
                }
            ],
        },
        {
            "title": "B9.0 10-MINUTE MARKERS (NAVIGATION)",
            "note": "For guidance on the specific contents of this checklist, refer to SFC training material.",
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Compass", "COMPLETE"),
                        ("2.", "Logs", "COMPLETE"),
                        ("3.", "Engine Instruments", "COMPLETE"),
                        ("4.", "Altitude", "COMPLETE"),
                        ("5.", "Radios", "COMPLETE"),
                        ("6.", "Orientation", "COMPLETE"),
                        ("7.", "Fuel Log", "COMPLETE"),
                        ("8.", "Forced Landing", "COMPLETE"),
                    ],
                }
            ],
        },
        {
            "title": "B10.0 PRE-DIVERSION",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Weather", "CONSIDERED"),
                        ("2.", "End Of Daylight", "CONSIDERED"),
                        ("3.", "LSALT", "CONSIDERED"),
                        ("4.", "Fuel", "CONSIDERED"),
                        ("5.", "Airspace", "CONSIDERED"),
                        ("6.", "SARWATCH", "CONSIDERED"),
                        ("7.", "Transmit", "CONSIDERED"),
                    ],
                }
            ],
        },
        {
            "title": "B11.0 INBOUND (NAVIGATION)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Avionics", "CHECKED & SET"),
                        ("2.", "Weather Brief (Weather Phenomena, Cloud, Visibility, Wind, Temperature, QNH)", "COMPLETE"),
                        ("3.", "Aerodrome Brief", "COMPLETE (If Joining The Circuit Or Visual Circling)"),
                        ("4.", "Procedure Brief", "COMPLETE"),
                        ("5.", "Threat Brief", "COMPLETE"),
                    ],
                }
            ],
        },
        {
            "title": "B12.0 PRE-APPROACH (IFR)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Mode", "GPS & OBS"),
                        ("2.", "Integrity", "MONITORED"),
                        ("3.", "Speed", "SET"),
                        ("4.", "Timer", "READY"),
                        ("5.", "QNH", "SET"),
                    ],
                }
            ],
        },
        {
            "title": "B13.0 HOLDING PATTERN (IFR)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Timer", "START OR READY"),
                        ("2.", "Track", "CRS SET"),
                        ("3.", "Turn", "HDG & AIRCRAFT"),
                        ("4.", "Integrity", "MONITORED"),
                        ("5.", "Altitude", "SET"),
                        ("6.", "Transmit", "AS REQUIRED"),
                    ],
                }
            ],
        },
        {
            "title": "B14.0 TIMER RUNNING (IFR)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "20 Seconds Remaining", "CRS SET"),
                        ("2.", "10 Seconds Remaining", "HDG SET"),
                    ],
                }
            ],
        },
        {
            "title": "B15.0 RNP WAYPOINT (IFR)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Passing", "[WAYPOINT]"),
                        ("2.", "Tracking To", "[WAYPOINT]"),
                        ("3.", "Distance", "[DISTANCE] MILES"),
                        ("4.", "Tracking", "[TRACK] DEGREES"),
                        ("5.", "Altitude", "[ALTITUDE] FEET"),
                        ("6.", "RAIM Warnings", "NIL"),
                    ],
                }
            ],
        },
        {
            "title": "B16.0 AIRFIELD APPROACH",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "ATIS OR AWIS", "OBTAINED"),
                        ("2.", "Fuel", "BOTH & QTY GAL SUFFICIENT"),
                        ("3.", "Radio", "FREQUENCY SET"),
                        ("4.", "Engine Instruments", "GREEN"),
                        ("5.", "CRS", "ALIGNED WITH RUNWAY"),
                        ("6.", "HDG", "ALIGNED WITH RUNWAY (If Aerodrome In Sight)"),
                        ("7.", "Airframe", "FLAPS UP, GEAR FIXED"),
                        ("8.", "Altimeters (PFD & STBY)", "QNH SET"),
                        ("9.", "Transponder", "CODE SET"),
                    ],
                }
            ],
        },
        {
            "title": "B17.0 FINAL APPROACH FIX / POINT (IFR)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Approach", "ESTABLISHED"),
                        ("2.", "Integrity", "MONITORED"),
                        ("3.", "Missed Approach", "HDG & ALTITUDE SET"),
                    ],
                }
            ],
        },
        {
            "title": "B18.0 POST-AIRWORK (IFR)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Altitude", "CHECKED & SET"),
                        ("2.", "Tracking", "CHECKED & SET"),
                        ("3.", "Avionics", "CHECKED & SET"),
                    ],
                }
            ],
        },
        {
            "title": "B19.0 DOWNWIND",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Track", "PARALLEL WITH RUNWAY"),
                        ("2.", "Altitude", "SET & MAINTAINED"),
                        ("3.", "Power", "SET"),
                        ("4.", "Spacing", "[ONE HALF OR ONE THIRD] WINGSTRUT"),
                    ],
                }
            ],
        },
        {
            "title": "B20.0 BEFORE LANDING",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Fuel (Selector & QTY GAL)", "BOTH & SUFFICIENT"),
                        ("2.", "Mixture", "FULL RICH"),
                        ("3.", "Gear", "FIXED"),
                        ("4.", "Brakes", "PRESSURE CHECKED & OFF"),
                        ("5.", "Auto Pilot", "OFF"),
                        ("6.", "Switches", "MAGNETOS BOTH, LIGHTS ON, PITOT HEAT AS REQUIRED, CABIN POWER OFF"),
                        ("7.", "Security", "SEATBELTS & DOORS SECURE"),
                    ],
                }
            ],
        },
        {
            "title": "B21.0 FLAP EXTENSION & RETRACTION",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": "FLAP EXTENSION",
                    "items": [
                        ("1.", "Speed Below 110 KIAS", "FLAPS 10°"),
                        ("2.", "Speed Below 85 KIAS", "FLAPS 20°"),
                        ("3.", "Speed Below 85 KIAS", "FLAPS FULL"),
                    ],
                },
                {
                    "subtitle": "FLAP RETRACTION",
                    "items": [
                        ("1.", "Flaps Identified", "FLAPS 20°"),
                        ("2.", "Positive Rate Of Climb, Flaps Identified", "FLAPS 10°"),
                        ("3.", "Speed Above 60 KIAS, Flaps Identified", "FLAPS UP"),
                    ],
                },
            ],
        },
        {
            "title": "B22.0 FINAL APPROACH",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Final Approach", "ESTABLISHED"),
                        ("2.", "Flaps", "FULL"),
                    ],
                }
            ],
        },
        {
            "title": "B23.0 LANDING (300' AGL)",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Approach", "STABILISED"),
                        ("2.", "Heels", "ON THE FLOOR"),
                        ("3.", "Clearance", "RECEIVED (Or Pending)"),
                        ("4.", "Runway", "CLEAR (Or Occupied)"),
                        ("5.", "Windsock", "CHECKED"),
                    ],
                }
            ],
        },
        {
            "title": "B24.0 GO-AROUND & MISSED APPROACH",
            "recall_box": True,
            "subsections": [
                {
                    "subtitle": None,
                    "items": [
                        ("1.", "Power", "FULL"),
                        ("2.", "Attitude", "SET"),
                        ("3.", "Flaps", "RETRACT"),
                        ("4.", "Transmit", "AS REQUIRED"),
                    ],
                }
            ],
        },
    ],
}


@st.cache_data(show_spinner=False)
def generate_tts_base64(text, voice):
    async def _gen():
        communicate = edge_tts.Communicate(text, voice)
        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]
        return audio_bytes

    audio_data = asyncio.run(_gen())
    return base64.b64encode(audio_data).decode("utf-8")


@st.cache_data(show_spinner=False)
def generate_tts_batch_base64(texts_tuple, voice):
    async def _fetch_one(sem, text):
        async with sem:
            try:
                communicate = edge_tts.Communicate(text, voice)
                audio_bytes = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_bytes += chunk["data"]
                return base64.b64encode(audio_bytes).decode("utf-8")
            except Exception:
                return ""

    async def _run_all():
        sem = asyncio.Semaphore(6)
        return await asyncio.gather(*(_fetch_one(sem, t) for t in texts_tuple))

    return asyncio.run(_run_all())


def clean_for_speech(text):
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = text.replace("[", "").replace("]", "")
    return " ".join(text.split())


def build_section_speech(section):
    clean_title = re.sub(r"^[AB]\d+\.\d+\s*", "", section["title"]).strip()
    parts = [f"{clean_title} checklist."]

    for subsection in section["subsections"]:
        if subsection.get("subtitle"):
            parts.append(f"{subsection['subtitle']}.")
        for _, item, action in subsection["items"]:
            parts.append(f"{clean_for_speech(item)}, {clean_for_speech(action)}.")

    closing = section.get("footer") or f"{clean_title} checklist complete."
    parts.append(closing)
    return " ".join(parts)


def format_item_html(num, item, highlight=False):
    if highlight:
        highlighted = re.sub(
            r"^(\[?)(\d+|[A-Za-z])",
            r'\1<mark style="background-color: #FFF000; color: #000000; padding: 0 2px;">\2</mark>',
            item,
            count=1,
        )
        return f"<b>{num} {highlighted}</b>"
    return f"<b>{num} {item}</b>"


def reset_all():
    for key in list(st.session_state.keys()):
        if key.startswith("chk_"):
            st.session_state[key] = False
    st.session_state.audio_event = None
    st.session_state.active_section_audio = None
    st.session_state.active_voice_runner = None


def reset_section(section_keys, section_title):
    for key in section_keys:
        st.session_state[key] = False
    st.session_state.audio_event = None
    if st.session_state.get("active_section_audio") == section_title:
        st.session_state.active_section_audio = None
    if st.session_state.get("active_voice_runner") == section_title:
        st.session_state.active_voice_runner = None


def on_item_click(key, item, action, section_title, footer, section_keys):
    new_state = not st.session_state.get(key, False)
    st.session_state[key] = new_state

    if not new_state:
        return

    spoken_item = f"{clean_for_speech(item)}, {clean_for_speech(action)}"
    all_done = all(st.session_state.get(k, False) for k in section_keys)

    if all_done:
        closing = footer if footer else f"{section_title} complete"
        st.session_state.audio_event = {
            "type": "complete",
            "text": f"{spoken_item}. {closing}",
            "ts": time.time(),
        }
    else:
        st.session_state.audio_event = {
            "type": "tick",
            "text": spoken_item,
            "ts": time.time(),
        }


def play_audio_cue(event, enable_beep, enable_speech, voice, speed):
    if not event or (not enable_beep and not enable_speech):
        return

    event_type = json.dumps(event["type"])
    beep_flag = "true" if enable_beep else "false"

    audio_b64 = ""
    if enable_speech:
        try:
            audio_b64 = generate_tts_base64(event["text"], voice)
        except Exception:
            audio_b64 = ""

    js_code = f"""
    <script>
    // ts: {event["ts"]}
    (function() {{
        const playBeep = {beep_flag};
        const type = {event_type};
        const audioB64 = "{audio_b64}";
        const rate = {speed};

        if (playBeep) {{
            try {{
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                const ctx = new AudioCtx();
                const now = ctx.currentTime;

                if (type === "tick") {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = "sine";
                    osc.frequency.setValueAtTime(880, now);
                    gain.gain.setValueAtTime(0.12, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now);
                    osc.stop(now + 0.08);
                }} else if (type === "complete") {{
                    [523.25, 783.99].forEach((freq, i) => {{
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = "sine";
                        osc.frequency.setValueAtTime(freq, now + i * 0.14);
                        gain.gain.setValueAtTime(0.15, now + i * 0.14);
                        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.14 + 0.25);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start(now + i * 0.14);
                        osc.stop(now + i * 0.14 + 0.25);
                    }});
                }}
            }} catch (e) {{}}
        }}

        if (audioB64) {{
            const audio = new Audio("data:audio/mp3;base64," + audioB64);
            audio.playbackRate = rate;
            audio.play().catch(() => {{}});
        }}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


def render_section_player(section, voice, speed):
    try:
        audio_b64 = generate_tts_base64(build_section_speech(section), voice)
    except Exception:
        st.error("Could not load audio for this section.")
        return

    player_html = f"""
    <div style="display: flex; align-items: center; padding: 2px 0;">
        <audio id="secPlayer" controls autoplay style="width: 100%; height: 38px;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
    </div>
    <script>
        const player = document.getElementById("secPlayer");
        if (player) {{
            player.playbackRate = {speed};
            player.play().catch(() => {{}});
        }}
    </script>
    """
    components.html(player_html, height=48)


VOICE_RUNNER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
  * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { margin: 0; padding: 4px 2px; background: transparent; color: __FG__; }
  .card {
    background: __CARD_BG__;
    border: 2px solid __BORDER__;
    border-radius: 10px;
    padding: 14px 16px;
  }
  .top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 10px;
  }
  .badge {
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
    background: __BADGE_BG__;
    color: __BADGE_FG__;
    letter-spacing: 0.2px;
  }
  .progress-text {
    font-size: 13px;
    font-weight: 700;
    color: __MUTED__;
  }
  .prompt-box {
    background: __PROMPT_BG__;
    border: 1px solid __BORDER__;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
  }
  .sub-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: __MUTED__;
    margin-bottom: 4px;
  }
  .line-flex {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 14px;
    flex-wrap: wrap;
  }
  .item-text {
    font-size: 17px;
    font-weight: 700;
    color: __FG__;
  }
  .action-text {
    font-size: 17px;
    font-weight: 800;
    text-align: right;
    color: __FG__;
  }
  .action-hidden { color: __MUTED__; letter-spacing: 2px; }
  .action-matched { color: __GREEN__; }
  .status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    padding: 8px 12px;
    border-radius: 8px;
    background: __STATUS_BG__;
    margin-bottom: 12px;
    font-size: 13px;
  }
  .status-left { font-weight: 700; display: flex; align-items: center; gap: 8px; }
  .dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: __MUTED__; display: inline-block;
  }
  .dot.speaking { background: #3B82F6; }
  .dot.listening { background: #EF4444; animation: pulse 1.1s infinite; }
  .dot.matched { background: __GREEN__; }
  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.35); opacity: 0.5; }
    100% { transform: scale(1); opacity: 1; }
  }
  .heard {
    font-style: italic;
    color: __MUTED__;
    max-width: 58%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .controls {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 10px;
  }
  button {
    cursor: pointer;
    border-radius: 7px;
    border: 1px solid __BORDER__;
    background: __BTN_BG__;
    color: __FG__;
    font-size: 13px;
    font-weight: 700;
    padding: 8px 12px;
    transition: opacity 0.15s ease;
  }
  button:hover { opacity: 0.86; }
  button.primary {
    background: __GREEN__;
    color: #000000;
    border-color: __GREEN__;
  }
  .list-wrap {
    max-height: 145px;
    overflow-y: auto;
    border-top: 1px solid __BORDER__;
    padding-top: 8px;
  }
  .row {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    font-size: 13px;
    padding: 4px 6px;
    border-radius: 5px;
  }
  .row.active { background: __ACTIVE_ROW__; font-weight: 700; }
  .row.done .r-act { color: __GREEN__; font-weight: 700; }
  .r-act { text-align: right; font-weight: 700; }
  .hint {
    margin-top: 8px;
    font-size: 11.5px;
    color: __MUTED__;
  }
</style>
</head>
<body>
<div class="card">
  <div class="top-row">
    <span class="badge" id="modeBadge"></span>
    <span class="progress-text" id="progressText"></span>
  </div>

  <div class="prompt-box">
    <div class="sub-label" id="subLabel"></div>
    <div class="line-flex">
      <div class="item-text" id="itemText"></div>
      <div class="action-text" id="actionText"></div>
    </div>
  </div>

  <div class="status-bar">
    <div class="status-left">
      <span class="dot" id="statusDot"></span>
      <span id="statusText">Ready — click Start to begin</span>
    </div>
    <div class="heard" id="heardText"></div>
  </div>

  <div class="controls">
    <button class="primary" id="startBtn">▶ Start Voice Session</button>
    <button id="repeatBtn">🔁 Repeat</button>
    <button id="confirmBtn">✓ Confirm</button>
    <button id="skipBtn">⏭ Skip</button>
    <button id="restartBtn">↺ Restart</button>
  </div>

  <div class="list-wrap" id="itemList"></div>
  <div class="hint" id="hintText"></div>
</div>

<script>
const CFG = __CONFIG_JSON__;
const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;

let idx = 0;
let running = false;
let paused = false;
let phase = "idle"; // idle | speaking | listening | matched | done
let revealed = false;
let fatalMicError = false;
let currentAudio = null;
let recognition = null;
let audioCtx = null;
let advanceTimer = null;
let restartRecTimer = null;
let doneMap = new Array(CFG.items.length).fill(false);

const modeBadge = document.getElementById("modeBadge");
const progressText = document.getElementById("progressText");
const subLabel = document.getElementById("subLabel");
const itemText = document.getElementById("itemText");
const actionText = document.getElementById("actionText");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const heardText = document.getElementById("heardText");
const startBtn = document.getElementById("startBtn");
const repeatBtn = document.getElementById("repeatBtn");
const confirmBtn = document.getElementById("confirmBtn");
const skipBtn = document.getElementById("skipBtn");
const restartBtn = document.getElementById("restartBtn");
const itemList = document.getElementById("itemList");
const hintText = document.getElementById("hintText");

modeBadge.textContent = CFG.strictMode
  ? "🎙️ STRICT RECALL — Speak Response"
  : "🎙️ CONFIRM MODE — Say 'Checked'";

hintText.textContent = CFG.strictMode
  ? "Luna reads the left-hand item. Speak the right-hand response to advance. Voice commands: 'repeat', 'skip'."
  : "Luna reads the full line. Say 'checked' (or 'set', 'roger', 'next') to advance. Voice commands: 'repeat', 'skip'.";

const CONFIRM_WORDS = new Set([
  "checked", "check", "set", "roger", "next", "done",
  "copy", "confirm", "confirmed", "ok", "okay", "yes", "checked."
]);

const FILLER_WORDS = new Set([
  "the", "is", "are", "a", "an", "to", "of", "for", "and", "with", "be"
]);

function normalizeText(str) {
  let s = (str || "").toLowerCase();
  s = s.replace(/°/g, " degrees ");
  s = s.replace(/&/g, " and ");
  s = s.replace(/[-/]/g, " ");
  s = s.replace(/cut\s*off/g, "cutoff");
  s = s.replace(/q\s*(and|n)\s*h/g, "qnh");
  s = s.replace(/r\s*p\s*m/g, "rpm");
  s = s.replace(/k\s*i\s*a\s*s/g, "knots");
  s = s.replace(/kias/g, "knots");
  s = s.replace(/kts/g, "knots");
  s = s.replace(/stby/g, "standby");
  s = s.replace(/hdg/g, "heading");
  s = s.replace(/crs/g, "course");
  s = s.replace(/kneel/g, "nil");
  s = s.replace(/stabilized/g, "stabilised");
  s = s.replace(/(\d+)mm/g, "$1 mm");
  s = s.replace(/\bmillimeters?\b|\bmillimetres?\b/g, "mm");
  s = s.replace(/\bone\s+thousand\b/g, "1000");
  s = s.replace(/\bthree\s+thousand\b/g, "3000");
  s = s.replace(/\beighteen\s+hundred\b/g, "1800");
  s = s.replace(/\bone\s+thousand\s+eight\s+hundred\b/g, "1800");
  s = s.replace(/\bsix\s+hundred\b/g, "600");
  s = s.replace(/\beight\s+hundred\b/g, "800");
  s = s.replace(/\bone\s+seventy\s+five\b|\bone\s+hundred\s+seventy\s+five\b/g, "175");
  s = s.replace(/\bone\s+fifty\b|\bone\s+hundred\s+fifty\b/g, "150");
  s = s.replace(/\bone\s+ten\b|\bone\s+hundred\s+ten\b/g, "110");
  s = s.replace(/\beighty\s+five\b/g, "85");
  s = s.replace(/\bsixty\b/g, "60");
  s = s.replace(/\bfifty\b/g, "50");
  s = s.replace(/\bthirty\b/g, "30");
  s = s.replace(/\btwenty\s+eight\b/g, "28");
  s = s.replace(/\btwenty\s+five\b/g, "25");
  s = s.replace(/\btwenty\s+four\b/g, "24");
  s = s.replace(/\btwenty\b/g, "20");
  s = s.replace(/\bten\b/g, "10");
  s = s.replace(/\beight\b/g, "8");
  s = s.replace(/\bsix\b/g, "6");
  s = s.replace(/\bthree\b/g, "3");
  s = s.replace(/\btwo\b/g, "2");
  s = s.replace(/\bone\b/g, "1");
  s = s.replace(/\bzero\b/g, "0");
  s = s.replace(/[^a-z0-9\s]/g, " ");
  return s.replace(/\s+/g, " ").trim();
}

function tokenMatch(spokenTok, targetTok) {
  if (spokenTok === targetTok) return true;
  if (targetTok === "nil" && (spokenTok === "none" || spokenTok === "0" || spokenTok === "no")) return true;
  if (targetTok === "crs" && (spokenTok === "course" || spokenTok === "gps")) return true;
  if (targetTok === "course" && spokenTok === "crs") return true;
  if (targetTok === "heading" && spokenTok === "hdg") return true;
  if (targetTok === "mm" && spokenTok === "millimeter") return true;
  if (targetTok.length >= 4 && spokenTok.length >= 4) {
    if (spokenTok.startsWith(targetTok.slice(0, 4)) || targetTok.startsWith(spokenTok.slice(0, 4))) {
      return true;
    }
  }
  return false;
}

function matchesSingleOption(spokenNorm, optionRaw) {
  const optNorm = normalizeText(optionRaw);
  if (!optNorm) return false;
  let targetTokens = optNorm.split(" ");
  if (targetTokens.length > 2) {
    const filtered = targetTokens.filter(t => !FILLER_WORDS.has(t));
    if (filtered.length > 0) targetTokens = filtered;
  }
  const spokenTokens = spokenNorm.split(" ").filter(Boolean);
  if (spokenTokens.length === 0) return false;

  let hits = 0;
  for (const t of targetTokens) {
    if (spokenTokens.some(s => tokenMatch(s, t))) hits++;
  }

  let needed;
  if (targetTokens.length === 1) needed = 1;
  else if (targetTokens.length === 2) {
    needed = (targetTokens[1] === "range" || targetTokens[1] === "degrees" || targetTokens[1] === "feet" || targetTokens[1] === "miles") ? 1 : 2;
  } else if (targetTokens.length <= 4) {
    needed = Math.ceil(targetTokens.length * 0.6);
  } else {
    needed = Math.ceil(targetTokens.length * 0.45);
  }
  return hits >= needed;
}

function checkSpeechMatch(transcript, itemObj, isFinal) {
  const norm = normalizeText(transcript);
  if (!norm) return null;

  if (/\b(repeat|say again)\b/.test(norm)) return "REPEAT";
  if (/\bskip\b/.test(norm)) return "SKIP";

  if (!CFG.strictMode) {
    const tokens = norm.split(" ");
    if (tokens.some(t => CONFIRM_WORDS.has(t))) return "MATCH";
    return null;
  }

  // Pure variable placeholder like [WAYPOINT]
  if (/^\[[^\]]+\]$/.test(itemObj.action.trim()) && !/\bOR\b/i.test(itemObj.action)) {
    return (isFinal && norm.length >= 2) ? "MATCH" : null;
  }

  // Choice items containing "OR"
  const clean = itemObj.cleanAction;
  if (/\bOR\b/i.test(clean)) {
    const options = clean.split(/\bOR\b/i).map(s => s.trim()).filter(Boolean);
    if (options.some(opt => matchesSingleOption(norm, opt))) return "MATCH";
    return null;
  }

  if (matchesSingleOption(norm, clean)) return "MATCH";
  return null;
}

function ensureAudioCtx() {
  if (!audioCtx) {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (Ctx) audioCtx = new Ctx();
  }
  if (audioCtx && audioCtx.state === "suspended") {
    audioCtx.resume().catch(() => {});
  }
}

function playBeep(type) {
  if (!CFG.enableBeep) return;
  try {
    ensureAudioCtx();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    if (type === "tick") {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(880, now);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.08);
    } else if (type === "complete") {
      [523.25, 783.99].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, now + i * 0.14);
        gain.gain.setValueAtTime(0.15, now + i * 0.14);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.14 + 0.25);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now + i * 0.14);
        osc.stop(now + i * 0.14 + 0.25);
      });
    }
  } catch (e) {}
}

function stopRecognition() {
  clearTimeout(restartRecTimer);
  if (recognition) {
    try {
      recognition.onresult = null;
      recognition.onerror = null;
      recognition.onend = null;
      recognition.abort();
    } catch (e) {}
    recognition = null;
  }
}

function stopAudio() {
  clearTimeout(advanceTimer);
  if (currentAudio) {
    try {
      currentAudio.onended = null;
      currentAudio.pause();
      currentAudio = null;
    } catch (e) {}
  }
}

function setStatus(dotClass, text) {
  statusDot.className = "dot" + (dotClass ? " " + dotClass : "");
  statusText.textContent = text;
}

function renderUI() {
  const doneCount = doneMap.filter(Boolean).length;
  progressText.textContent = doneCount + " / " + CFG.items.length + " done";

  if (phase === "done") {
    subLabel.textContent = "CHECKLIST COMPLETE";
    itemText.textContent = CFG.closingText;
    actionText.textContent = "✓";
    actionText.className = "action-text action-matched";
  } else {
    const cur = CFG.items[idx];
    subLabel.textContent = cur.subtitle ? cur.subtitle : CFG.sectionTitle;
    itemText.textContent = cur.num + " " + cur.item;

    if (CFG.strictMode && !revealed && !doneMap[idx]) {
      actionText.textContent = "•••••";
      actionText.className = "action-text action-hidden";
    } else {
      actionText.textContent = cur.action;
      actionText.className = "action-text" + ((doneMap[idx] || phase === "matched") ? " action-matched" : "");
    }
  }

  startBtn.textContent = running && !paused ? "⏸ Pause" : (phase === "done" ? "↺ Run Again" : "▶ Start Voice Session");

  itemList.innerHTML = "";
  CFG.items.forEach((it, i) => {
    const row = document.createElement("div");
    row.className = "row" + (i === idx && phase !== "done" ? " active" : "") + (doneMap[i] ? " done" : "");
    const left = document.createElement("span");
    left.textContent = (doneMap[i] ? "✓ " : "") + it.num + " " + it.item;
    const right = document.createElement("span");
    right.className = "r-act";
    right.textContent = (CFG.strictMode && !doneMap[i]) ? "•••••" : it.action;
    row.appendChild(left);
    row.appendChild(right);
    row.onclick = () => {
      if (running) {
        stopRecognition();
        stopAudio();
        runItem(i);
      } else {
        idx = i;
        phase = "idle";
        renderUI();
      }
    };
    itemList.appendChild(row);
    if (i === idx && phase !== "done") {
      row.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  });
}

function startListening(targetIdx) {
  if (!running || paused || idx !== targetIdx) return;
  stopRecognition();

  if (!SpeechRec) {
    setStatus("", "Speech recognition requires Chrome or Edge — use ✓ Confirm");
    return;
  }
  if (fatalMicError) {
    setStatus("", "Mic blocked — allow microphone access or use ✓ Confirm");
    return;
  }

  phase = "listening";
  setStatus("listening", CFG.strictMode ? "Listening for response..." : "Listening for 'Checked'...");

  try {
    recognition = new SpeechRec();
    recognition.lang = "en-SG";
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 3;

    recognition.onresult = (event) => {
      if (!running || paused || phase !== "listening" || idx !== targetIdx) return;
      let latestTranscript = "";

      for (let r = event.resultIndex; r < event.results.length; r++) {
        const res = event.results[r];
        const isFinal = res.isFinal;
        for (let a = 0; a < res.length; a++) {
          const text = res[a].transcript || "";
          if (a === 0) latestTranscript = text;
          const decision = checkSpeechMatch(text, CFG.items[targetIdx], isFinal);
          if (decision === "MATCH") {
            heardText.textContent = 'Heard: "' + text.trim() + '"';
            completeItem(targetIdx, false);
            return;
          } else if (decision === "REPEAT" && isFinal) {
            heardText.textContent = 'Heard: "' + text.trim() + '"';
            stopRecognition();
            runItem(targetIdx);
            return;
          } else if (decision === "SKIP" && isFinal) {
            heardText.textContent = 'Heard: "' + text.trim() + '"';
            completeItem(targetIdx, true);
            return;
          }
        }
      }
      if (latestTranscript.trim()) {
        heardText.textContent = 'Heard: "' + latestTranscript.trim() + '"';
      }
    };

    recognition.onerror = (event) => {
      if (event.error === "not-allowed" || event.error === "service-not-allowed") {
        fatalMicError = true;
        setStatus("", "Mic permission denied — allow mic in browser bar or use ✓ Confirm");
        stopRecognition();
      }
    };

    recognition.onend = () => {
      if (running && !paused && phase === "listening" && idx === targetIdx && !fatalMicError) {
        restartRecTimer = setTimeout(() => startListening(targetIdx), 250);
      }
    };

    recognition.start();
  } catch (e) {
    setStatus("", "Could not start mic — use ✓ Confirm");
  }
}

function runItem(targetIdx) {
  stopRecognition();
  stopAudio();

  if (targetIdx >= CFG.items.length) {
    finishSession();
    return;
  }

  idx = targetIdx;
  revealed = false;
  heardText.textContent = "";
  phase = "speaking";
  setStatus("speaking", "Luna speaking...");
  renderUI();

  const b64 = CFG.items[idx].audioB64;
  if (!b64) {
    advanceTimer = setTimeout(() => startListening(idx), 250);
    return;
  }

  currentAudio = new Audio("data:audio/mp3;base64," + b64);
  currentAudio.playbackRate = CFG.speed;
  currentAudio.onended = () => {
    if (!running || paused || idx !== targetIdx) return;
    advanceTimer = setTimeout(() => startListening(targetIdx), 220);
  };
  currentAudio.play().catch(() => {
    running = false;
    phase = "idle";
    setStatus("", "Click ▶ Start Voice Session to enable audio & mic");
    renderUI();
  });
}

function completeItem(targetIdx, skipped) {
  stopRecognition();
  stopAudio();
  doneMap[targetIdx] = true;
  revealed = true;
  phase = "matched";

  const isLast = targetIdx >= CFG.items.length - 1;
  if (!skipped && !isLast) {
    playBeep("tick");
  }
  setStatus("matched", skipped ? "Skipped" : "Checked!");
  renderUI();

  advanceTimer = setTimeout(() => {
    if (running && !paused) {
      runItem(targetIdx + 1);
    }
  }, 450);
}

function finishSession() {
  stopRecognition();
  stopAudio();
  running = false;
  paused = false;
  phase = "done";
  playBeep("complete");
  setStatus("matched", "Checklist complete!");
  renderUI();

  if (CFG.closingAudio) {
    currentAudio = new Audio("data:audio/mp3;base64," + CFG.closingAudio);
    currentAudio.playbackRate = CFG.speed;
    currentAudio.play().catch(() => {});
  }
}

startBtn.onclick = () => {
  ensureAudioCtx();
  fatalMicError = false;
  if (phase === "done") {
    doneMap = new Array(CFG.items.length).fill(false);
    idx = 0;
    running = true;
    paused = false;
    runItem(0);
    return;
  }
  if (!running || paused) {
    running = true;
    paused = false;
    runItem(idx);
  } else {
    paused = true;
    stopRecognition();
    stopAudio();
    setStatus("", "Paused");
    renderUI();
  }
};

repeatBtn.onclick = () => {
  ensureAudioCtx();
  if (phase === "done") return;
  running = true;
  paused = false;
  runItem(idx);
};

confirmBtn.onclick = () => {
  ensureAudioCtx();
  if (phase === "done") return;
  if (!running) {
    running = true;
    paused = false;
  }
  completeItem(idx, false);
};

skipBtn.onclick = () => {
  ensureAudioCtx();
  if (phase === "done") return;
  if (!running) {
    running = true;
    paused = false;
  }
  completeItem(idx, true);
};

restartBtn.onclick = () => {
  ensureAudioCtx();
  stopRecognition();
  stopAudio();
  doneMap = new Array(CFG.items.length).fill(false);
  idx = 0;
  running = true;
  paused = false;
  fatalMicError = false;
  runItem(0);
};

renderUI();
</script>
</body>
</html>
"""


def render_voice_runner(section, voice, speed, enable_beep, strict_mode, night_mode):
    clean_title = re.sub(r"^[AB]\d+\.\d+\s*", "", section["title"]).strip()
    closing_text = section.get("footer") or f"{clean_title} checklist complete"

    flat_items = []
    prompts = []
    for subsection in section["subsections"]:
        sub = subsection.get("subtitle")
        for num, item, action in subsection["items"]:
            clean_item = clean_for_speech(item)
            clean_action = clean_for_speech(action)
            prompt = f"{clean_item}." if strict_mode else f"{clean_item}, {clean_action}."
            flat_items.append(
                {
                    "num": num,
                    "item": item,
                    "action": action,
                    "cleanAction": clean_action,
                    "subtitle": sub,
                }
            )
            prompts.append(prompt)

    prompts.append(closing_text)

    with st.spinner("Preparing Luna's voice prompts..."):
        clips = generate_tts_batch_base64(tuple(prompts), voice)

    for i, item_obj in enumerate(flat_items):
        item_obj["audioB64"] = clips[i] if i < len(clips) else ""
    closing_audio = clips[-1] if clips else ""

    config = {
        "sectionTitle": section["title"],
        "strictMode": strict_mode,
        "speed": speed,
        "enableBeep": enable_beep,
        "closingText": closing_text,
        "closingAudio": closing_audio,
        "items": flat_items,
    }

    if night_mode:
        palette = {
            "__FG__": "#E6EDF3",
            "__CARD_BG__": "#161B22",
            "__BORDER__": "#30363D",
            "__BADGE_BG__": "#21262D",
            "__BADGE_FG__": "#E6EDF3",
            "__MUTED__": "#9CA3AF",
            "__PROMPT_BG__": "#0E1117",
            "__STATUS_BG__": "#0E1117",
            "__BTN_BG__": "#21262D",
            "__GREEN__": "#00E676",
            "__ACTIVE_ROW__": "rgba(255, 255, 255, 0.08)",
        }
    else:
        palette = {
            "__FG__": "#111827",
            "__CARD_BG__": "#F9FAFB",
            "__BORDER__": "#D1D5DB",
            "__BADGE_BG__": "#E5E7EB",
            "__BADGE_FG__": "#111827",
            "__MUTED__": "#6B7280",
            "__PROMPT_BG__": "#FFFFFF",
            "__STATUS_BG__": "#FFFFFF",
            "__BTN_BG__": "#FFFFFF",
            "__GREEN__": "#00C853",
            "__ACTIVE_ROW__": "rgba(0, 0, 0, 0.06)",
        }

    html = VOICE_RUNNER_TEMPLATE
    for token, val in palette.items():
        html = html.replace(token, val)
    config_json = json.dumps(config).replace("</", "<\\/")
    html = html.replace("__CONFIG_JSON__", config_json)

    components.html(html, height=400)


def render_subsection(
    section_title,
    sub_idx,
    subsection,
    footer,
    section_keys,
    highlight=False,
    is_recall_area=False,
    recall_mode=False,
):
    completed = 0
    total = 0

    if subsection["subtitle"]:
        st.markdown(f"**<u>{subsection['subtitle']}</u>**", unsafe_allow_html=True)
    if subsection.get("subnote"):
        st.markdown(f"**{subsection['subnote']}**")
    if subsection.get("note"):
        st.info(f"**NOTE:** {subsection['note']}")

    for i_idx, (num, item, action) in enumerate(subsection["items"]):
        total += 1
        key = f"chk_{section_title}_{sub_idx}_{i_idx}"
        is_checked = st.session_state.get(key, False)

        if is_checked:
            completed += 1

        safe_action = action.replace("[", r"\[").replace("]", r"\]")
        if recall_mode and is_recall_area and not is_checked:
            action_label = "*•••••*"
        elif is_checked:
            action_label = f":green[**{safe_action}**]"
        else:
            action_label = f"**{safe_action}**"

        col1, col2 = st.columns([5, 5], vertical_alignment="center")

        with col1:
            st.markdown(format_item_html(num, item, highlight), unsafe_allow_html=True)
        with col2:
            st.button(
                action_label,
                key=f"act_{section_title}_{sub_idx}_{i_idx}",
                on_click=on_item_click,
                args=(key, item, action, section_title, footer, section_keys),
                use_container_width=True,
            )

    return total, completed


if "audio_event" not in st.session_state:
    st.session_state.audio_event = None
if "active_section_audio" not in st.session_state:
    st.session_state.active_section_audio = None
if "active_voice_runner" not in st.session_state:
    st.session_state.active_voice_runner = None

st.title("C172R&S G1000 Normal Checklist")

with st.sidebar:
    st.header("Navigation")
    selected_part = st.radio("Select Part", list(CHECKLIST_PARTS.keys()))
    section_titles = ["Show All"] + [s["title"] for s in CHECKLIST_PARTS[selected_part]]
    selected_section = st.selectbox("Jump to Checklist", section_titles)
    st.divider()

    st.header("Audio Cues")
    enable_beep = st.toggle("Beeps & Completion Chime", value=True)
    enable_speech = st.toggle("Spoken Callouts", value=True)
    selected_voice_label = st.selectbox("Voice", list(VOICE_OPTIONS.keys()))
    selected_voice = VOICE_OPTIONS[selected_voice_label]
    speech_speed = st.slider("Speaking Speed", 0.80, 1.30, 1.05, 0.05, format="%.2fx")
    strict_voice_recall = st.toggle(
        "Voice Runner: Strict Recall Mode",
        value=False,
        help="OFF: Luna reads the full line and waits for 'Checked'. ON: Luna reads only the left-hand item and waits for you to speak the response.",
    )

    if st.button("⬇️ Preload All Section Audio", use_container_width=True):
        all_sections = [
            section
            for sections in CHECKLIST_PARTS.values()
            for section in sections
        ]
        progress_bar = st.progress(0, text="Starting audio download...")
        total = len(all_sections)

        for idx, sec in enumerate(all_sections, start=1):
            progress_bar.progress(
                idx / total,
                text=f"Loading ({idx}/{total}): {sec['title']}",
            )
            try:
                generate_tts_base64(build_section_speech(sec), selected_voice)
            except Exception:
                pass

        progress_bar.empty()
        st.success("All section audio ready!")

    st.divider()
    st.header("Display")
    enable_highlights = st.toggle("Yellow Mnemonic Highlights", value=True)
    recall_mode = st.toggle("Recall Practice Mode", value=False)
    night_mode = st.toggle("Night / Low-Glare Cockpit Theme", value=False)
    st.divider()
    st.button("Reset All Items", on_click=reset_all, use_container_width=True)

if night_mode:
    theme_css = """
    <style>
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
        color: #E6EDF3 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
        color: #E6EDF3 !important;
    }
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #E6EDF3 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #21262D !important;
        color: #E6EDF3 !important;
        border-color: #30363D !important;
    }
    [data-testid="stAppViewContainer"] button,
    [data-testid="stSidebar"] button {
        background-color: #21262D !important;
        color: #E6EDF3 !important;
        border: 1px solid #30363D !important;
    }
    [data-testid="stAppViewContainer"] button:hover,
    [data-testid="stSidebar"] button:hover {
        background-color: #30363D !important;
    }
    [data-testid="stAppViewContainer"] code {
        background-color: #21262D !important;
        color: #E6EDF3 !important;
    }
    [data-testid="stAppViewContainer"] hr,
    [data-testid="stSidebar"] hr {
        border-color: #30363D !important;
    }
    [data-testid="stAlert"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        color: #E6EDF3 !important;
    }
    mark {
        background-color: #EAB308 !important;
        color: #000000 !important;
    }
    div[class*="st-key-recall_"] {
        border: 5px solid #E6EDF3 !important;
        border-radius: 2px !important;
        padding: 10px 14px !important;
        background-color: #161B22 !important;
    }
    div[class*="st-key-act_"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 2px 4px !important;
        min-height: 0px !important;
        justify-content: flex-end !important;
        text-align: right !important;
        color: #E6EDF3 !important;
    }
    div[class*="st-key-act_"] button p {
        font-weight: 700 !important;
        text-align: right !important;
        color: #E6EDF3 !important;
    }
    div[class*="st-key-act_"] button p span {
        color: #00E676 !important;
    }
    div[class*="st-key-act_"] button p em {
        color: #6B7280 !important;
        font-style: normal !important;
    }
    div[class*="st-key-act_"] button:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
    }
    </style>
    """
else:
    theme_css = """
    <style>
    div[class*="st-key-recall_"] {
        border: 5px solid #000000 !important;
        border-radius: 2px !important;
        padding: 10px 14px !important;
    }
    div[class*="st-key-act_"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 2px 4px !important;
        min-height: 0px !important;
        justify-content: flex-end !important;
        text-align: right !important;
        color: #000000 !important;
    }
    div[class*="st-key-act_"] button p {
        font-weight: 700 !important;
        text-align: right !important;
    }
    div[class*="st-key-act_"] button p span {
        color: #00C853 !important;
    }
    div[class*="st-key-act_"] button p em {
        color: #9CA3AF !important;
        font-style: normal !important;
    }
    div[class*="st-key-act_"] button:hover {
        background-color: rgba(0, 0, 0, 0.05) !important;
    }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

st.header(selected_part)

sections_to_show = CHECKLIST_PARTS[selected_part]
if selected_section != "Show All":
    sections_to_show = [s for s in sections_to_show if s["title"] == selected_section]

for section in sections_to_show:
    section_keys = [
        f"chk_{section['title']}_{sub_idx}_{i_idx}"
        for sub_idx, subsection in enumerate(section["subsections"])
        for i_idx in range(len(subsection["items"]))
    ]
    done_count = sum(1 for k in section_keys if st.session_state.get(k, False))
    total_count = len(section_keys)
    is_playing = st.session_state.active_section_audio == section["title"]
    is_voice_running = st.session_state.active_voice_runner == section["title"]

    hdr_col1, hdr_col2, hdr_col3, hdr_col4 = st.columns(
        [2.9, 1.0, 1.1, 1.0], vertical_alignment="center"
    )
    with hdr_col1:
        st.subheader(f"{section['title']}  `{done_count}/{total_count}`")
    with hdr_col2:
        if is_playing:
            if st.button("⏹ Stop", key=f"stop_sec_{section['title']}", use_container_width=True):
                st.session_state.active_section_audio = None
                st.rerun()
        else:
            if st.button("🔊 Play", key=f"play_sec_{section['title']}", use_container_width=True):
                st.session_state.active_section_audio = section["title"]
                st.session_state.active_voice_runner = None
                st.session_state.audio_event = None
                st.rerun()
    with hdr_col3:
        if is_voice_running:
            if st.button("⏹ End", key=f"end_vr_{section['title']}", use_container_width=True):
                st.session_state.active_voice_runner = None
                st.rerun()
        else:
            if st.button("🎙️ Voice", key=f"start_vr_{section['title']}", use_container_width=True):
                st.session_state.active_voice_runner = section["title"]
                st.session_state.active_section_audio = None
                st.session_state.audio_event = None
                st.rerun()
    with hdr_col4:
        st.button(
            "↺ Reset",
            key=f"reset_sec_{section['title']}",
            on_click=reset_section,
            args=(section_keys, section["title"]),
            use_container_width=True,
        )

    if is_playing:
        render_section_player(section, selected_voice, speech_speed)

    if is_voice_running:
        render_voice_runner(
            section,
            selected_voice,
            speech_speed,
            enable_beep,
            strict_voice_recall,
            night_mode,
        )

    if section.get("caution"):
        st.warning(f"**CAUTION:** {section['caution']}")
    if section.get("note"):
        st.info(f"**NOTE:** {section['note']}")

    total_items = 0
    completed_items = 0

    if section.get("recall_box"):
        with st.container(border=True, key=f"recall_sec_{section['title']}"):
            for sub_idx, subsection in enumerate(section["subsections"]):
                t, c = render_subsection(
                    section["title"],
                    sub_idx,
                    subsection,
                    section.get("footer"),
                    section_keys,
                    highlight=enable_highlights,
                    is_recall_area=True,
                    recall_mode=recall_mode,
                )
                total_items += t
                completed_items += c
    else:
        for sub_idx, subsection in enumerate(section["subsections"]):
            if subsection.get("recall"):
                with st.container(border=True, key=f"recall_sub_{section['title']}_{sub_idx}"):
                    t, c = render_subsection(
                        section["title"],
                        sub_idx,
                        subsection,
                        section.get("footer"),
                        section_keys,
                        is_recall_area=True,
                        recall_mode=recall_mode,
                    )
                    total_items += t
                    completed_items += c
            else:
                t, c = render_subsection(
                    section["title"],
                    sub_idx,
                    subsection,
                    section.get("footer"),
                    section_keys,
                )
                total_items += t
                completed_items += c

    if section.get("brief_text"):
        brief_html = section["brief_text"].replace("\n", "<br>")
        if section.get("brief_recall"):
            pic_checked = st.session_state.get(f"chk_{section['title']}_0_2", False)
            with st.container(border=True, key=f"recall_brief_{section['title']}"):
                if recall_mode and not pic_checked:
                    st.markdown(
                        "<div style='color: #9CA3AF; font-style: italic; text-align: center;'>"
                        "PIC Brief hidden in Recall Practice Mode — click item 3 to reveal</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(f"<i>{brief_html}</i>", unsafe_allow_html=True)
        else:
            st.markdown(f"> {section['brief_text'].replace(chr(10), '  ' + chr(10) + '> ')}")

    if section.get("footer"):
        if completed_items == total_items and total_items > 0:
            st.success(section["footer"])
        else:
            st.markdown(
                f"<div style='text-align: center; font-style: italic; margin-top: 8px;'>{section['footer']}</div>",
                unsafe_allow_html=True,
            )
    elif completed_items == total_items and total_items > 0:
        st.success(f"{section['title']} complete")

    if section.get("post_note"):
        st.info(f"**NOTE:** {section['post_note']}")

    st.divider()

if st.session_state.audio_event:
    play_audio_cue(
        st.session_state.audio_event,
        enable_beep,
        enable_speech,
        selected_voice,
        speech_speed,
    )
    st.session_state.audio_event = None
