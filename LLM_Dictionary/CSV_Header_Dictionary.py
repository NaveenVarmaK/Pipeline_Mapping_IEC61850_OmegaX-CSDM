MEASUREMENTS = {
    "beh": {
        "description": "Read-only value, describing the behaviour of a domain logical node. It depends on the current operating mode of the logical node ('DomainLN.Mod'), and the current operating mode of the logical device that contains it ('LLN0.Mod'). Processing of the quality status ('q') of the received data is the prerequisite for correct interpretation of 'DomainLN.Beh'.",
        "unit": "UNITLESS",
        "enum_kind": "ENS-Beh_ENS",
        "property": "Behaviour"
},
    "gralm": {
        "description": "If true, a new group alarm trigger status has been activated by one of individual alarm trigger states. Group alarm trigger status summarises different alarm trigger states, as assigned via configuration.",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "GroupAlarmTriggerStatus"
},
    "grind": {
        "description": "If true, a new group indication has been activated by one of individual indications. Group indication summarises different indications, as assigned via configuration.",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "GroupIndicationActivated"
},
    "grwrn": {
        "description": "If true, a new group warning trigger status has been activated by one of individual warning trigger states. Group warning trigger status summarises different warning trigger states, as assigned via configuration.",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "GroupWarningTriggerStatus"
},
    "ceaengzreqst": {
        "description": "",
        "unit": "UNITLESS",
        "type": "ENC-CeasetoEnergizeStateKind_ENC",
        "property": "CeaseToEnergizeState"
},
    "ecpref": {
        "description": "Referenced ECP which is the source of the measurement used by the DER mode. It consists of the index or address of the appropriate LN DECP. This address may be within the DER, or within a proxy of ECP, or within a device at the ECP.",
        "unit": "UNITLESS",
        "enum_kind": "ORG_STD",
        "property": "ECPReference"
},
    "fctena": {
        "description": "(controllable) Activation of the DER operational function ctlVal = set to off (FALSE) | set to on (TRUE) Status of the function : stVal = off (FALSE) | on (TRUE)",
        "unit": "UNITLESS",
        "enum_kind": "SPC_STD",
        "property": "DERActivationStatus"
},
    "hzhilim": {
        "description": "The frequency high limit of the normal frequency range. The measured frequency must be below this high limit before the DER may be allowed to return to service.",
        "unit": "HZ",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "FrequencyHighLimit"
},
    "hzlolim": {
        "description": "The frequency low limit of the normal frequency range. The measured frequency must be above this low limit before the DER may be allowed to return to service.",
        "unit": "HZ",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "FrequencyLowLimit"
},
    "rtndlTmms": {
        "description": "Time delay (ms) before returning to service in order to ensure that both the frequency and voltage are within their high and low limits",
        "unit": "MilliM",
        "enum_kind": "ING_STD",
        "property": "TimeDelayBeforeReturningToService"
},
    "rtnrpmtmms": {
        "description": "Return to service duration (ms) that is a time for ramping up that must not be exceeded. Active power shall increase linearly, or in a stepwise linear ramp, with an average rate-of-change not exceeding the DER nameplate active power rating divided by this return to service duration.",
        "unit": "SEC",
        "type": "ING-STD_ING--SP",
        "property": "ReturnToServiceDuration"
},
    "rtnsvcauto": {
        "description": "If true, the DER is authorized to automatically return to service; if false, the DER must wait until an external RtnSvcAuth is received to allow it to return to service.",
        "unit": "BOOLEAN",
        "type": "SPG-SP-STD_SPG--SP",
        "property": "RtnSvcAuto"
},
    "varlimpct": {
        "description": "Limit of reactive power permitted to be supplied or absorbed across the PCC during cease to energize as percent of VArMax (0% - 100%) plus the angle",
        "unit": "PERCENT",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "VArLimitPct"
},
    "vhilimg": {
        "description": "The voltage high limit of the normal voltage range. The measured voltage must be below this high limit before the DER may be allowed to return to service.",
        "unit": "V",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "VoltageHighLimit"
},
    "vloimgnd": {
        "description": "The voltage low limit of the normal voltage range. The measured voltage must be above this low limit before the DER may be allowed to return to service.",
        "unit": "V",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "VoltageLowLimit"
},
    "namplt": {
        "description": "Name plate of the logical node.",
        "unit": "UNITLESS",
        "enum_kind": "LPL-STD-7-420-rev2019A_LPL",
        "property": "NodeNamePlate"
},
    "amax": {
        "description": "Setting for maximum operational current rating under nominal voltage under nominal power factor",
        "unit": "A",
        "type": "ASG-SP-STD_ASG--SP",
        "property": "MaxOperationalCurrentRating"
},
    "amaxrtg": {
        "description": "Maximum current rating under nominal voltage under nominal power factor",
        "unit": "A",
        "type": "ASG-SP-STD_ASG--SP",
        "property": "MaxCurrentRatingUnderNominalVoltageAndPowerFactor"
},
    "authconn": {
        "description": "(controllable) if true, the DER is authorized to connect, otherwise it has to remain (or become) disconnected. Authorization may come from an external source or may be a default setting.",
        "unit": "UNITLESS",
        "enum_kind": "SPC_STD",
        "property": "AuthorizationStatus"
},
    "authdscon": {
        "description": "(controllable) if true, the DER is authorized to disconnect, otherwise shall remain connected (if possible)",
        "unit": "BOOLEAN",
        "type": "SPC-STD_SPC",
        "property": "AuthorizationToDisconnect"
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
},
    "ceaengzctl": {
        "description": "(controllable) Operating with value true initiates the cease to energize state of the DER; operating with value false initiates the return to service (get back to Idle, then reflect the settings of any or all default settings, enabled operational functions, and/or schedules) of the DER.",
        "unit": "UNITLESS",
        "enum_kind": "SPC_STD",
        "property": "CeaEngzCtl"
},
    "cnstwmax1": {
        "description": "The calculation of the maximum power that the generator could output, based on constraining environmental conditions (e.g. solar insolation or wind speed or constraints from heat or vibrations). The delta between this calculation and the actual power being output indicates how much additional power could be output.",
        "unit": "UNITLESS",
        "enum_kind": "MV-STD_MV",
        "property": "MaxPowerOutput"
},
    "ctbvarpct": {
        "description": "Percentage of the reactive power currently generated which results from controllable resource, .i.e whose level can be potentially controlled/set under the request of an entity external to the given DER. This percentage is expressed as current controllable reactive power over maximum rated controllable reactive power (CtbVArMaxRtg)",
        "unit": "PERCENT",
        "enum_kind": "MV-STD_MV",
        "property": "CtbVArPct"
},
    "ctbwpct": {
        "description": "Percentage of the active power currently generated which results from controllable resource, .i.e whose level can be potentially controlled/set under the request of an entity external to the given DER. This percentage is expressed as current controllable active power over maximum rated controllable active power (CtbWMaxRtg)",
        "unit": "PERCENT",
        "enum_kind": "MV-STD_MV",
        "property": "PercentageOfControllableActivePower"
},
    "deropst": {
        "description": "State of operation of the distributed energy resource",
        "unit": "UNITLESS",
        "type": "ENC-DERStateKind_ENC",
        "property": "DERStateKind"
},
    "dertyp": {
        "description": "Type of DER",
        "unit": "UNITLESS",
        "enum_kind": "ENG-DERUnitKind_ENG--SP",
        "property": "DERTyp"
},
    "emgmod": {
        "description": "(controllable) if true the DER shall operate in emergency mode, otherwise shall operate in normal mode. In emergency mode, emergency settings, emergency limits, and other emergency-related setpoints will be in effect.",
        "unit": "UNITLESS",
        "enum_kind": "SPC_STD",
        "property": "EmergencyMode"
},
    "fllebckbeh": {
        "description": "a selector setting indicating to the DER the expected behavior in case of not receiving any more valid setpoint(s), i.e. for example whether to fall back to the default or to keep with the latest received valid set point or other behaviors",
        "unit": "UNITLESS",
        "enum_kind": "ENG-SP-STD_ENG--SP",
        "property": "SelectorSetting"
},
    "gndreactrtg": {
        "description": "Grounding reactance",
        "unit": "OHM",
        "type": "ASG-SP-STD_ASG--SP",
        "property": "GroundingReactance"
},
    "gndrisrtg": {
        "description": "Grounding resistance",
        "unit": "OHM",
        "type": "ASG-SP-STD_ASG--SP",
        "property": "GroundResistance"
},
    "gnenper": {
        "description": "Energy generated during the period since last reset",
        "unit": "KiloW-R",
        "type": "MV-STD_MV",
        "property": "EnergyGeneratedSinceLastReset"
},
    "gnenot": {
        "description": "Total energy generated",
        "unit": "MWh",
        "type": "MV-STD_MV",
        "property": "TotalEnergyGenerated"
},
    "ivaravl": {
        "description": "The amount of reactive power available for injecting without impacting active power output (the use of this DO is mutually exclusive with the use of VArAvl)",
        "unit": "V-A_Reactive",
        "enum_kind": "MV_STD",
        "property": "AvailableReactivePower"
},
    "ivar tot": {
        "description": "The total amount of reactive power available for injecting even if possibly impacting active power output (the use of this DO is mutually exclusive with the use of VArTot)",
        "unit": "V-A_Reactive",
        "enum_kind": "MV_STD",
        "property": "TotalReactivePowerAvailable"
},
    "optmh": {
        "description": "Operation time of the external (electrical, mechanical or communication) equipment since start of the operation.",
        "unit": "SEC",
        "enum_kind": "INC_STD",
        "property": "OperationTimeExternalEquipment"
},
    "optms": {
        "description": "Total time DER unit has operated \u2013 resettable: accumulated time since the last time the time was reset",
        "unit": "SEC",
        "enum_kind": "INC_STD",
        "property": "TimeOperated"
},
    "perstrcnt": {
        "description": "Count of starts in period since reset",
        "unit": "UNITLESS",
        "enum_kind": "INC_STD",
        "property": "StartCountSinceReset"
},
    "phsconntyp": {
        "description": "Phase type of electrical connection of the DER",
        "unit": "UNITLESS",
        "type": "ENG-PhaseKind_ENG--SP",
        "property": "PhaseConnectionType"
},
    "renvarpct": {
        "description": "Percentage of the reactive power currently generated which results from renewable energy resource. What is considered as renewable is a local definition.",
        "unit": "PERCENT",
        "enum_kind": "MV_STD",
        "property": "ReactivePowerPercentageRenewable"
},
    "renwpct": {
        "description": "Percentage of the active power currently generated which results from renewable energy resource. What is considered as renewable is a local definition.",
        "unit": "PERCENT",
        "type": "MV-STD_MV",
        "property": "RenewablePowerPercentage"
},
    "totstrcnt": {
        "description": "Count of total number of starts",
        "unit": "UNITLESS",
        "enum_kind": "INC_STD",
        "property": "TotalStarts"
},
    "vmax": {
        "description": "Setting for maximum voltage operational rating",
        "unit": "V",
        "type": "ASG-SP-STD_ASG--SP",
        "property": "MaxVoltageOperationalRating"
},
    "vmaxrtg": {
        "description": "Maximum voltage rating",
        "unit": "V",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "MaxVoltageRating"
},
    "vmin": {
        "description": "Setting for minimum voltage operational rating",
        "unit": "V",
        "enum_kind": "ASG-SP-STD",
        "property": "MinVoltageOperationalRating"
},
    "vminrtg": {
        "description": "Minimum voltage rating",
        "unit": "V",
        "enum_kind": "ASG-SP-STD",
        "property": "MinVoltageRating"
},
    "clcintvper": {
        "description": "Number of units to consider to calculate the calculation interval duration, in case 'ClcIntvTyp' is not 'EXTERNAL'.",
        "unit": "UNITLESS",
        "enum_kind": "ING-STD_ING--SP",
        "property": "ClcIntvPer"
},
    "wmax": {
        "description": "Setting for maximum active power",
        "unit": "W",
        "type": "ASG-SP-STD_ASG--SP",
        "property": "MaxActivePower"
},
    "clcmod": {
        "description": "Calculation mode.",
        "unit": "UNITLESS",
        "type": "ENG-CalcModeKind-Period_ENG--SP"
},
    "wmaxrtg": {
        "description": "Nameplate maximum active generation power rating at unity power factor",
        "unit": "W",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "MaxActiveGenerationPowerRatingAtUnityPowerFactor"
},
    "wrmpdft": {
        "description": "Default ramp rate for changes in active power: percentage of WMax per second",
        "unit": "PERCENT",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "RampRateActivePower"
},
    "clcsrc": {
        "description": "Object reference to source logical node",
        "unit": "UNITLESS",
        "enum_kind": "ORG_STD",
        "property": "SourceLogicalNodeReference"
},
    "clcmth": {
        "description": "Kind of statistical calculation, specifying how the data attributes that represent analogue or counter values have been calculated. The calculation method shall be the same for all data objects of the logical node instance.",
        "unit": "UNITLESS",
        "type": "ENG-CalcMethodKind-Average_ENG--SP",
        "property": "CalculationMethod"
},
    "clcintvtyp": {
        "description": "Kind of calculation interval.",
        "unit": "UNITLESS",
        "type": "ENG_CalcIntervalKind_Cycle_ENG--SP",
        "property": "CalculationIntervalKind"
},
    "actyp": {
        "description": "Type of AC system.",
        "unit": "UNITLESS",
        "type": "ENG-SP-ACSystemKind_ENG--SP",
        "property": "ACSystemKind"
},
    "invdclosalm": {
        "description": "Alarm trigger status: Inverter detects loss of DC power",
        "unit": "UNITLESS",
        "type": "SPS-STD_SPS",
        "property": "InverterDCPowerLossAlarmStatus"
},
    "invgrielosalm": {
        "description": "Alarm trigger status: Inverter detects loss of grid power",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "InverterGridLossAlarmStatus"
},
    "outwset": {
        "description": "Output power setting.",
        "unit": "W",
        "enum_kind": "ASG-SP-STD",
        "property": "OutputPowerSetting"
},
    "var tg": {
        "description": "The continuous apparent power capability of the power inverter.",
        "unit": "KiloV-A",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "ApparentPower"
},
    "vrtg": {
        "description": "Rated voltage (intrinsic property)",
        "unit": "V",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "RatedVoltage"
},
    "wrtg": {
        "description": "Rated active power of the inverter",
        "unit": "W",
        "enum_kind": "ASG-SP-STD",
        "property": "RatedActivePower"
},
    "wtgt": {
        "description": "Target active power of the inverter",
        "unit": "W",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "ActivePowerTarget"
},
    "encltmp1": {
        "description": "Maximum temperatures among all the Power Electronics devices constituting the inverter arms.",
        "unit": "DEG_C",
        "type": "MV-EXT_MV",
        "property": "EnclosureTemperature"
},
    "wvargvlim": {
        "description": "PQV set of limiting curves",
        "unit": "MVAr",
        "enum_kind": "CSG-STD_CSG--SP",
        "property": "PQVLimitingCurves"
},
    "heatsinktmp1": {
        "description": "Heat sink temperature",
        "unit": "DEG_C",
        "type": "MV-EXT_MV",
        "property": "Temperature"
},
    "wvargvlimset": {
        "description": "Active curve characteristic curve for PQV limit",
        "unit": "MVAr",
        "enum_kind": "CSG-STD_CSG--SP",
        "property": "ActiveCurveCharacteristicCurveForPQVLimit"
},
    "ceaengzctl1": {
        "description": "(controllable) If set to true, Cease to Energize request has been activated, otherwise generating service is allowed,",
        "unit": "UNITLESS",
        "enum_kind": "SPC_STD",
        "property": "CeaseToEnergizeControl"
},
    "ceaengzctlst1": {
        "description": "If true, Cease to energize request for this DER element is active, otherwise generating service is allowed. This DO reflects as well the control performed by this LN to the DPMC CeaEngzCtl controllable DO or to the DEResourceLN DO of the same DER element",
        "unit": "UNITLESS",
        "type": "SPS-STD_SPS",
        "property": "CeaseToEnergizeRequestActive"
},
    "derref1": {
        "description": "Reference to the DER resource LN (a child of DERResourceLN)",
        "unit": "UNITLESS",
        "enum_kind": "ORG_STD",
        "property": "DERReference"
},
    "difvaresp1": {
        "description": "Effective differential reactive power setpoint of the same instance considered by the DPMC LN",
        "unit": "V-A_Reactive",
        "type": "MV-STD_MV",
        "property": "DifferentialReactivePowerSetpoint"
},
    "difvarsppt1": {
        "description": "Reactive differential power setpoint. In case no value is received by the client or DifVArSptAct is set to false, its mxVal shall be associated with quality:invalid.",
        "unit": "UNITLESS",
        "enum_kind": "APC_STD",
        "property": "ReactiveDifferentialPowerSetpoint"
},
    "difvarspтапact1": {
        "description": "If false, the reactive power value stored in DifVArSpt of the same instance is considered as quality:invalid otherwise the sender of the corresponding DifVArSpt of the same instance is active.",
        "unit": "V-A_Reactive",
        "enum_kind": "SPC_STD",
        "property": "DifVArSptAct"
},
    "difwesp1": {
        "description": "Effective differential active power setpoint of the same instance considered by the DPMC LN",
        "unit": "W",
        "type": "MV-STD_MV",
        "property": "DifferentialActivePowerSetpoint"
},
    "difwspt1": {
        "description": "Active differential power setpoint. In case no value is received by the client or DifWSptAct is set to false, its mxVal shall be associated with quality:invalid.",
        "unit": "W",
        "enum_kind": "APC_STD",
        "property": "ActiveDifferentialPowerSetpoint"
},
    "difwsptact1": {
        "description": "If false, the value stored in DifWSpt of the same instance is considered as quality:invalid otherwise the sender of the corresponding DifWSpt of the same instance is active.",
        "unit": "UNITLESS",
        "enum_kind": "SPC-STD_SPC",
        "property": "DifWSptAct1"
},
    "pfspt1": {
        "description": "Power factor set point. In case no value is received by the client or PFSptAct is set to false, its mxVal shall be set to the default value PFSet with quality good. As soon as it receives a valid value (this includes the condition that PFSptAct is set to true), it overrides the default value set in PFSet.",
        "unit": "PERCENT",
        "type": "APC-EXT_APC",
        "property": "PowerFactorSetpoint"
},
    "ecpref1": {
        "description": "Reference to a Electrical Reference Point LN (a child of ElectricalReferencePointLN)",
        "unit": "UNITLESS",
        "enum_kind": "ORG_STD",
        "property": "ElectricalReferencePointLN"
},
    "inref1": {
        "description": "Object reference of data object bound to the input n.",
        "unit": "UNITLESS",
        "enum_kind": "ORG_STD",
        "property": "ObjectReference"
},
    "pfxextspt1": {
        "description": "Complementary PF setpoint parameter of the PFSpt of same instance: (controllable) True = Underexcited; False = Overexcited. In case no value is received by the client or PFExtSptAct is set to false, its mxVal shall be set to the default value PFExtSet with quality good. As soon as it receives a valid value (this includes the condition that PFExtSptAct is set to true), it overrides the default value set in PFExtSet.",
        "unit": "PERCENT",
        "type": "SPC-STD_SPC",
        "property": "PFExtSpt1"
},
    "pfxextsptact1": {
        "description": "If false, the value stored in PFExtSpt of the same instance is considered as quality:invalid otherwise the sender of the corresponding PFExtSpt of the same instance is active.",
        "unit": "UNITLESS",
        "enum_kind": "SPC-STD_SPC",
        "property": "PowerFactor"
},
    "pfsptact1": {
        "description": "If false, the value stored in PFSpt of the same instance is considered as quality:invalid otherwise the sender of the corresponding PFSpt of the same instance is active.",
        "unit": "UNITLESS",
        "enum_kind": "SPC-STD",
        "property": "PFSptAct1"
},
    "reqpf1": {
        "description": "Power Factor requested from either a (DER) resource controlled by this power management function or from a hierarchically lower Power Management function",
        "unit": "UNITLESS",
        "type": "MV-STD_MV",
        "property": "PowerFactor"
},
    "reqpfext1": {
        "description": "Complementary parameter of the ReqPF of same instance : True = Underexcited; False = Overexcited",
        "unit": "UNITLESS",
        "type": "SPS-STD_SPS",
        "property": "ReqPFExt1"
},
    "reqtotvar": {
        "description": "Total reactive power requested to the (DER) resource associated to this power management function. This resource may be hierarchically composed of many DERs.",
        "unit": "KiloV-A_Reactive",
        "type": "MV-STD_MV",
        "property": "TotalReactivePowerRequested"
},
    "reqtotw": {
        "description": "Total active power requested to the (DER) resource associated to this power management function. This resource may be hierarchically composed of many DERs.",
        "unit": "W",
        "type": "MV-STD_MV",
        "property": "ActivePowerRequested"
},
    "reqvar1": {
        "description": "Reactive power requested from either a (DER) resource controlled by this power management function or from a hierarchically lower Power Management function",
        "unit": "V-A_Reactive",
        "enum_kind": "MV_STD",
        "property": "ReactivePowerRequested"
},
    "reqw1": {
        "description": "Active power requested from either a (DER) resource controlled by this power management function or from a hierarchically lower Power Management function",
        "unit": "W",
        "type": "MV-STD_MV",
        "property": "ActivePowerRequested"
},
    "varspet1": {
        "description": "Received reactive power setpoint. In case no value is received by the client or VArSptAct is set to false, its mxVal shall be set to the default value VArSet with quality good. As soon as it receives a valid value (this includes the condition that VArSptAct is set to true), it overrides the default value set in VArSet.",
        "unit": "V-A_Reactive",
        "enum_kind": "APC_STD",
        "property": "ReactivePowerSetpoint"
},
    "varsptact1": {
        "description": "If false, the reactive power value stored in VArSpt of the same instance is considered as quality:invalid otherwise the sender of the corresponding VArSpt of the same instance is active.",
        "unit": "V-A_Reactive",
        "enum_kind": "SPC_STD",
        "property": "ReactivePower"
},
    "varspttopfct1": {
        "description": "Current top priority operational function driving the setting of the expected reactive power of the concerned DER.",
        "unit": "V-A_Reactive",
        "enum_kind": "ORS_STD",
        "property": "PowerFactor"
},
    "wlimspt1": {
        "description": "Limiting setpoint of the DER's active power. In case no value is received by the client or WLimSptAct is set to false, its mxVal shall be set to the default value WLimSet with quality good. As soon as it receives a valid value (this includes the condition that WLimSptAct is set to true), it overrides the default value set in WLimSet.",
        "unit": "W",
        "type": "APC-STD_APC",
        "property": "ActivePowerLimitSetpoint"
},
    "wlimsptact1": {
        "description": "If false, the value stored in WLimSpt of the same instance is considered as quality:invalid otherwise the sender of the corresponding WLimSpt of the same instance is active.",
        "unit": "UNITLESS",
        "enum_kind": "SPC-STD_SPC",
        "property": "ActivePowerQuality"
},
    "wspt1": {
        "description": "Active power setpoint. In case no value is received by the client or WSptAct is set to false, its mxVal shall be set to the default value WSet with quality good. As soon as it receives a valid value (this includes the condition that WSptAct is set to true), it overrides the default value set in WSet.",
        "unit": "W",
        "enum_kind": "APC_STD",
        "property": "ActivePowerSetpoint"
},
    "wsptact1": {
        "description": "If false, the value stored in WSpt of the same instance is considered as quality:invalid otherwise the sender of the corresponding WSpt of the same instance is active.",
        "unit": "UNITLESS",
        "enum_kind": "SPC-STD",
        "property": "ActivePowerQuality"
},
    "wspttopfct1": {
        "description": "Current top priority operational function driving the setting of the expected active power of the concerned DER.",
        "unit": "UNITLESS",
        "enum_kind": "ORS_STD",
        "property": "WSptTopFct1"
},
    "reqwlim1": {
        "description": "Limit of active power requested from a DER controlled by this power management function",
        "unit": "W",
        "type": "MV-EXT_MV",
        "property": "ActivePowerLimit"
},
    "WLimSptTopFct1": {
        "description": "Current top priority operational function driving the setting of the expected limitation of active power of the concerned DER.",
        "unit": "W",
        "type": "ORS-EXT_ORS",
        "property": "ActivePowerLimitation"
},
    "reqtotwlim1": {
        "description": "Total limit of the active power requested to the DER associated to this power management function.",
        "unit": "KiloW",
        "type": "MV-EXT_MV",
        "property": "ActivePowerLimit"
},
    "valimspt1": {
        "description": "Limiting setpoint of the DER\u2019s active power",
        "unit": "W",
        "type": "APC-EXT_APC",
        "property": "ActivePowerSetpoint"
},
    "valims spt act1": {
        "description": "If false, the value stored in WLimSpt of the same instance is invalid. If true, the sender of the corresponding WLimSpt of the same instance is active",
        "unit": "W",
        "enum_kind": "SPC-EXT",
        "property": "ActivePower"
},
    "eehealth": {
        "description": "State of external (electrical, mechanical or communication) equipment to which the logical node is associated.",
        "unit": "UNITLESS",
        "enum_kind": "ENS-Health_ENS",
        "property": "EEHealth"
},
    "typ": {
        "description": "Assembly type",
        "unit": "UNITLESS",
        "type": "ENG-PVAssemblyKind_ENG--SP",
        "property": "AssemblyType"
},
    "arrmodctl": {
        "description": "Mode selected to control the power output of the array",
        "unit": "PERCENT",
        "type": "ENC-PVTrackingControlKind_ENC",
        "property": "ArrayPowerOutputMode"
},
    "ctlmodst": {
        "description": "Array control mode status",
        "unit": "UNITLESS",
        "enum_kind": "INS_STD",
        "property": "ControlModeStatus"
},
    "trk rte": {
        "description": "Power tracker update rate",
        "unit": "SEC",
        "enum_kind": "ING-STD_ING--SP",
        "property": "PowerTrackerUpdateRate"
},
    "pvc tl st": {
        "description": "",
        "unit": "UNITLESS",
        "type": "ENS-PVControlStateKind-EXT_ENS"
},
    "reqidc": {
        "description": "",
        "unit": "OHM",
        "type": "MV-EXT_MV"
},
    "reqpdc": {
        "description": "",
        "unit": "OHM",
        "type": "MV-EXT_MV"
},
    "reqvdc": {
        "description": "DC resistance",
        "unit": "OHM",
        "type": "MV-EXT_MV",
        "property": "DCResistance"
},
    "azideg": {
        "description": "Device azimuth degrees from true north toward east positive",
        "unit": "DEG_C",
        "type": "MV-STD_MV",
        "property": "Azimuth"
},
    "eldeg": {
        "description": "Device elevation degrees from horizontal",
        "unit": "DEG_C",
        "type": "MV-STD_MV",
        "property": "ElevationDegreesFromHorizontal"
},
    "trkcctl": {
        "description": "Tracking command",
        "unit": "UNITLESS",
        "type": "ENC-PVTrackingControlKind_ENC",
        "property": "TrackingCommand"
},
    "trkst": {
        "description": "Tracking status",
        "unit": "UNITLESS",
        "type": "ENS-PVTrackingStatusKind_ENS",
        "property": "TrackingStatus"
},
    "incltrack1": {
        "description": "",
        "unit": "UNITLESS",
        "type": "ORG-EXT_ORG",
        "property": "InclinationTrack"
},
    "azidegt tgt": {
        "description": "Target azimuth degrees from true north toward east positive",
        "unit": "DEG",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "TargetAzimuthDegreesFromTrueNorthTowardEast"
},
    "eldegtgt": {
        "description": "Target elevation from horizontal",
        "unit": "M",
        "enum_kind": "ASG-SP-STD",
        "property": "TargetElevationFromHorizontal"
},
    "trkalm": {
        "description": "Alarm trigger status: Tracking alarm \u2013 True: alarm condition",
        "unit": "BOOLEAN",
        "enum_kind": "SPS_STD",
        "property": "TrackingAlarmStatus"
},
    "trktech": {
        "description": "Tracking technology",
        "unit": "UNITLESS",
        "type": "ENG-PVTrackingTechnologyKind_ENG--SP",
        "property": "TrackingTechnology"
},
    "trktyp": {
        "description": "Tracking type",
        "unit": "UNITLESS",
        "type": "ENG-PVTrackingKind_ENG--SP",
        "property": "TrackingType"
},
    "reqw": {
        "description": "Requested active power resulting from the function. Quality attribute shall be invalid when function is not active.",
        "unit": "W",
        "type": "MV-STD_MV",
        "property": "RequestedActivePower"
},
    "rmprteuse": {
        "description": "Use ramp rates limit. True = limited to ramp rates ; False = Not limited to ramp rates",
        "unit": "BOOLEAN",
        "type": "SPG-SP-STD_SPG--SP",
        "property": "RampRateLimit"
},
    "modngacc": {
        "description": "Average accuracy with which the function will follow the stated values of the dependent curve, in minus units from the stated curve value.",
        "unit": "M-Per-SEC",
        "enum_kind": "ASG-SP-STD_ASG--SP",
        "property": "AverageAccuracy"
},
    "reqwlim": {
        "description": "Requested limiting setpoint of active power generation (or consumption)",
        "unit": "W",
        "type": "MV-STD_MV",
        "property": "ActivePowerSetpoint"
},
    "cntval": {
        "description": "Count value since the last reset of the counter; resetting is a local issue.",
        "unit": "UNITLESS",
        "enum_kind": "BCR_STD",
        "property": "CountValue"
},
    "almcnt": {
        "description": "Alarm counter",
        "unit": "UNITLESS",
        "enum_kind": "BCR-EXT_BCR",
        "property": "AlarmCounter"
},
    "alm": {
        "description": "GAPC ALM Type - Do Alm special EDF R",
        "unit": "UNITLESS",
        "enum_kind": "INS_LIST",
        "property": "Alm"
},
    "wrncnt": {
        "description": "Warning counter",
        "unit": "UNITLESS",
        "enum_kind": "BCR-EXT_BCR",
        "property": "WarningCounter"
},
    "xxxind1": {
        "description": "",
        "unit": "UNITLESS",
        "type": "INS-LIST_INS"
},
    "opctl": {
        "description": "(controllable) If true, the device is running, until stopped with value false.",
        "unit": "UNITLESS",
        "enum_kind": "SPC-STD",
        "property": "DeviceStatus"
},
    "spd": {
        "description": "Rotational speed (rotational speed SIUnit [s-1])",
        "unit": "SEC",
        "enum_kind": "MV_STD",
        "property": "RotationalSpeed"
},
    "firealarm": {
        "description": "if true, a fire is present",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "FireAlarmStatus"
},
    "firefghtact": {
        "description": "(controllable) Operating with value true initiates the activation of the fire fighting system; operating with value false is ignored. The change of its status value is a local issue.",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "FireFightingSystemActivationStatus"
},
    "locsta": {
        "description": "(controllable) If true, control authority is at station level and control from remote is disabled; otherwise control from remote is allowed.",
        "unit": "UNITLESS",
        "enum_kind": "SPC_STD",
        "property": "StationLevelControl"
},
    "opcntrs": {
        "description": "(controllable) Operations count, can be reset to a value different than 0.",
        "unit": "UNITLESS",
        "enum_kind": "INC_STD",
        "property": "OperationsCount"
},
    "loc": {
        "description": "If true, the control behaviour is allowed at this level.",
        "unit": "BOOLEAN",
        "enum_kind": "SPS_STD",
        "property": "ControlAllowedAtLevel"
},
    "illumact1": {
        "description": "(controllable) If true, illumination is activated; otherwise illumination is disactivated.",
        "unit": "UNITLESS",
        "enum_kind": "SPC-STD",
        "property": "IlluminationActivation"
},
    "levpct": {
        "description": "Current level in the tank [%]",
        "unit": "PERCENT",
        "type": "MV-STD_MV",
        "property": "TankLevelPercent"
},
    "vlm": {
        "description": "Current volumetric content in the container.",
        "unit": "M3",
        "enum_kind": "MV_STD",
        "property": "VolumetricContent"
},
    "levmaxalm1": {
        "description": "If true, a predefined alarm level of the maximum level of the tank has been reached",
        "unit": "BOOLEAN",
        "type": "SPS-EXT_SPS",
        "property": "AlarmLevelMaxTankReached"
},
    "levminalm1": {
        "description": "If true, a predefined alarm level of the maximum level of the tank has been reached, and the level is below the threshold, otherwise false",
        "unit": "BOOLEAN",
        "type": "SPS-EXT_SPS",
        "property": "AlarmLevelReached"
},
    "lkgalm": {
        "description": "If true, a leak has been detected.",
        "unit": "UNITLESS",
        "enum_kind": "SPS-EXT_SPS",
        "property": "LeakDetected"
},
    "chliv": {
        "description": "If true, channel is receiving telegrams within a specified time interval 'ChLivTms'. In case of a redundancy protocol this refers to channel A.",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "ChannelReceivingTelegrams"
},
    "health": {
        "description": "Reflects the state of the logical device related hardware and software. It is derived from the worst (most critical) value of the health attribute of all the domain logical nodes contained in the logical device: 'Health' = max('DomainLN[i].Health').",
        "unit": "UNITLESS",
        "enum_kind": "ENS-Health_ENS",
        "property": "Health"
},
    "lockey": {
        "description": "If true, the operation of the whole logical device has been switched (from remote) to local. This changeover is always done locally with a physical key or toggle switch, which may have a set of contacts from which the position can be read.",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "DeviceSwitchState"
},
    "mod": {
        "description": "(controllable) Operating mode of the logical device that may be changed by operator; its value influences behaviour of the domain logical nodes ('DomainLN.Beh') contained in the logical device. Processing of the quality status ('q') of the received data is the prerequisite for correct interpretation of the operating mode.",
        "unit": "UNITLESS",
        "enum_kind": "ENC-Mod_ENC",
        "property": "OperatingMode"
},
    "phyhealth": {
        "description": "Reflects the state of the physical device related hardware and software.",
        "unit": "UNITLESS",
        "enum_kind": "ENS-Health_ENS",
        "property": "PhyHealth"
},
    "phyNam": {
        "description": "Physical device name plate.",
        "unit": "UNITLESS",
        "enum_kind": "DPL_STD",
        "property": "DeviceNamePlate"
},
    "proxy": {
        "description": "If true, the physical device is a proxy (i.e., the logical device embedding this logical node is representing another physical device).",
        "unit": "BOOLEAN",
        "enum_kind": "SPS_STD",
        "property": "IsProxyDevice"
},
    "flwrate": {
        "description": "Volume flow rate",
        "unit": "M3",
        "enum_kind": "MV_STD",
        "property": "FlowRate"
},
    "mattyp": {
        "description": "Type of material",
        "unit": "UNITLESS",
        "enum_kind": "ENG-MaterialKind_ENG--SP",
        "property": "MaterialType"
},
    "matst": {
        "description": "State of material",
        "unit": "UNITLESS",
        "enum_kind": "ENG-MaterialStateKind_ENG--SP"
},
    "amp": {
        "description": "DC current.",
        "unit": "A",
        "type": "MV-STD_MV",
        "property": "DCCurrent"
},
    "risnggnd": {
        "description": "DC resistance between negative pole and earth",
        "unit": "OHM",
        "type": "MV-STD_MV",
        "property": "DCResistanceNegativePoleToEarth"
},
    "rispsgnd": {
        "description": "DC resistance between positive pole and earth",
        "unit": "OHM",
        "type": "MV-STD_MV",
        "property": "DCResistancePositivePoleToEarth"
},
    "vol": {
        "description": "DC voltage.",
        "unit": "V",
        "type": "MV-STD_MV",
        "property": "DCVoltage"
},
    "watt": {
        "description": "DC power.",
        "unit": "W",
        "type": "MV-STD_MV",
        "property": "Power"
},
    "dmdwatt": {
        "description": "Power",
        "unit": "W",
        "type": "MV-EXT_MV"
},
    "rismidgnd": {
        "description": "",
        "unit": "OHM",
        "type": "MV-EXT_MV",
        "property": "DCResistanceNegativePoleToEarth"
},
    "supwatt": {
        "description": "Watt",
        "unit": "W",
        "type": "MV-EXT_MV"
},
    "rnfll": {
        "description": "Rainfall (typically in mm - length SIUnit [m])",
        "unit": "MilliM",
        "enum_kind": "MV_STD",
        "property": "Rainfall"
},
    "snwcvr": {
        "description": "Snow cover (typically in mm - length SIUnit [m])",
        "unit": "MilliM",
        "enum_kind": "MV_STD",
        "property": "SnowCover"
},
    "snwden": {
        "description": "Snowfall density (typically in g/cm3 - density SIUnit [kg/m3])",
        "unit": "HectoPA",
        "enum_kind": "MV_STD",
        "property": "SnowfallDensity"
},
    "snweq": {
        "description": "Water equivalent of snowfall (typically in mm - length SIUnit [m])",
        "unit": "MilliM",
        "enum_kind": "MV_STD",
        "property": "SnowfallEquivalent"
},
    "snwfll": {
        "description": "Snowfall (typically in mm - length SIUnit [m])",
        "unit": "MilliM",
        "enum_kind": "MV_STD",
        "property": "Snowfall"
},
    "wdgustspd": {
        "description": "Maximum wind gust speed.",
        "unit": "M-Per-SEC",
        "enum_kind": "MV-STD_MV",
        "property": "WindGustSpeed"
},
    "envpres": {
        "description": "Barometric pressure of environment.",
        "unit": "Pa",
        "enum_kind": "MV_STD",
        "property": "EnvPres"
},
    "dctinsol1": {
        "description": "Direct normal insolation",
        "unit": "W-M2",
        "enum_kind": "MV-EXT",
        "property": "DctInsol1"
},
    "dffinsol1": {
        "description": "Diffuse insolation",
        "unit": "W-M2",
        "type": "MV-EXT_MV",
        "property": "DiffuseInsolation"
},
    "envhum1": {
        "description": "Ambient humidity",
        "unit": "PERCENT",
        "enum_kind": "MV-EXT",
        "property": "EnvHum1"
},
    "dewpt": {
        "description": "Dew point.",
        "unit": "DEG_C",
        "type": "MV-STD_MV",
        "property": "DewPoint"
},
    "envtmp1": {
        "description": "Ambient temperature",
        "unit": "DEG_C",
        "type": "MV-EXT_MV",
        "property": "AmbientTemperature"
},
    "horinsol1": {
        "description": "Total horizontal insolation",
        "unit": "W-M2",
        "type": "MV-EXT_MV",
        "property": "HorizontalInsolation"
},
    "horwdirdir1": {
        "description": "Total horizontal wind direction",
        "unit": "DEG",
        "type": "MV-EXT_MV"
},
    "horwdspd1": {
        "description": "Average horizontal wind speed",
        "unit": "M-Per-SEC",
        "type": "MV-EXT_MV"
},
    "poainsol1": {
        "description": "Plane Of Array Insolation",
        "unit": "W-M2",
        "type": "MV-EXT_MV",
        "property": "Insolation"
},
    "verwdird1": {
        "description": "Total vertical wind direction",
        "unit": "DEG",
        "type": "MV-EXT_MV",
        "property": "WindDirection"
},
    "verwdspd1": {
        "description": "Average vertical wind speed",
        "unit": "M-Per-SEC",
        "type": "MV-EXT_MV"
},
    "dctinsolh1": {
        "description": "Direct normal insolation per hour (W/m\u00b2/H)",
        "unit": "W-M2",
        "enum_kind": "BCR_EXT",
        "property": "DctInsolH1"
},
    "dffinsolh1": {
        "description": "Diffuse insolation per hour (W/m\u00b2/H)",
        "unit": "W-M2",
        "enum_kind": "BCR_EXT",
        "property": "DiffuseInsolationPerHour"
},
    "horinsolh1": {
        "description": "Total horizontal insolation per hour (W^2/m/H)",
        "unit": "W-M2",
        "enum_kind": "BCR_EXT",
        "property": "HorizontalInsolationPerHour"
},
    "poainsolh1": {
        "description": "Plan Of Array insolation per hour (W/m\u00b2/H)",
        "unit": "W-M2",
        "enum_kind": "BCR_EXT",
        "property": "InsolationPerHour"
},
    "solazideg": {
        "description": "Solar azimuth angle (horizontal angle with respect to north) in degree",
        "unit": "DEG",
        "type": "MV-EXT_MV",
        "property": "AzimuthAngle"
},
    "soleldg": {
        "description": "Solar elevation angle (angle between the horizontal and the line to the Sun) in degree",
        "unit": "DEG",
        "type": "MV-EXT_MV",
        "property": "SolarElevationAngle"
},
    "solzniDeg": {
        "description": "Solar zenith angle (angle between the sun\u2019s rays and the vertical direction) in degree",
        "unit": "DEG_C",
        "type": "MV-EXT_MV",
        "property": "SolarZenithAngle"
},
    "sunshineTm": {
        "description": "Sunshine duration Definition of the World Meteorological Organization (WMO): standardized design of the Campbell\u2013Stokes recorder, called an Interim Reference Sunshine Recorder (IRSR). The sunshine duration is defined as the period during which direct solar irradiance exceeds a threshold value of 120 W/m2.",
        "unit": "W-M2",
        "enum_kind": "BCR_EXT",
        "property": "SunshineDuration"
},
    "dmdvarh": {
        "description": "Reactive energy demand (direction: from busbar)",
        "unit": "KiloV-A_Reactive",
        "enum_kind": "BCR_STD",
        "property": "ReactiveEnergyDemand"
},
    "dmdvarhmeas": {
        "description": "Reactive energy demand (direction: backward based on RvPwrFlwSign convention) reported as MV",
        "unit": "MegaV_A_Reactive",
        "type": "MV-STD-TR90-6-rev2018B_MV",
        "property": "ReactiveEnergyDemand"
},
    "dmdwh": {
        "description": "Real energy demand (direction: from busbar)",
        "unit": "KiloW-R",
        "enum_kind": "BCR_STD",
        "property": "RealEnergyDemandFromBusbar"
},
    "dmdwhmeas": {
        "description": "Real energy demand (direction: backward based on RvPwrFlwSign convention) reported as MV",
        "unit": "MegaW",
        "type": "MV-STD-TR90-6-rev2018B_MV",
        "property": "RealEnergyDemand"
},
    "supvahemas": {
        "description": "Supplied apparent energy reported as MV",
        "unit": "MegaV-A",
        "enum_kind": "MV-STD-TR90-6-rev2018B_MV",
        "property": "SuppliedApparentEnergy"
},
    "supvarh": {
        "description": "Reactive energy supply (default direction: towards busbar)",
        "unit": "KiloV-A_Reactive",
        "enum_kind": "BCR_STD",
        "property": "ReactiveEnergySupply"
},
    "supvarhmeas": {
        "description": "Reactive energy supply (default direction: foreward based on RvPwrFlwSign convention) reported as MV",
        "unit": "MegaV_A_Reactive",
        "type": "MV-STD-TR90-6-rev2018B_MV",
        "property": "ReactiveEnergySupply"
},
    "supwh": {
        "description": "Real energy supply (default direction: towards busbar)",
        "unit": "KiloW-R",
        "enum_kind": "BCR_STD",
        "property": "RealEnergySupply"
},
    "totvaheas": {
        "description": "Net apparent energy reported as MV",
        "unit": "MegaV-A",
        "type": "MV-STD-TR90-6-rev2018B_MV",
        "property": "NetApparentEnergy"
},
    "totvarh": {
        "description": "Net reactive energy since last reset.",
        "unit": "KiloV-A_Reactive",
        "enum_kind": "BCR_STD",
        "property": "NetReactiveEnergy"
},
    "totvarhmeas": {
        "description": "Net reactive energy reported as MV",
        "unit": "MegaV_A_Reactive",
        "type": "MV-STD-TR90-6-rev2018B_MV",
        "property": "NetReactiveEnergy"
},
    "totwh": {
        "description": "Net real energy since last reset.",
        "unit": "W-HR",
        "enum_kind": "BCR_STD",
        "property": "NetRealEnergySinceLastReset"
},
    "totwhmeas": {
        "description": "Net real energy reported as MV",
        "unit": "MegaW",
        "type": "MV-STD-TR90-6-rev2018B_MV",
        "property": "NetRealEnergy"
},
    "dmdvarhtm": {
        "description": "UNITLESS",
        "unit": "V-A_Reactive",
        "type": "BCR-EXT_BCR",
        "property": "VAR"
},
    "dmdwhtm": {
        "description": "",
        "unit": "UNITLESS",
        "type": "BCR-EXT_BCR"
},
    "supvarhtm": {
        "description": "Unspecified BCR",
        "unit": "V-A_Reactive",
        "enum_kind": "BCR_EXT",
        "property": "VARhTm"
},
    "supwhthm": {
        "description": "",
        "unit": "UNITLESS",
        "type": "BCR-EXT_BCR"
},
    "pfsign": {
        "description": "Sign convention for power factor 'PF' (and reactive power 'VAr')",
        "unit": "UNITLESS",
        "type": "ENG-PFSignKind-EXT_ENG--SP",
        "property": "PowerFactorSign"
},
    "q3vahmeas": {
        "description": "Quadrant 3 apparent energy reported as MV",
        "unit": "MegaW",
        "enum_kind": "MV-STD-TR90-6-rev2018B_MV",
        "property": "ApparentEnergyQuadrant3"
},
    "a": {
        "description": "Phase to ground/phase to neutral three phase currents.",
        "unit": "A",
        "type": "WYE-STD_WYE",
        "property": "ThreePhaseCurrents"
},
    "avaphs": {
        "description": "Arithmetic average of the magnitude of current of the 3 phases: average(Ia,Ib,Ic)",
        "unit": "A",
        "type": "MV-STD_MV",
        "property": "CurrentAverageMagnitudePhases"
},
    "avphvphs": {
        "description": "Arithmetic average of the magnitude of phase to reference voltage of the 3 phases: average(PhVa, PhVb, PhVc).",
        "unit": "UNITLESS",
        "type": "MV-STD_MV",
        "property": "PhaseAngleAverage"
},
    "avpppvphs": {
        "description": "Arithmetic average of the magnitude of phase to phase voltage of the 3 phases: average(PPVa, PPVb, PPVc)",
        "unit": "UNITLESS",
        "enum_kind": "MV-STD_MV",
        "property": "PhaseToPhaseVoltageAverage"
},
    "hz": {
        "description": "Frequency [Hz]",
        "unit": "HZ",
        "type": "MV-STD_MV",
        "property": "Frequency"
},
    "pfext": {
        "description": "PFExt set to true = overexcited; PFExt set to false = underexcited",
        "unit": "UNITLESS",
        "type": "SPS-STD-TR90-3-rev2015B_SPS",
        "property": "PFExt"
},
    "phv": {
        "description": "Phase to ground (line) voltages.",
        "unit": "V",
        "enum_kind": "WYE_STD",
        "property": "VoltagePhGroundLine"
},
    "pnv": {
        "description": "Phase to neutral voltages.",
        "unit": "V",
        "enum_kind": "WYE_STD",
        "property": "PhaseToNeutralVoltage"
},
    "ppv": {
        "description": "Phase to phase voltages.",
        "unit": "V",
        "enum_kind": "DEL_STD",
        "property": "PhaseToPhaseVoltage"
},
    "totpf": {
        "description": "Average power factor in a three-phase circuit.",
        "unit": "PERCENT",
        "type": "MV-STD_MV",
        "property": "PowerFactor"
},
    "totva": {
        "description": "The total apparent power in a three-phase circuit [VA]",
        "unit": "V-A",
        "enum_kind": "MV_STD",
        "property": "TotalApparentPowerThreePhaseCircuit"
},
    "totvar": {
        "description": "Total reactive power in a three-phase circuit [VAr]",
        "unit": "V-A_Reactive",
        "enum_kind": "MV_STD",
        "property": "TotalReactivePowerThreePhaseCircuit"
},
    "totw": {
        "description": "Total real power in a three-phase circuit [W]",
        "unit": "W",
        "enum_kind": "MV_STD",
        "property": "TotalRealPowerThreePhaseCircuit"
},
    "dmdva": {
        "description": "",
        "unit": "V-A",
        "type": "MV-EXT_MV",
        "property": "DmdVA"
},
    "dmdvar": {
        "description": "Reactive power",
        "unit": "MVAr",
        "type": "MV-EXT_MV",
        "property": "ReactivePower"
},
    "dmdw": {
        "description": "",
        "unit": "UNITLESS",
        "type": "MV-EXT_MV"
},
    "supva": {
        "description": "",
        "unit": "V",
        "type": "MV-EXT_MV"
},
    "supvar": {
        "description": "Voltage Apparent Reactive",
        "unit": "MVAr",
        "type": "MV-EXT_MV",
        "property": "VoltageApparentReactive"
},
    "supw": {
        "description": "",
        "unit": "W",
        "type": "MV-EXT_MV"
},
    "va": {
        "description": "Phase to ground/phase to neutral apparent powers S.",
        "unit": "V-A",
        "enum_kind": "WYE_STD",
        "property": "ApparentPowerPhaseToGroundNeutral"
},
    "var": {
        "description": "Phase to ground/phase to neutral reactive powers Q.",
        "unit": "KiloV-A_Reactive",
        "enum_kind": "WYE_STD",
        "property": "Q"
},
    "w": {
        "description": "Phase to ground/phase to neutral real powers P.",
        "unit": "W",
        "enum_kind": "WYE_STD",
        "property": "RealPowerPhaseToGroundNeutral"
},
    "ang": {
        "description": "Measured angle",
        "unit": "DEG",
        "type": "MV-STD_MV",
        "property": "Angle"
},
    "hum": {
        "description": "Measured humidity",
        "unit": "PERCENT",
        "type": "MV-STD_MV",
        "property": "Humidity"
},
    "trip": {
        "description": "If true, the humidity exceeded trip level setting 'TripSet'",
        "unit": "UNITLESS",
        "type": "SPS-STD_SPS",
        "property": "Trip"
},
    "tmp": {
        "description": "Measured temperature (typically in degC)",
        "unit": "DEG_C",
        "enum_kind": "MV_STD",
        "property": "Temperature"
},
    "loalm": {
        "description": "",
        "unit": "UNITLESS",
        "enum_kind": "SPS-EXT",
        "property": "LoAlm"
},
    "lotrip": {
        "description": "",
        "unit": "SEC",
        "type": "SPS-EXT_SPS",
        "property": "TripTime"
},
    "almsset": {
        "description": "Temperature alarm trigger status level setting.",
        "unit": "DEG_C",
        "type": "ASG-SP-EXT_ASG--SP",
        "property": "TemperatureAlarmTriggerStatusLevelSetting"
},
    "loalmsset": {
        "description": "",
        "unit": "UNITLESS",
        "type": "ASG-SP-EXT_ASG--SP",
        "property": "LoAlmSet"
},
    "tripSet": {
        "description": "Temperature trip level setting.",
        "unit": "DEG_C",
        "type": "ASG-SP-EXT_ASG--SP",
        "property": "TripSet"
},
    "lotripset": {
        "description": "",
        "unit": "SEC"
},
    "blkcls": {
        "description": "(controllable) If true, 'close' action has been blocked; can be set from another logical node. Operating capability ('XCBR.CBOpCap' and 'XSWI.SwOpCap' for circuit breaker and switch, respectively) does not reflect the blocked closing.",
        "unit": "UNITLESS",
        "enum_kind": "SPC_STD",
        "property": "BlockedClosing"
},
    "blkopn": {
        "description": "(controllable) If true, 'open' action has been blocked; can be set from another logical node. Operating capability ('XCBR.CBOpCap' and 'XSWI.SwOpCap' for circuit breaker and switch, respectively) does not reflect the blocked opening.",
        "unit": "UNITLESS",
        "enum_kind": "SPC_STD",
        "property": "BlockedOpening"
},
    "opcnt": {
        "description": "Count of operations; not resettable from remote, but may be reset from local.",
        "unit": "UNITLESS",
        "enum_kind": "INS_STD",
        "property": "OperationCount"
},
    "pos": {
        "description": "(controllable) Circuit breaker/switch position.",
        "unit": "UNITLESS",
        "type": "DPC-STD_DPC",
        "property": "CircuitBreakerSwitchPosition"
},
    "fust": {
        "description": "If true, fuse has operated (interrupted).",
        "unit": "UNITLESS",
        "enum_kind": "SPS_STD",
        "property": "FuseOperated"
},
    "futyp": {
        "description": "Type of fuse.",
        "unit": "UNITLESS",
        "enum_kind": "ENG-Fuse-STD_ENG--SP",
        "property": "FuseType"
},
    "swtyp": {
        "description": "Type of the switch.",
        "unit": "UNITLESS",
        "enum_kind": "ENS-SwitchFunctionKind_ENS",
        "property": "SwitchType"
},
    "vprs": {
        "description": "if true, indicate that Voltage has reached a level over the minimum threshold possibly defined in VolMin",
        "unit": "UNITLESS",
        "type": "SPS-STD-TR90-3-rev2015B_SPS",
        "property": "VoltageAboveMinimumThreshold"
},
    "pos spt": {
        "description": "",
        "unit": "PERCENT",
        "type": "APC-EXT_APC"
},
    "spdspt": {
        "description": "",
        "unit": "UNITLESS",
        "type": "APC-EXT_APC"
}}