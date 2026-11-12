"""Campus dataset: 13 locations (12 buildings + main gate), 18 walking paths.

Edge weights are walking minutes. FOOTFALL values are the average daily visitor
counts used by the prototype; replace them with your own recorded figures.
"""

# code -> (full name, kind)
BUILDINGS = {
    "GATE": ("Main Gate and Shuttle Stop", "gate"),
    "ADM":  ("Administration Block", "office"),
    "LIB":  ("Main Library", "library"),
    "ANX":  ("Library Annex", "library"),
    "LT1":  ("Lecture Theatre 1", "lecture"),
    "LT2":  ("Lecture Theatre 2", "lecture"),
    "LT3":  ("Lecture Theatre 3", "lecture"),
    "LT4":  ("Lecture Theatre 4", "lecture"),
    "CAF":  ("Cafeteria", "service"),
    "SPC":  ("Sports Complex", "sports"),
    "HST1": ("Hostel 1", "hostel"),
    "HST2": ("Hostel 2", "hostel"),
    "HST3": ("Hostel 3", "hostel"),
}

# average daily footfall per location (replace with your own counts)
FOOTFALL = {
    "GATE": 1100, "ADM": 640, "LIB": 910, "ANX": 520, "LT1": 820, "LT2": 450,
    "LT3": 380, "LT4": 300, "CAF": 870, "SPC": 270, "HST1": 360, "HST2": 330,
    "HST3": 290,
}

# undirected paths: (a, b, minutes)
EDGES = [
    ("GATE", "ADM", 3), ("GATE", "LIB", 4), ("GATE", "CAF", 7),
    ("ADM", "LIB", 2), ("ADM", "LT1", 5), ("LIB", "ANX", 2),
    ("LIB", "CAF", 3), ("LIB", "LT1", 4), ("LT1", "LT2", 2),
    ("LT2", "LT3", 3), ("LT3", "LT4", 2), ("CAF", "LT3", 4),
    ("CAF", "SPC", 6), ("CAF", "HST1", 5), ("HST1", "HST2", 2),
    ("HST2", "HST3", 2), ("SPC", "HST3", 4), ("ANX", "LT2", 3),
]

# a few rooms per building: room code -> building code
ROOMS = {
    "LIB-G1": "LIB", "LIB-RR": "LIB", "ANX-S1": "ANX", "ANX-S2": "ANX",
    "LT1-101": "LT1", "LT2-201": "LT2", "LT3-301": "LT3", "LT4-401": "LT4",
    "ADM-VC": "ADM", "ADM-REG": "ADM", "CAF-MAIN": "CAF", "SPC-GYM": "SPC",
    "HST1-A1": "HST1", "HST2-B4": "HST2", "HST3-C2": "HST3",
}
