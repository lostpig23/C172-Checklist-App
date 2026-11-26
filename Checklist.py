import streamlit as st

st.set_page_config(page_title="C172R&S G1000 Checklist Rev. 3.0", layout="centered")

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
                    "subtitle": "NORMAL START (Oil temperature below the green range, or after a failed start)",
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
                    "subtitle": "NORMAL START (Oil temperature within the green range, and first start attempt)",
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


def reset_all():
    for key in list(st.session_state.keys()):
        if key.startswith("chk_"):
            st.session_state[key] = False


st.title("C172R&S G1000 Normal Checklist")

with st.sidebar:
    st.header("Navigation")
    selected_part = st.radio("Select Part", list(CHECKLIST_PARTS.keys()))
    section_titles = ["Show All"] + [s["title"] for s in CHECKLIST_PARTS[selected_part]]
    selected_section = st.selectbox("Jump to Checklist", section_titles)
    st.divider()
    st.button("Reset All Checkboxes", on_click=reset_all, use_container_width=True)

st.header(selected_part)

sections_to_show = CHECKLIST_PARTS[selected_part]
if selected_section != "Show All":
    sections_to_show = [s for s in sections_to_show if s["title"] == selected_section]

for section in sections_to_show:
    st.subheader(section["title"])

    if section.get("caution"):
        st.warning(f"**CAUTION:** {section['caution']}")
    if section.get("note"):
        st.info(f"**NOTE:** {section['note']}")

    total_items = 0
    completed_items = 0

    for sub_idx, subsection in enumerate(section["subsections"]):
        if subsection["subtitle"]:
            st.markdown(f"**<u>{subsection['subtitle']}</u>**", unsafe_allow_html=True)
        if subsection.get("note"):
            st.info(f"**NOTE:** {subsection['note']}")

        for i_idx, (num, item, action) in enumerate(subsection["items"]):
            total_items += 1
            key = f"chk_{section['title']}_{sub_idx}_{i_idx}"
            col1, col2, col3 = st.columns([5, 4, 1], vertical_alignment="center")

            with col1:
                st.markdown(f"**{num} {item}**")
            with col2:
                st.markdown(
                    f"<div style='text-align: right; font-weight: bold;'>{action}</div>",
                    unsafe_allow_html=True,
                )
            with col3:
                if st.checkbox("Done", key=key, label_visibility="collapsed"):
                    completed_items += 1

    if section.get("brief_text"):
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
