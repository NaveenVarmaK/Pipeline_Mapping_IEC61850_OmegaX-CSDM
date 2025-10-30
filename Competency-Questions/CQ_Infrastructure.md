# Competency Questions for the Renewable Solar Ontology

## CQ1
Question: For a given equipment, what is the WeatherStation to refer to in order to get the irradiance time series?  
SPARQL:
PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>
PREFIX infra: <http://w3id.org/omega-x/ontology/Infrastructure/>

SELECT ?equipment ?weatherStation
WHERE {
  ?equipment infra:Equipment .
  ?equipment infra:connectedTo ?weatherStation .
}
## CQ2
Question: What are the equipments controlled by a tracker?
SPARQL:
PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?tracker ?equipment
WHERE {
  ?tracker a solar:SolarTracker ;
           solar:controls ?equipment .
}
## CQ3
Question: What are the inverters of an inverter station?
SPARQL:
PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?inverterStation ?inverter
WHERE {
  ?inverter a solar:Inverter ;
            solar:subSystemOfInverterStation ?inverterStation .
}
## CQ4
Question: Which solar arrays consist of which strings?
SPARQL:
PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?array ?string
WHERE {
  ?array a solar:SolarArray ;
         solar:consistsOfStrings ?string .
}
## CQ5
Question: Which strings consist of which panels?
SPARQL:
PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?string ?panel
WHERE {
  ?string a solar:SolarString ;
          solar:consistsOfPanels ?panel .
}
## CQ6
Question: Which panels consist of which modules?
SPARQL:
PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?panel ?module
WHERE {
  ?panel a solar:SolarPanel ;
         solar:consistsOfModules ?module .
}
## CQ7
Question: Which modules consist of which cells?
SPARQL:
PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?module ?cell
WHERE {
  ?module a solar:SolarModule ;
          solar:consistsOfCells ?cell .
}
## CQ8
Question: What are the feeders belonging to each substation?
SPARQL:

PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?substation ?feeder
WHERE {
  ?feeder a solar:Feeder ;
          solar:subSystemOfSubstation ?substation .
}
## CQ9
Question: What is the number of strings and modules per string in each combiner box?
SPARQL:

PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?combiner ?nbStrings ?nbModules
WHERE {
  ?combiner a solar:CombinerBox ;
            solar:numberOfStrings ?nbStrings ;
            solar:numberOfModulesPerString ?nbModules .
}
## CQ10
Question: What is the rotation axes number and control algorithm of each solar tracker?
SPARQL:
PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?tracker ?axesNumber ?algorithm
WHERE {
  ?tracker a solar:SolarTracker ;
           solar:TrackerRotationAxexNumber ?axesNumber ;
           solar:TrackerControlAlorithm ?algorithm .
}
## CQ11
Question: What are the combiner boxes of level 2?
SPARQL:

PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>

SELECT ?combinerboxes
WHERE {
  ?combinerboxes a solar:CombinerBox ;
                 solar:level ?level .
  FILTER(?level = 2)
}
## CQ12
Question: What is the topology of the site?
SPARQL:

PREFIX solar: <http://w3id.org/omega-x/ontology/RenewablesSolar/>
PREFIX infra: <http://w3id.org/omega-x/ontology/Infrastructure/>

SELECT ?site ?substation ?feeder ?inverterStation ?inverter ?powerModule ?array ?string ?panel ?cell ?tracker ?weatherStation
WHERE {
  ?site a solar:Site .
  ?site infra:connectedTo ?substation .

  OPTIONAL {
    ?feeder solar:subSystemOfSubstation ?substation .
    ?inverterStation solar:subSystemOfInverterStation ?inverterStation .
    ?inverter solar:subSystemOfInverterStation ?inverterStation .
    ?powerModule solar:subSystemOfInveter ?inverter .
  }

  OPTIONAL {
    ?array solar:consistsOfStrings ?string .
    ?string solar:consistsOfPanels ?panel .
    ?panel solar:consistsOfCells ?cell .
  }

  OPTIONAL { ?tracker solar:controls ?array . }

  OPTIONAL {
    ?equipment a solar:Equipment ;
               infra:connectedTo ?weatherStation .
  }
}









