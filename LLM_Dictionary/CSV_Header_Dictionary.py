#A Very Small part of the Data Objects that are extracted from the Document using LLM are shown here.
#In the Actual Project this file is the same as this one "ETL-Pipeline/Resources/CSV_Header_Dictionary.py" which supposed to update the measurements automatically when we run the LLM.
MEASUREMENTS = {
    "beh": {
        "description": "Read-only value, describing the behaviour of a domain logical node. It depends on the current operating mode of the logical node ('DomainLN.Mod'), and the current operating mode of the logical device that contains it ('LLN0.Mod'). Processing of the quality status ('q') of the received data is the prerequisite for correct interpretation of 'DomainLN.Beh'.",
        "unit": "UNITLESS",
        "enum_kind": "ENS-Beh_ENS",
        "property": "Behaviour"
},
   
    "hzhilim": {
        "description": "The frequency high limit of the normal frequency range. The measured frequency must be below this high limit before the DER may be allowed to return to service.",
        "unit": "HZ",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "FrequencyHighLimit"
},
    
    "vhilimg": {
        "description": "The voltage high limit of the normal voltage range. The measured voltage must be below this high limit before the DER may be allowed to return to service.",
        "unit": "V",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "VoltageHighLimit"
},
    
    "amax": {
        "description": "Setting for maximum operational current rating under nominal voltage under nominal power factor",
        "unit": "A",
        "type": "ASG-SP-STD_ASG--SP",
        "property": "MaxOperationalCurrentRating"
},
    
    "avaraAvl": {
        "description": "The amount of reactive power available for absorbing without impacting active power output (the use of this DO is mutually exclusive with the use of VArAvl)",
        "unit": "V-A_Reactive",
        "enum_kind": "MV_STD",
        "property": "AvailableReactivePower"
},
    "avartot": {
        "description": "The total amount of reactive power available for absorbing even if possibly impacting active power output (the use of this DO is mutually exclusive with the use of VArTot)",
        "unit": "V-A_Reactive",
        "enum_kind": "MV_STD",
        "property": "TotalReactivePowerAvailable"
}
}