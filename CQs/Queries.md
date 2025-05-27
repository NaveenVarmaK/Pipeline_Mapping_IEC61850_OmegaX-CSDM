### Table: Competency Questions (CQs) grouped by Infrastructure and Dynamic Data

| ID   | Competency Question (CQ) | SPARQL |
|------|---------------------------|---------|
| **Group 1: Infrastructure Data** |  |  |
| CQ1  | What are the main components of a given PV plant? | `PARK_ECP001_S3_SHL001_Inverter01` is a component of *PARK* PV plant. |
| CQ2  | What are the connected equipment to a particular substation? | For `PARK_ECP001_S3`, the connected equipment are `PARK_ECP001_S3_METEO01` and `PARK_ECP001_S3_METEO02`. |
| CQ3  | What is the number of combiner boxes level 1 connected to a particular inverter? | For `PARK_ECP001_S3_SHL001_Inverter01`, four combiner boxes level 1 are connected to the inverter. |
| CQ4  | What are the subsystems of a particular inverter station? | For `PARK_ECP001_S3_SHL001`, `PARK_ECP001_S3_SHL001_Inverter01`, `PARK_ECP001_S3_SHL001_Inverter02`, and `PARK_ECP001_S3_SHL001_Inverter03` are subsystems of the inverter station. |
| CQ5  | What are the combiner box level 2 in the topology? | `PARK_ECP001_S3_SHL001_CA001_CB003` is a combiner box level 2 in the *CAT1* topology. |
| **Group 2: Dynamic Data** |  |  |
| CQ6  | What is the DC current attached to a specific inverter for a week? | For `week1`, for `PARK_ECP001_S3_SHL001_Inverter01`, the values are taken from the column `mmdc1.amp.mag.f` where the timestamp is in the first week of data extraction. |
| CQ7  | What are the ambient temperature readings from a particular weather station for a specific week? | For `week2`, for `PARK_ECP001_S3_METEO02`, the values are taken from the column `mmet1.envtmp.mag.f` where the timestamp is in the second week of data extraction. |
| CQ8  | What is the maximum irradiance for a specific site? | The maximum value is taken from the column `mmet1.poainsol1.mag.f` for all weather stations in the specific site. |
| CQ9  | What is the heat sink temperature of a specific inverter for a specific day? | For 05 May 2024, for `PARK_ECP001_S3_SHL001_Inverter01`, the value is taken from the column `dinv1.heatsinktmp.mag.f`. |
| CQ10 | What is the minimum DC Voltage attached to a specific inverter? | The minimum value is taken from the column `mmdc1.vol.mag.f` for `PARK_ECP001_S3_SHL001_Inverter01`. |
