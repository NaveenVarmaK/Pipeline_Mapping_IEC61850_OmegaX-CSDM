
### Competency questions for the renwable solar infrastructure
| **CQ2** | For a given equipment, what is the WeatherStation to refer to in order to get the irradiance time series? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?equipment ?weatherStation
WHERE {
  ?equipment a infra:Equipment .
  ?equipment infra:hasWeatherStation ?weatherStation .
}
``` |
| **CQ3** | What are the equipments controlled by a tracker? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?tracker ?equipment
WHERE {
  ?tracker a solar:SolarTracker ;
           solar:controls ?equipment .
}
``` |
| **CQ4** | What are the inverters of an inverter station? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?inverterStation ?inverter
WHERE {
  ?inverter a solar:Inverter ;
            solar:subSystemOfInverterStation ?inverterStation .
}
``` |
| **CQ5** | Which solar arrays consist of which strings? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?array ?string
WHERE {
  ?array a solar:SolarArray ;
         solar:consistsOfStrings ?string .
}
``` |
| **CQ6** | Which strings consist of which panels? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?string ?panel
WHERE {
  ?string a solar:SolarString ;
          solar:consistsOfPanels ?panel .
}
``` |
| **CQ7** | Which panels consist of which cells? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?panel ?cell
WHERE {
  ?panel a solar:SolarModule ;
         solar:consistsOfCells ?cell .
}
``` |
| **CQ8** | What is the number of strings and modules per string in each combiner box? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?combiner ?nbStrings ?nbModules
WHERE {
  ?combiner a solar:CombinerBox ;
            solar:numberOfStrings ?nbStrings ;
            solar:numberOfModulesPerString ?nbModules .
}
``` |
| **CQ9** | What are the feeders belonging to each substation? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?substation ?feeder
WHERE {
  ?feeder a solar:Feeder ;
          solar:subSystemOfSubstation ?substation .
}
``` |
| **CQ10** | What is the rotation axes number and control algorithm of each solar tracker? | ```sparql
PREFIX solar: <http://example.org/solar#>
SELECT ?tracker ?axesNumber ?algorithm
WHERE {
  ?tracker a solar:SolarTracker ;
           solar:TrackerRotationAxexNumber ?axesNumber ;
           solar:TrackerControlAlorithm ?algorithm .
}
``` |

---

✅ **Coverage summary:**
- **CQ1–CQ4** → validation of control & subsystem relationships  
- **CQ5–CQ7** → validation of structural hierarchy (array → string → panel → cell)  
- **CQ8** → validation of numeric data properties  
- **CQ9** → validation of substation composition  
- **CQ10** → validation of tracker configuration  

Would you like me to add **two dynamic CQs** (e.g., about linking time series or irradiance measurements from `WeatherStation` to infrastructure elements) to make it compatible with your **dynamic datasets layer**?

