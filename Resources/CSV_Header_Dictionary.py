"""
Dictionary for IEC 61850 header mapping to units and descriptions
This dictionary maps header components to their semantic meanings and units
for use in RML generation with Jinja2 templates.
"""

# Statistical nodes dictionary
STAT_NODES = {
    "s1": {"description": "Statistical Logical Node - maximum value over 10 minutes"},
    "s2": {"description": "Statistical Logical Node - minimum value over 10 minutes"},
    "s3": {"description": "Statistical Logical Node - average value over 10 minutes"},
    "s4": {"description": "Statistical Logical Node - accumulated value over 10 minutes"}
}

# Device types dictionary
DEVICE_TYPES = {
    "dinv": {"description": "Standard Inverter"},
    "inv": {"description": "Inverter"}
}

# Logical nodes dictionary
LOGICAL_NODES = {
    # Device level logical nodes
    "lln0": {
        "class": "LLN0",
        "type": "LLN0_STD",
        "description": "Logical device (This logical device contains common information for logical device Inverter)"
    },
    "lphd": {
        "class": "LPHD",
        "type": "LPHD",
        "description": "Physical device"
    },

    # DER control logical nodes
    "dpmc": {
        "class": "DPMC",
        "type": "DPMC_STD",
        "description": "DER Power management"
    },
    "dgen": {
        "class": "DGEN",
        "type": "DGEN_STD",
        "description": "DER generator units"
    },
    "dpvc": {
        "class": "DPVC",
        "type": "DPVC_STD",
        "description": "DER photovoltaic controller"
    },
    "dinv": {
        "class": "DINV",
        "type": "DINV_STD",
        "description": "DER inverter model – supervision"
    },

    # Measurement logical nodes
    "mmxu": {
        "class": "MMXU",
        "type": "sxMMXU_STD",
        "description": "Measurement 3ph"
    },
    "mmdc": {
        "class": "MMDC",
        "type": "sxMMDC_STD",
        "description": "Measurement DC"
    },
    "mmtr": {
        "class": "MMTR",
        "type": "sxMMTR_STD",
        "description": "Metering 3h"
    },

    # Supervision logical nodes
    "extstmp": {
        "class": "STMP",
        "type": "sxSTMP_STD",
        "description": "Temperature supervision"
    },
    "shum": {
        "class": "SHUM",
        "type": "sxSHUM_EXT",
        "description": "Humidity supervision"
    },

    # Switch logical nodes
    "acxswi": {
        "class": "XSWI",
        "type": "XSWI_STD",
        "description": "AC Switch"
    },
    "dcxswi": {
        "class": "XSWI",
        "type": "XSWI_STD",
        "description": "DC Switch"
    },
    "xcbr": {
        "class": "XCBR",
        "type": "XCBR_STD",
        "description": "AC circuit breaker"
    },

    # Temperature measurement logical nodes
    "stmp": {
        "class": "STMP",
        "type": "STMP_STD",
        "description": "Temperature meas. not managed by DINV"
    },
    "linereastmp": {
        "class": "STMP",
        "type": "STMP_STD",
        "description": "Line reactor temperature measurement"
    },

    # Fan monitoring
    "kfan": {
        "class": "KFAN",
        "type": "KFAN_STD",
        "description": "Fan monitoring"
    },

    # Alarm and status logical nodes
    "alm_gapc1": {
        "class": "GAPC",
        "type": "ALM_GAPC",
        "description": "Alarm generic LN"
    },
    "st_gapc2": {
        "class": "GAPC",
        "type": "ST_GAPC",
        "description": "Status generic LN"
    }
}

# Measurements dictionary with units
MEASUREMENTS = {
    # From sxDINV_GLOBAL
    "beh": {
        "description": "Behaviour of the LN (ON, OFF, TEST, BLOCKED)",
        "unit": None,
        "enum_kind": "ENS_Beh"
    },
    "invdclosam": {
        "description": "Inverter detects loss of AC power",
        "unit": None,
        "enum_kind": "SPS_STD"
    },
    "invgrlosalm": {
        "description": "Inverter detects loss of grid power",
        "unit": None,
        "enum_kind": "SPS_STD"
    },
    "wtgt": {
        "description": "Target active power (setting)",
        "unit": None,
        "enum_kind": "ASG_STD"
    },
    "wvarvlim": {
        "description": "PQV set of limiting curves",
        "unit": None,
        "enum_kind": "CSG_STD"
    },
    "wvarvlimset": {
        "description": "Active curve characteristic curve for PQV limit",
        "unit": None,
        "enum_kind": "CSG_STD"
    },
    "vartg": {
        "description": "The continuous apparent power capability of the power inverter",
        "unit": "VA",
        "enum_kind": "ASG_STD"
    },
    "actyp": {
        "description": "Type of AC system",
        "unit": None,
        "enum_kind": "ENG_ACSystemKind"
    },
    "outwset": {
        "description": "Output power setting",
        "unit": "W",
        "enum_kind": "ASG_STD"
    },
    "heatsinktmp": {
        "description": "Heat sink temperature",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "encltmp": {
        "description": "Enclosure temperature",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "volphs": {
        "description": "Phase voltage",
        "unit": "V",
        "enum_kind": "MV_EXT"
    },
    "amp": {
        "description": "DC Current",
        "unit": "A",
        "enum_kind": "MV_STD"
    },
    "watt": {
        "description": "Active power",
        "unit": "W",
        "enum_kind": "MV_STD"
    },
    "var": {
        "description": "Reactive power",
        "unit": "VAR",
        "enum_kind": "MV_EXT"
    },
    "hz": {
        "description": "Frequency",
        "unit": "HZ",
        "enum_kind": "MV_EXT"
    },
    # "pf": {
    #     "description": "Power factor",
    #     "unit": "PER_UNIT",
    #     "enum_kind": "MV_EXT"
    # },
    # "kwh": {
    #     "description": "Energy counter",
    #     "unit": "kW_HR",
    #     "enum_kind": "MV_EXT"
    # },
    # "efftot": {
    #     "description": "Total efficiency",
    #     "unit": "PERCENT",
    #     "enum_kind": "MV_EXT"
    # },

    # From sxMMDC_STD table (DC measurements)
    # "amp_dc": {
    #     "description": "DC current",
    #     "unit": "A",
    #     "enum_kind": "MV_STD"
    # },
    # "watt_dc": {
    #     "description": "DC power",
    #     "unit": "kW",
    #     "enum_kind": "MV_STD"
    # },
    "supwatt": {
        "description": "DC power demand",
        "unit": "kW",
        "enum_kind": "MV_EXT"
    },
    "dmdwatt": {
        "description": "DC power supplied",
        "unit": "kW",
        "enum_kind": "MV_EXT"
    },
    "vol": {
        "description": "DC voltage",
        "unit": "V",
        "enum_kind": "MV_STD"
    },
    "volpsgnd": {
        "description": "DC voltage between positive pole and earth",
        "unit": "V",
        "enum_kind": "MV_STD"
    },
    "volnggnd": {
        "description": "DC voltage between negative pole and earth",
        "unit": "V",
        "enum_kind": "MV_STD"
    },
    "rispsgnd": {
        "description": "DC resistance between positive pole and earth",
        "unit": "OHM",
        "enum_kind": "MV_STD"
    },
    "risnggnd": {
        "description": "DC resistance between negative pole and earth",
        "unit": "OHM",
        "enum_kind": "MV_STD"
    },
    "rismidgnd": {
        "description": "Midpoint-ground insulation resistance",
        "unit": "OHM",
        "enum_kind": "MV_EXT",
        "multiple": True
    },

    # From sxMMET_STD table (meteorological measurements)
    # "presccond": {
    #     "description": "Behaviour",
    #     "unit": None,
    #     "enum_kind": "ENS_Beh"
    # },
    "dctinsol": {
        "description": "Direct normal insolation",
        "unit": "W_PER_M2",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "dctinsolh": {
        "description": "Direct insolation per hour",
        "unit": "W_PER_M2_HR",
        "enum_kind": "BCR_EXT",
        "multiple": True
    },
    "dewpt": {
        "description": "Dew point",
        "unit": "DEG_C",
        "enum_kind": "MV_STD"
    },
    "dffinsol": {
        "description": "Diffuse insolation",
        "unit": "W_PER_M2",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "dffinsolh": {
        "description": "Diffuse insolation per hour",
        "unit": "W_PER_M2_HR",
        "enum_kind": "BCR_EXT",
        "multiple": True
    },
    "envhum": {
        "description": "Ambient humidity",
        "unit": "PERCENT",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "envpres": {
        "description": "Barometric pressure",
        "unit": "PA",
        "enum_kind": "MV_STD"
    },
    "envtmp": {
        "description": "Ambient temperature",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "horinsol": {
        "description": "Total horizontal insolation",
        "unit": "W_PER_M2",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "horinsolh": {
        "description": "Total horizontal insolation per hour",
        "unit": "W_PER_M2_HR",
        "enum_kind": "BCR_EXT",
        "multiple": True
    },
    "horwddir": {
        "description": "Total horizontal wind direction",
        "unit": "DEG",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "horwdspd": {
        "description": "Average horizontal wind speed",
        "unit": "M_PER_SEC",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "poainsol": {
        "description": "Plane Of Array Insolation",
        "unit": "W_PER_M2",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "poainsolh": {
        "description": "Plane of Array insolation per hour",
        "unit": "W_PER_M2_HR",
        "enum_kind": "BCR_EXT",
        "multiple": True
    },
    "rnfll": {
        "description": "Rainfall",
        "unit": "MM",
        "enum_kind": "MV_STD"
    },
    "rnflltm": {
        "description": "Rainfall on a period of time",
        "unit": "MM",
        "enum_kind": "BCR_EXT"
    },
    "snwcvr": {
        "description": "Snow cover (typically in mm - length SIUnit [m])",
        "unit": "MM",
        "enum_kind": "MV_STD"
    },
    "snwden": {
        "description": "Snowfall density (typically in g/cm3 - density SIUnit [kg/m3])",
        "unit": "G_PER_CM3",
        "enum_kind": "MV_STD"
    },
    "snweq": {
        "description": "Water equivalent of snowfall (typically in mm - length SIUnit [m])",
        "unit": "MM",
        "enum_kind": "MV_STD"
    },
    "snwfll": {
        "description": "Snowfall (typically in mm - length SIUnit [m])",
        "unit": "MM",
        "enum_kind": "MV_STD"
    },
    "snwflltm": {
        "description": "snowfall (typically in mm - length SIUnit [m] on a period of time)",
        "unit": "MM",
        "enum_kind": "BCR_EXT"
    },
    "solazideg": {
        "description":"solar azimuth angle (horizontal angle with repsect to the North) in degrees",
        "unit": "DEG",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "soleideg": {
     "description":" Solar elevation angle (angle between the horizontal and the line to the sun) in degrees",
        "unit": "DEG",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "solznideg": {
        "description":"solar zenith angle (angle between the sun rays and the vertical direction) in degrees",
        "unit": "DEG",
        "enum_kind": "MV_EXT",
        "multiple": True
    },
    "sunshinetm": {
        "description":"sunshine duration Definiton of the world meterological organization (WMO): standardized design of the campbell-stokes recorder, called an interim reference sunshine recorder (IRS). The sunshine diration is defined as the period during which direct solar irradiance exceeds a threshold valie of 120 W/m2.",
        "unit": "HOUR",
        "enum_kind": "BCR_EXT"
    },
    "wdgustspd":{
        "description":"maximum wind gust speed",
        "enum_kind":"MV_STD",
    },
    "wdgustdir":{
        "description":"maximum wind gust direction",
        "enum_kind":"MV_EXT",
    },
# From sxMMXU_STD table (three-phase electrical measurements)
    "a": {
        "description": "Phase to gnd/n 3ph currents",
        "unit": "A",
        "enum_kind": "WYE_STD"
    },
    "avaphs": {
        "description": "Arithmetic average of the magnitude of current of the 3ph to reference voltage of the 3 phases",
        "unit": "A",
        "enum_kind": "MV_STD"
    },
    "avphvphs": {
        "description": "Arithmetic average of the magnitude of phase to reference voltage of the 3ph",
        "unit": "V",
        "enum_kind": "MV_STD"
    },
    "avppvphs": {
        "description": "Arithmetic average of the magnitude of phase to phase voltage of the 3ph",
        "unit": "V",
        "enum_kind": "MV_STD"
    },
    "dmdva": {
        "description": "Apparent power demand",
        "unit": "VA",
        "enum_kind": "MV_EXT"
    },
    "dmdvar": {
        "description": "Reactive power demand",
        "unit": "VAR",
        "enum_kind": "MV_EXT"
    },
    "dmdw": {
        "description": "Active power demand",
        "unit": "W",
        "enum_kind": "MV_EXT"
    },
    "pfext": {
        "description": "PFExt set to true = overexcited; PFExt set to false = underexcited",
        "unit": None,
        "enum_kind": "SPS_STD"
    },
    "pfsign": {
        "description": "Sign convention for power factor 'PF' (and reactive power 'VAr')",
        "unit": None,
        "enum_kind": "ENG_PFSign"
    },
    "pnv": {
        "description": "Phase to neutral voltages",
        "unit": "V",
        "enum_kind": "WYE_STD"
    },
    "ppv": {
        "description": "Phase to phase voltages",
        "unit": "V",
        "enum_kind": "DEL_STD"
    },
    "supva": {
        "description": "Apparent power supply",
        "unit": "VA",
        "enum_kind": "MV_EXT"
    },
    "supvar": {
        "description": "Reactive power supply",
        "unit": "VAR",
        "enum_kind": "MV_EXT"
    },
    "supw": {
        "description": "Active power supply",
        "unit": "W",
        "enum_kind": "MV_EXT"
    },
    "totpf": {
        "description": "Average PF of 3ph",
        "unit": "PER_UNIT",
        "enum_kind": "MV_STD"
    },
    "totva": {
        "description": "Total apparent power",
        "unit": "VA",
        "enum_kind": "MV_STD"
    },
    "totvar": {
        "description": "Total reactive power",
        "unit": "VAR",
        "enum_kind": "MV_STD"
    },
    "totw": {
        "description": "Total active power",
        "unit": "W",
        "enum_kind": "MV_STD"
    },
    "va": {
        "description": "Phase to ground/phase to neutral apparent powers S",
        "unit": "VA",
        "enum_kind": "WYE_STD"
    },
    "var": {
        "description": "Phase to ground/phase to neutral reactive powers Q",
        "unit": "VAR",
        "enum_kind": "WYE_STD"
    },
    "w": {
        "description": "Phase to ground/phase to neutral real powers P",
        "unit": "W",
        "enum_kind": "WYE_STD"
    },

}

# Value types dictionary
VALUE_TYPES = {
    "mag": {"description": "Magnitude value"},
    "q": {"description": "Quality value"},
    "t": {"description": "Timestamp"}
}

# Data types dictionary
DATA_TYPES = {
    "f": {"description": "Float value", "xsd_type": "float"},
    "i": {"description": "Integer value", "xsd_type": "integer"},
    "b": {"description": "Boolean value", "xsd_type": "boolean"},
    "s": {"description": "String value", "xsd_type": "string"}
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
    "PER_UNIT": "UNITLESS",
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