# Competency SPARQL Queries for Omega-X Knowledge Graph

This document contains a collection of SPARQL queries designed to interrogate an Omega-X based knowledge graph. Each section includes a competency question, the corresponding SPARQL query, and a placeholder for the results.

## 1. What is the DC current for a specific inverter for an hour?

This query retrieves DC current measurements for a specific inverter within a one-hour time window.

```sparql
PREFIX eds: <https://w3id.org/omega-x/ontology/EnergyDataSet/>
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>
PREFIX prop: <https://w3id.org/omega-x/ontology/Property/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?dateTime ?value
WHERE {
  # Define the specific evaluation point (inverter)
  BIND(<https://w3id.org/omega-x/ontology/KG/PARK-DataSets/EvaluationPoint/PARK_ECP002_S3_SHL004Inverter02> AS ?evaluationPoint)

  # Find the EnergyDataSet that includes this evaluation point
  ?energyDataSet eds:includesEvaluationPoint ?evaluationPoint .

  # Find the DataCollections comprised in this EnergyDataSet
  ?energyDataSet ets:comprises ?dataCollection .

  # Filter for the DataCollection that is about DC Current
  ?dataCollection ets:isAboutProperty prop:DCCurrent.

  # Get the DataPoints belonging to this DataCollection
  ?dataPoint ets:belongsTo ?dataCollection .

  # Get the timestamp and the data value link for each DataPoint
  ?dataPoint ets:dataTime ?dateTime ;
             ets:hasDataValue ?dataValue .

  # Get the actual numerical value
  ?dataValue ets:value ?value .

  # Filter for a specific time window
  FILTER (?dateTime >= "2024-06-26T16:00:00"^^xsd:dateTime && ?dateTime < "2024-06-26T17:00:00"^^xsd:dateTime)
}
ORDER BY ?dateTime

```

**Result:**

| Date & Time | DC Current (A) |
|-------------|----------------|
| 2024-06-26T16:00:00 | 349.0 |
| 2024-06-26T16:10:00 | 315.0 |
| 2024-06-26T16:20:00 | 296.0 |
| 2024-06-26T16:30:00 | 275.0 |
| 2024-06-26T16:40:00 | 245.0 |
| 2024-06-26T16:50:00 | 222.0 |

---

## 2. What is the highest enclosure temperature of a specific device for a specific day?

This query retrieves highest enclosure temperature measurements for a specific device over the course of a full day.

```sparql
PREFIX eds: <https://w3id.org/omega-x/ontology/EnergyDataSet/>
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>
PREFIX prop: <https://w3id.org/omega-x/ontology/Property/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?dateTime ?maxTemperature
WHERE {
  # Define the specific evaluation point (inverter)
  BIND(<https://w3id.org/omega-x/ontology/KG/PARK-DataSets/EvaluationPoint/PARK_ECP002_S3_SHL004Inverter02> AS ?evaluationPoint)

  # Find the EnergyDataSet that includes this evaluation point
  ?energyDataSet eds:includesEvaluationPoint ?evaluationPoint .

  # Find the DataCollections comprised in this EnergyDataSet
  ?energyDataSet ets:comprises ?dataCollection .

  # Filter for the DataCollection that is about Enclosure Temperature
  ?dataCollection ets:isAboutProperty prop:EnclosureTemperature .

  # Get the DataPoints belonging to this DataCollection
  ?dataPoint ets:belongsTo ?dataCollection .

  # Get the timestamp and the data value link for each DataPoint
  ?dataPoint ets:dataTime ?dateTime ;
             ets:hasDataValue ?dataValue .

  # Get the actual numerical value
  ?dataValue ets:value ?maxTemperature .

  # Filter for the specific day (2024-06-26)
  FILTER (?dateTime >= "2024-06-29T00:00:00"^^xsd:dateTime && ?dateTime < "2024-06-30T00:00:00"^^xsd:dateTime)

  # Subquery to find the maximum temperature for that day
  {
    SELECT (MAX(?tempValue) AS ?maxTempForDay) WHERE {
      ?energyDataSet2 eds:includesEvaluationPoint <https://w3id.org/omega-x/ontology/KG/PARK-DataSets/EvaluationPoint/PARK_ECP002_S3_SHL004Inverter02> .
      ?energyDataSet2 ets:comprises ?dataCollection2 .
      ?dataCollection2 ets:isAboutProperty prop:EnclosureTemperature .
      ?dataPoint2 ets:belongsTo ?dataCollection2 .
      ?dataPoint2 ets:dataTime ?dateTime2 ;
                  ets:hasDataValue ?dataValue2 .
      ?dataValue2 ets:value ?tempValue .
      FILTER (?dateTime2 >= "2024-06-29T00:00:00"^^xsd:dateTime && ?dateTime2 < "2024-06-30T00:00:00"^^xsd:dateTime)
    }
  }
  
  # Filter to only get the record(s) with the maximum temperature
  FILTER (?maxTemperature = ?maxTempForDay)
}
ORDER BY ?dateTime

```

**Result:**

| Date & Time | Maximum Temperature (°C) |
|-------------|-------------------------|
| 2024-06-29T13:10:00 | 41.0 |


---

## 3. What is the average DC voltage for a specific device?

This query finds the average DC voltage value recorded for a specific device across all available data points.

```sparql
PREFIX eds: <https://w3id.org/omega-x/ontology/EnergyDataSet/>
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>
PREFIX prop: <https://w3id.org/omega-x/ontology/Property/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (AVG(?value) AS ?averageDCVoltage) ?date
WHERE {
  # Define the specific evaluation point (inverter)
  BIND(<https://w3id.org/omega-x/ontology/KG/PARK-DataSets/EvaluationPoint/PARK_ECP002_S3_SHL004Inverter02> AS ?evaluationPoint)
  
  # Define the specific date
  BIND("2024-06-26"^^xsd:date AS ?date)

  # Find the EnergyDataSet that includes this evaluation point
  ?energyDataSet eds:includesEvaluationPoint ?evaluationPoint .

  # Find the DataCollections comprised in this EnergyDataSet
  ?energyDataSet ets:comprises ?dataCollection .

  # Filter for the DataCollection that is about DC Voltage
  ?dataCollection ets:isAboutProperty prop:DCVoltage .

  # Get the DataPoints belonging to this DataCollection
  ?dataPoint ets:belongsTo ?dataCollection .

  # Get the timestamp and the data value link for each DataPoint
  ?dataPoint ets:dataTime ?dateTime ;
             ets:hasDataValue ?dataValue .

  # Get the actual numerical value
  ?dataValue ets:value ?value .

  # Filter for the specific day (2024-06-26)
  FILTER (?dateTime >= "2024-06-26T00:00:00"^^xsd:dateTime && ?dateTime < "2024-06-30T00:00:00"^^xsd:dateTime)
}
GROUP BY ?date

```

**Result:**

| Date | Average DC Voltage (V) |
|------|--------------------|
| 2024-06-26 | 329.8950310559006 |

---

## 4. What are the properties in the KG?

This query discovers all distinct properties that are referenced in the knowledge graph's data collections.

```sparql
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>

SELECT DISTINCT ?property
WHERE {
  ?dataCollection ets:isAboutProperty ?property .
}
```

**Result:**

| Property Name |
|---------------|
| PlaneOfArrayIrradiance |
| BackOfPanelTemperature |
| EnclosureTemperature |
| HeatSinkTemperature |
| DCVoltage |
| DCCurrent |
| DCPower |
| TotalRealPower |

---

## 5. What is the minimum heatsink temperature for a device in a day?


```sparql
PREFIX eds: <https://w3id.org/omega-x/ontology/EnergyDataSet/>
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>
PREFIX prop: <https://w3id.org/omega-x/ontology/Property/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (MIN(?value) AS ?minimumHeatSinkTemperature) ?date
WHERE {
  # Define the specific evaluation point (inverter)
  BIND(<https://w3id.org/omega-x/ontology/KG/PARK-DataSets/EvaluationPoint/PARK_ECP001_S3_SHL001Inverter01> AS ?evaluationPoint)
  
  # Define the specific date
  BIND("2024-06-26"^^xsd:date AS ?date)

  # Find the EnergyDataSet that includes this evaluation point
  ?energyDataSet eds:includesEvaluationPoint ?evaluationPoint .

  # Find the DataCollections comprised in this EnergyDataSet
  ?energyDataSet ets:comprises ?dataCollection .

  # Filter for the DataCollection that is about Heat Sink Temperature
  ?dataCollection ets:isAboutProperty prop:HeatSinkTemperature .

  # Get the DataPoints belonging to this DataCollection
  ?dataPoint ets:belongsTo ?dataCollection .

  # Get the timestamp and the data value link for each DataPoint
  ?dataPoint ets:dataTime ?dateTime ;
             ets:hasDataValue ?dataValue .

  # Get the actual numerical value
  ?dataValue ets:value ?value .

  # Filter for the specific day (2024-06-26)
  FILTER (?dateTime >= "2024-06-26T00:00:00"^^xsd:dateTime && ?dateTime < "2024-06-27T00:00:00"^^xsd:dateTime)
}
GROUP BY ?date

```

**Result:**

| Date | Minimum Heat Sink Temperature (°C) |
|------|----------------------------------|
| 2024-06-26 | 2.84 |
