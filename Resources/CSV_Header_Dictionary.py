
"""
Dictionary for IEC 61850 header mapping to units and descriptions
This dictionary maps header components to their semantic meanings and units
for use in RML generation with Jinja2 templates.
"""

# Statistical nodes dictionary
STAT_NODES = {
    "s2": {"aggregation_kind": "Minimum",
           "description": "Statistical LN instance S2 represents the minimum value of the data in period of 10 minutes"},
    "s3": {"aggregation_kind": "Maximum",
           "description": "Statistical LN instance S3 represents the maximum value of the data in period of 10 minutes"},
    "s4": {"aggregation_kind": "Average",
           "description": "Statistical LN instance S4 represents the average value of the data in period of 10 minutes"},
    "s5": {"aggregation_kind": "Sum",
           "description":"Statistical LN instance S5 represents the standard deviation of the data in period of 10 minutes"},

}

# Device types dictionary
DEVICE_TYPES = {
    "dinv": {"description": "Standard Inverter"},
    "inv": {"description": "Inverter"},
    # "mmet": {"description": "Meteorological measurements"},
    # "pvstmp": {"description": "PV temperature (Back of panel)"},
    # "sang": {"description": "Angle supervision"},
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
    # "mmet": {
    #     "class": "MMET",
    #     "type": "sxMMET_STD",
    #     "description": "Meteorological measurements"
    # },
    # "pvstmp": {
    #     "class":"STMP",
    #     "type":"sxSTMP_STD",
    #     "description":"PV temperature (Back of panel)",
    #     # "unit":"DEG_C"
    # },
    # "sang" : {
    #     "class":"SANG",
    #     "type":"SANG_EXT",
    #     "description":"Angle supervision"
    # },
    #




    # DER control logical nodes
    "dpmc": {
        "class": "DPMC",
        "type": "DPMC_STD",
        "description": "DER Power management",
        "property": "DERPowerManagement"
    },
    "dgen": {
        "class": "DGEN",
        "type": "DGEN_STD",
        "description": "DER generator units",
        "property": "DERGeneratorUnits"
    },
    "dpvc": {
        "class": "DPVC",
        "type": "DPVC_STD",
        "description": "DER photovoltaic controller",
        "property": "DERPhotovoltaicController"
    },
    "dinv": {
        "class": "DINV",
        "type": "DINV_STD",
        "description": "DER inverter model – supervision",
        "property": "DERInverterModel"
    },

    # Measurement logical nodes
    "mmxu": {
        "class": "MMXU",
        "type": "sxMMXU_STD",
        "description": "Measurement 3ph",
        "property": "Measurement3ph"
    },
    "mmdc": {
        "class": "MMDC",
        "type": "sxMMDC_STD",
        "description": "Measurement DC",
        "property": "MeasurementDC"
    },
    "mmtr": {
        "class": "MMTR",
        "type": "sxMMTR_STD",
        "description": "Metering 3h",
        "property": "Metering3h"
    },

    # Supervision logical nodes
    "extstmp": {
        "class": "STMP",
        "type": "sxSTMP_STD",
        "description": "Temperature supervision",
        "property": "TemperatureSupervision"
    },
    "shum": {
        "class": "SHUM",
        "type": "sxSHUM_EXT",
        "description": "Humidity supervision",
        "property": "HumiditySupervision"
    },

    # Switch logical nodes
    "acxswi": {
        "class": "XSWI",
        "type": "XSWI_STD",
        "description": "AC Switch",
        "property": "ACSwitch"
    },
    "dcxswi": {
        "class": "XSWI",
        "type": "XSWI_STD",
        "description": "DC Switch",
        "property": "DCSwitch"
    },
    "xcbr": {
        "class": "XCBR",
        "type": "XCBR_STD",
        "description": "AC circuit breaker",
        "property": "ACCircuitBreaker"
    },

    # Temperature measurement logical nodes
    "stmp": {
        "class": "STMP",
        "type": "STMP_STD",
        "description": "Temperature meas. not managed by DINV",
        "property": "TemperatureMeasurement"
    },
    "linereastmp": {
        "class": "STMP",
        "type": "STMP_STD",
        "description": "Line reactor temperature measurement",
        "property": "LineReactorTemperatureMeasurement"
    },

    # Fan monitoring
    "kfan": {
        "class": "KFAN",
        "type": "KFAN_STD",
        "description": "Fan monitoring",
        "property": "FanMonitoring"
    },

    # Alarm and status logical nodes
    "alm_gapc1": {
        "class": "GAPC",
        "type": "ALM_GAPC",
        "description": "Alarm generic LN",
        "property": "AlarmGenericLN"
    },
    "st_gapc2": {
        "class": "GAPC",
        "type": "ST_GAPC",
        "description": "Status generic LN",
        "property": "StatusGenericLN"
    }
}

# Measurements dictionary with units
MEASUREMENTS = {
    # From sxDINV_GLOBAL
    "beh": {
        "description": "Behaviour of the LN (ON, OFF, TEST, BLOCKED)",
        "unit": None,
        "enum_kind": "ENS_Beh",
        "property": "BehaviourofLN"
    },
    "invdclosam": {
        "description": "Inverter detects loss of AC power",
        "unit": None,
        "enum_kind": "SPS_STD",
        "property": "InverterLossOfACPower"
    },
    "invgrlosalm": {
        "description": "Inverter detects loss of grid power",
        "unit": None,
        "enum_kind": "SPS_STD",
        "property": "InverterLossOfGridPower"
    },
    "wtgt": {
        "description": "Target active power (setting)",
        "unit": None,
        "enum_kind": "ASG_STD",
        "property": "TargetActivePower"
    },
    "wvarvlim": {
        "description": "PQV set of limiting curves",
        "unit": None,
        "enum_kind": "CSG_STD",
        "property": "PQVSetOfLimitingCurves"
    },
    "wvarvlimset": {
        "description": "Active curve characteristic curve for PQV limit",
        "unit": None,
        "enum_kind": "CSG_STD",
        "property": "ActiveCurveCharacteristicCurveForPQVLimit"
    },
    "vartg": {
        "description": "The continuous apparent power capability of the power inverter",
        "unit": "VA",
        "enum_kind": "ASG_STD",
        "property": "ContinuousApparentPowerCapability"
    },
    "actyp": {
        "description": "Type of AC system",
        "unit": None,
        "enum_kind": "ENG_ACSystemKind",
        "property": "TypeOfACSystem"
    },
    "outwset": {
        "description": "Output power setting",
        "unit": "W",
        "enum_kind": "ASG_STD",
        "property": "OutputPowerSetting"
    },
    "heatsinktmp": {
        "description": "Heat sink temperature",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "HeatSinkTemperature"
    },
    "encltmp": {
        "description": "Enclosure temperature",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "EnclosureTemperature"
    },
    "volphs": {
        "description": "Phase voltage",
        "unit": "V",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "PhaseVoltage"
    },
    "amp": {
        "description": "DC Current",
        "unit": "A",
        "enum_kind": "MV_STD",
        "property": "DCCurrent"
    },
    "watt": {
        "description": "Active power",
        "unit": "W",
        "enum_kind": "MV_STD",
        "property": "ActivePower"
    },
    "var": {
        "description": "Reactive power",
        "unit": "VAR",
        "enum_kind": "MV_EXT",
        "property": "ReactivePower"
    },
    "hz": {
        "description": "Frequency",
        "unit": "HZ",
        "enum_kind": "MV_EXT",
        "property": "Frequency"
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
        "enum_kind": "MV_EXT",
        "property": "DCPowerDemand"
    },
    "dmdwatt": {
        "description": "DC power supplied",
        "unit": "kW",
        "enum_kind": "MV_EXT",
        "property": "DCPowerSupplied"
    },
    "vol": {
        "description": "DC voltage",
        "unit": "V",
        "enum_kind": "MV_STD",
        "property": "DCVoltage"
    },
    "volpsgnd": {
        "description": "DC voltage between positive pole and earth",
        "unit": "V",
        "enum_kind": "MV_STD",
        "property": "DCVoltagePositivePoleToEarth"
    },
    "volnggnd": {
        "description": "DC voltage between negative pole and earth",
        "unit": "V",
        "enum_kind": "MV_STD",
        "property": "DCVoltageNegativePoleToEarth"
    },
    "rispsgnd": {
        "description": "DC resistance between positive pole and earth",
        "unit": "OHM",
        "enum_kind": "MV_STD",
        "property": "DCResistancePositivePoleToEarth"
    },
    "risnggnd": {
        "description": "DC resistance between negative pole and earth",
        "unit": "OHM",
        "enum_kind": "MV_STD",
        "property": "DCResistanceNegativePoleToEarth"
    },
    "rismidgnd": {
        "description": "Midpoint-ground insulation resistance",
        "unit": "OHM",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "MidpointGroundInsulationResistance"
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
        "multiple": True,
        "property": "DirectNormalInsolation"
    },
    "dctinsolh": {
        "description": "Direct insolation per hour",
        "unit": "W_PER_M2_HR",
        "enum_kind": "BCR_EXT",
        "multiple": True,
        "property": "DirectInsolationPerHour"
    },
    "dewpt": {
        "description": "Dew point",
        "unit": "DEG_C",
        "enum_kind": "MV_STD",
        "property": "DewPoint"
    },
    "dffinsol": {
        "description": "Diffuse insolation",
        "unit": "W_PER_M2",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "DiffuseInsolation"
    },
    "dffinsolh": {
        "description": "Diffuse insolation per hour",
        "unit": "W_PER_M2_HR",
        "enum_kind": "BCR_EXT",
        "multiple": True,
        "property": "DiffuseInsolationPerHour"
    },
    "envhum": {
        "description": "Ambient humidity",
        "unit": "PERCENT",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "AmbientHumidity"
    },
    "envpres": {
        "description": "Barometric pressure",
        "unit": "PA",
        "enum_kind": "MV_STD",
        "property": "BarometricPressure"
    },
    "envtmp": {
        "description": "Ambient temperature",
        "unit": "DEG_C",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "AmbientTemperature"
    },
    "horinsol": {
        "description": "Total horizontal insolation",
        "unit": "W_PER_M2",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "TotalHorizontalInsolation"
    },
    "horinsolh": {
        "description": "Total horizontal insolation per hour",
        "unit": "W_PER_M2_HR",
        "enum_kind": "BCR_EXT",
        "multiple": True,
        "property": "TotalHorizontalInsolationPerHour"
    },
    "horwddir": {
        "description": "Total horizontal wind direction",
        "unit": "DEG",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "TotalHorizontalWindDirection"
    },
    "horwdspd": {
        "description": "Average horizontal wind speed",
        "unit": "M_PER_SEC",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "AverageHorizontalWindSpeed"
    },
    "poainsol": {
        "description": "Plane Of Array Insolation",
        "unit": "W_PER_M2",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "PlaneOfArrayIrradiance"
    },
    "poainsolh": {
        "description": "Plane of Array insolation per hour",
        "unit": "W_PER_M2_HR",
        "enum_kind": "BCR_EXT",
        "multiple": True,
        "property": "PlaneOfArrayIrradiancePerHour"
    },
    "rnfll": {
        "description": "Rainfall",
        "unit": "MM",
        "enum_kind": "MV_STD",
        "property": "Rainfall"
    },
    "rnflltm": {
        "description": "Rainfall on a period of time",
        "unit": "MM",
        "enum_kind": "BCR_EXT",
        "property": "RainfallOnPeriodOfTime"
    },
    "snwcvr": {
        "description": "Snow cover (typically in mm - length SIUnit [m])",
        "unit": "MM",
        "enum_kind": "MV_STD",
        "property": "SnowCover"
    },
    "snwden": {
        "description": "Snowfall density (typically in g/cm3 - density SIUnit [kg/m3])",
        "unit": "G_PER_CM3",
        "enum_kind": "MV_STD",
        "property": "SnowfallDensity"
    },
    "snweq": {
        "description": "Water equivalent of snowfall (typically in mm - length SIUnit [m])",
        "unit": "MM",
        "enum_kind": "MV_STD",
        "property": "WaterEquivalentOfSnowfall"
    },
    "snwfll": {
        "description": "Snowfall (typically in mm - length SIUnit [m])",
        "unit": "MM",
        "enum_kind": "MV_STD",
        "property": "Snowfall"
    },
    "snwflltm": {
        "description": "snowfall (typically in mm - length SIUnit [m] on a period of time)",
        "unit": "MM",
        "enum_kind": "BCR_EXT",
        "property": "SnowfallOnPeriodOfTime"
    },
    "solazideg": {
        "description":"solar azimuth angle (horizontal angle with repsect to the North) in degrees",
        "unit": "DEG",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "SolarAzimuthAngle"
    },
    "soleideg": {
     "description":" Solar elevation angle (angle between the horizontal and the line to the sun) in degrees",
        "unit": "DEG",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "SolarElevationAngle"
    },
    "solznideg": {
        "description":"solar zenith angle (angle between the sun rays and the vertical direction) in degrees",
        "unit": "DEG",
        "enum_kind": "MV_EXT",
        "multiple": True,
        "property": "SolarZenithAngle"
    },
    "sunshinetm": {
        "description":"sunshine duration Definiton of the world meterological organization (WMO): standardized design of the campbell-stokes recorder, called an interim reference sunshine recorder (IRS). The sunshine diration is defined as the period during which direct solar irradiance exceeds a threshold valie of 120 W/m2.",
        "unit": "HOUR",
        "enum_kind": "BCR_EXT",
        "property": "SunshineDuration"
    },
    "wdgustspd":{
        "description":"maximum wind gust speed",
        "enum_kind":"MV_STD",
        "property": "MaximumWindGustSpeed"
    },
    "wdgustdir":{
        "description":"maximum wind gust direction",
        "enum_kind":"MV_EXT",
        "property": "MaximumWindGustDirection"
    },
# From sxMMXU_STD table (three-phase electrical measurements)
    "a": {
        "description": "Phase to gnd/n 3ph currents",
        "unit": "A",
        "enum_kind": "WYE_STD",
        "property": "PhaseToGroundNeutral3phCurrents"
    },
    "avaphs": {
        "description": "Arithmetic average of the magnitude of current of the 3ph to reference voltage of the 3 phases",
        "unit": "A",
        "enum_kind": "MV_STD",
        "property": "ArithmeticAverageMagnitudeCurrent3phToReferenceVoltage"
    },
    "avphvphs": {
        "description": "Arithmetic average of the magnitude of phase to reference voltage of the 3ph",
        "unit": "V",
        "enum_kind": "MV_STD",
        "property": "ArithmeticAverageMagnitudePhaseToReferenceVoltage3ph"
    },
    "avppvphs": {
        "description": "Arithmetic average of the magnitude of phase to phase voltage of the 3ph",
        "unit": "V",
        "enum_kind": "MV_STD",
        "property": "ArithmeticAverageMagnitudePhaseToPhaseVoltage3ph"
    },
    "dmdva": {
        "description": "Apparent power demand",
        "unit": "VA",
        "enum_kind": "MV_EXT",
        "property": "ApparentPowerDemand"
    },
    "dmdvar": {
        "description": "Reactive power demand",
        "unit": "VAR",
        "enum_kind": "MV_EXT",
        "property": "ReactivePowerDemand"
    },
    "dmdw": {
        "description": "Active power demand",
        "unit": "W",
        "enum_kind": "MV_EXT",
        "property": "ActivePowerDemand"
    },
    "pfext": {
        "description": "PFExt set to true = overexcited; PFExt set to false = underexcited",
        "unit": None,
        "enum_kind": "SPS_STD",
        "property": "PowerFactorExternal"
    },
    "pfsign": {
        "description": "Sign convention for power factor 'PF' (and reactive power 'VAr')",
        "unit": None,
        "enum_kind": "ENG_PFSign",
        "property": "PowerFactorSignConvention"
    },
    "pnv": {
        "description": "Phase to neutral voltages",
        "unit": "V",
        "enum_kind": "WYE_STD",
        "property": "PhaseToNeutralVoltages"
    },
    "ppv": {
        "description": "Phase to phase voltages",
        "unit": "V",
        "enum_kind": "DEL_STD",
        "property": "PhaseToPhaseVoltages"
    },
    "supva": {
        "description": "Apparent power supply",
        "unit": "VA",
        "enum_kind": "MV_EXT",
        "property": "ApparentPowerSupply"
    },
    "supvar": {
        "description": "Reactive power supply",
        "unit": "VAR",
        "enum_kind": "MV_EXT",
        "property": "ReactivePowerSupply"
    },
    "supw": {
        "description": "Active power supply",
        "unit": "W",
        "enum_kind": "MV_EXT",
        "property": "ActivePowerSupply"
    },
    "totpf": {
        "description": "Average PF of 3ph",
        "unit": "PER_UNIT",
        "enum_kind": "MV_STD",
        "property": "TotalPowerFactor"
    },
    "totva": {
        "description": "Total apparent power",
        "unit": "VA",
        "enum_kind": "MV_STD",
        "property": "TotalApparentPower"
    },
    "totvar": {
        "description": "Total reactive power",
        "unit": "VAR",
        "enum_kind": "MV_STD",
        "property": "TotalReactivePower"
    },
    "totw": {
        "description": "Total active power",
        "unit": "W",
        "enum_kind": "MV_STD",
        "property": "TotalActivePower"
    },
    "va": {
        "description": "Phase to ground/phase to neutral apparent powers S",
        "unit": "VA",
        "enum_kind": "WYE_STD",
        "property": "PhaseToGroundPhaseToNeutralApparentPowers"
    },
    "var": {
        "description": "Phase to ground/phase to neutral reactive powers Q",
        "unit": "VAR",
        "enum_kind": "WYE_STD",
        "property": "PhaseToGroundPhaseToNeutralReactivePowers"
    },
    "w": {
        "description": "Phase to ground/phase to neutral real powers P",
        "unit": "W",
        "enum_kind": "WYE_STD",
        "property": "PhaseToGroundPhaseToNeutralRealPowers"
    },
    "tmp": {
        "description": "Temperature",
        "unit": "DEG_C",
        "property": "Temperature",
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
    "W_PER_M2": "W_PER_M2",
    "W_PER_M2_HR": "W_PER_M2_HR",
    "MM": "MM",
    "PA": "PA",
    "M_PER_SEC": "M_PER_SEC",
    "DEG": "DEG",
    "G_PER_CM3": "G_PER_CM3"
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