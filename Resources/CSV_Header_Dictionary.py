"""
Dictionary for IEC 61850 header mapping to units and descriptions
This dictionary maps header components to their semantic meanings and units
for use in RML generation with Jinja2 templates.
"""
# Statistical nodes dictionary

MEASUREMENTS = {
    "envtmp": {
        "description": "Air temperature",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "AirTemperature"
    },
    "poainsol": {
        "description": "Plane Of Array Insolation",
        "unit": "W_PER_M2",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "PlaneOfArrayIrradiance"
    },
    "pvstmp": {
        "description": "PV temperature (Back of panel)",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "BackOfPanelTemperature"
    },
    "heatsinktmp": {
        "description": "Heat sink temperature",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "HeatSinkTemperature"
    },
    "amp": {
        "description": "DC Current",
        "unit": "A",
        "enum_kind": "MV_STD",
        "property": "DCCurrent"
    },
    "vol": {
        "description": "DC voltage",
        "unit": "V",
        "enum_kind": "MV_STD",
        "property": "DCVoltage"
    },
    "watt": {
        "description": "DC power",
        "unit": "W",
        "enum_kind": "MV_STD",
        "property": "DCPower"
    },
    "TotW": {
        "description": "Total Real power",
        "unit": "W",
        "enum_kind": "MV_STD",
        "property": "TotalRealPower"
    },

}

# Unit mappings for QUDT vocabulary - extended to include new units
UNIT_TO_QUDT = {
    "DEG_C": "DEG_C",
    "V": "V",
    "A": "A",
    "W": "W",
    "kW": "KiloW",
    "VA": "V.A",
    "VAR": "V.A_R",
    "HZ": "HZ",
    "PERCENT": "PERCENT",
    "kW_HR": "KiloW-HR",
    "OHM": "OHM",
    "W_PER_M2": "W/M2",
    "W_PER_M2_HR": "W.HR/M2",
    "MM": "MM",
    "PA": "PA",
    "M_PER_SEC": "M/SEC",
    "DEG": "DEG",
    "G_PER_CM3": "G/CM3"
}


# Function to get QUDT unit from measurement
def get_qudt_unit(measurement_key):
    """
    Get the QUDT unit for a measurement key
    Returns None if no unit is defined
    """
    measurement_key = measurement_key.lower()

    if measurement_key in MEASUREMENTS and MEASUREMENTS[measurement_key]["unit"]:
        unit = MEASUREMENTS[measurement_key]["unit"]
        return UNIT_TO_QUDT.get(unit, unit)

    return None
