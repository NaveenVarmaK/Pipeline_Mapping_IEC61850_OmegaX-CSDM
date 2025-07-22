# SPARQL Queries for Omega-X Knowledge Graph

This document contains a collection of SPARQL queries designed to interrogate an Omega-X based knowledge graph. Each section includes a natural language question, the corresponding SPARQL query, and a placeholder for the results screenshot.

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
  BIND(<https://w3id.org/omega-x/ontology/KG/PARKDatasets/EvaluationPoint/PARK_ECP002_S3_SHL002_CA001> AS ?evaluationPoint)

  # Find the EnergyDataSet that includes this evaluation point
  ?energyDataSet eds:includesEvaluationPoint ?evaluationPoint .

  # Find the DataCollections comprised in this EnergyDataSet
  ?energyDataSet ets:comprises ?dataCollection .

  # Filter for the DataCollection that is about DC Current
  ?dataCollection ets:isAboutProperty prop:DCCurrent .

  # Get the DataPoints belonging to this DataCollection
  ?dataPoint ets:belongsTo ?dataCollection .

  # Get the timestamp and the data value link for each DataPoint
  ?dataPoint ets:dataTime ?dateTime ;
             ets:hasDataValue ?dataValue .

  # Get the actual numerical value
  ?dataValue ets:value ?value .

  # Filter for a specific one-hour time window
  FILTER (?dateTime >= "2024-06-26T15:00:00"^^xsd:dateTime && ?dateTime < "2024-06-26T16:00:00"^^xsd:dateTime)
}
ORDER BY ?dateTime
```

**Result:**

![Screenshot 2025-06-19 144533](https://github.com/user-attachments/assets/8d93f7aa-d88e-48b4-b6cf-8e7b7bd84fa9)


---

## 2. What is the heat sink temperature of a specific device for a specific day?

This query retrieves heat sink temperature measurements for a specific device over the course of a full day.

```sparql
PREFIX eds: <https://w3id.org/omega-x/ontology/EnergyDataSet/>
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>
PREFIX prop: <https://w3id.org/omega-x/ontology/Property/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?dateTime ?value
WHERE {
  # Define the specific evaluation point (device)
  BIND(<https://w3id.org/omega-x/ontology/KG/PARKDatasets/EvaluationPoint/PARK_ECP001_S3_SHL001Inverter01> AS ?evaluationPoint)

  # Find the EnergyDataSet that includes this evaluation point
  ?energyDataSet eds:includesEvaluationPoint ?evaluationPoint .

  # Find the DataCollections comprised in this EnergyDataSet
  ?energyDataSet ets:comprises ?dataCollection .

  # Filter for the DataCollection that is about Heat Sink Temperature
  # NOTE: 'prop:HeatSinkTemperature' is an assumed property URI
  ?dataCollection ets:isAboutProperty prop:HeatSinkTemperature .

  # Get the DataPoints belonging to this DataCollection
  ?dataPoint ets:belongsTo ?dataCollection .

  # Get the timestamp and the data value link for each DataPoint
  ?dataPoint ets:dataTime ?dateTime ;
             ets:hasDataValue ?dataValue .

  # Get the actual numerical value
  ?dataValue ets:value ?value .

  # Filter for a specific day
  FILTER (STRSTARTS(STR(?dateTime), "2024-06-26"))
}
ORDER BY ?dateTime
```

**Result:**

![Screenshot 2025-06-19 144824](https://github.com/user-attachments/assets/883ffc49-6ee4-4fcf-a54a-c4309c554adf)


---

## 3. What is the minimum DC current attached to a specific device?

This query finds the minimum DC current value recorded for a specific device across all available data points.

```sparql
PREFIX eds: <https://w3id.org/omega-x/ontology/EnergyDataSet/>
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>
PREFIX prop: <https://w3id.org/omega-x/ontology/Property/>

SELECT (MIN(?value) AS ?minDCCurrent)
WHERE {
  # Define the specific evaluation point (device)
  BIND(<https://w3id.org/omega-x/ontology/KG/PARKDatasets/EvaluationPoint/PARK_ECP002_S3_SHL002_CA001> AS ?evaluationPoint)

  # Find the EnergyDataSet that includes this evaluation point
  ?energyDataSet eds:includesEvaluationPoint ?evaluationPoint .

  # Find the DataCollections comprised in this EnergyDataSet
  ?energyDataSet ets:comprises ?dataCollection .

  # Filter for the DataCollection that is about DC Current
  ?dataCollection ets:isAboutProperty prop:DCCurrent .

  # Get the DataPoints belonging to this DataCollection
  ?dataPoint ets:belongsTo ?dataCollection .

  # Get the data value link for each DataPoint
  ?dataPoint ets:hasDataValue ?dataValue .

  # Get the actual numerical value
  ?dataValue ets:value ?value .
}
```

**Result:**

![Screenshot 2025-06-19 144902](https://github.com/user-attachments/assets/5790a1bf-4a49-46a1-b443-921289b92e00)


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

![Screenshot 2025-06-19 145004](https://github.com/user-attachments/assets/b1eeae24-98e9-4ad5-b0c6-3168bf7d75e4)


---

## 5. What is the average value of a device?

This query calculates the average value for all data points in a specific data collection. The data collection URI should be replaced with the desired collection.

```sparql
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (AVG(?numericValue) AS ?averageValue)
WHERE {
  # --- REPLACE THIS URI with the DataCollection you want to average ---
  BIND(<https://w3id.org/omega-x/ontology/KG/PARKDatasets/DataCollection/PARK_ECP002_S3_SHL002_CA001/s4MMDCAmpmagf/W1> AS ?dataCollection)

  ?dataPoint ets:belongsTo ?dataCollection ;
             ets:hasDataValue ?dataValue .

  ?dataValue ets:value ?value .

  # Ensure the value is treated as a number (double) for the AVG function
  BIND(xsd:double(?value) AS ?numericValue)
}
```

**Result:**

![Screenshot 2025-06-19 145101](https://github.com/user-attachments/assets/9e4baa81-9212-4ebb-818c-110947435b59)



## Notes

- All queries use the Omega-X ontology prefixes for consistency
- Time-based filters use XSD datetime format
- Property URIs may need adjustment based on your specific ontology implementation
- Screenshots should show the actual query results from your SPARQL endpoint
