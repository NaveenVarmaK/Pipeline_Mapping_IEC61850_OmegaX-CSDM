# Energy Dataset Processing Pipeline

A comprehensive pipeline for creating Knoweldge Graph from CSV files tagged with IEC 61850 standard.


##  Pipeline Overview
The pipeline is depicted in Figure ![image](https://github.com/user-attachments/assets/d717ad2a-ea9c-4ccb-9373-0023633858e7).

It consists of Three main steps:
1. **Extract** - Convert time to UTC, extract the list of devices and split  CSV files by device.
2. **Transform** - Use Jinja template to generate RML mapping files for each device. These mapping files are used in SDM-RDFizer to convert CSV data to RDF knowledge graphs.
3. **Load** - Store the knoweldge graphs in GrapghDB and query it using SPARQL.
## 📋 Prerequisites

### Required Dependencies

```bash
pip install pandas
pip install python-dateutil
pip install tqdm
pip install psutil
pip install jinja2
pip install requests
```

### External Tools

- **SDM-RDFizer**: Download and install from [SDM-RDFizer GitHub](https://github.com/SDM-TIB/SDM-RDFizer)
- **GraphDB**: Install GraphDB for knowledge graph storage and querying

### Directory Structure

Create the following directory structure before running:

```
project/
├── Input_CSV_Datasets/
│   └── Input_CSV_Datasets_by_Devices/
│       └── CSV_PerDevices/
├── Output/
│   └── RML/
├── Resources/
│   └── CSV_Header_Dictionary.py
├── Jinja_RML-Template_PerDevice.j2
├── CSV_Device_Seperator_With_TimeFormat.py
├── RML_Generation.py
└── GraphDBConnector.py
```

##  Step-by-Step Usage Guide

### Step 1: Extract 
**CSV Device Separation**: Processes your raw energy dataset CSV file and splits it by device while standardizing timestamps.

#### Command Line Usage

```bash
python CSV_Device_Seperator_With_TimeFormat.py input_file.csv [options]
```

#### Options

- `--output-dir`: Output directory for device CSV files (default: `Input_CSV_Datasets/Input_CSV_Datasets_by_Devices/CSV_PerDevices`)
- `--time-col`: Name of the time column to standardize (default: `Time`)
- `--device-col`: Name of the column containing device identifiers
- `--file-id`: ID string to append to output filenames (default: `W1`)

#### Examples

```bash
# Basic usage
python CSV_Device_Seperator_With_TimeFormat.py my_energy_data.csv

# With custom output directory and file ID
python CSV_Device_Seperator_With_TimeFormat.py my_energy_data.csv --output-dir ./separated_devices --file-id SITE001

# With specific device column
python CSV_Device_Seperator_With_TimeFormat.py my_energy_data.csv --device-col DeviceID
```

#### What it does:

- ✅ Automatically detects CSV format
- ✅ Extracts device names from headers or device columns
- ✅ Standardizes timestamps to ISO 8601 format (`2024-11-02T06:13:20`)
- ✅ Handles various timestamp formats (Unix, scientific notation, date strings)
- ✅ Splits data into separate CSV files per device
- ✅ Monitors performance (CPU, RAM, disk I/O)
- ✅ Creates detailed logs

#### Output

Creates individual CSV files for each device:
- `METEOSTA001_W1.csv`
- `INVERTER01_W1.csv`
- `WEATHER_STATION_W1.csv`

### Step 2: Transform
**RML Generation**

Generate RML files that define how CSV data maps to RDF triples. 

#### Usage

```python
python RML_Generation.py
```

#### Configuration

Edit the script to specify:

```python
# Input CSV path (output from Step 1)
csv_path = 'Input_CSV_Datasets/Input_CSV_Datasets_by_Devices/CSV_PerDevices/METEOSTA001_W1.csv'

# Output RML file path
output_filename = '../OmegaX-Pipeline/Output/RML/generated_METEOSTA001_W1.rml.ttl'
```

#### What it does:

- ✅ Parses CSV headers and maps them to semantic properties
- ✅ Uses measurement dictionary to identify data types and units
- ✅ Generates RML mapping files using Jinja2 templates
- ✅ Creates QUDT-compliant unit mappings
- ✅ Profiles execution time and memory usage


#### Output

Creates RML files like:
- `generated_METEOSTA001_W1.rml.ttl`
- `generated_INVERTER01_W1.rml.ttl`

### Step 3: RDF Generation with SDM-RDFizer

Use SDM-RDFizer to convert CSV data to RDF using the generated RML mappings.

#### Prerequisites

1. Install SDM-RDFizer following their [installation guide](https://github.com/SDM-TIB/SDM-RDFizer)
2. Create a configuration file for SDM-RDFizer

#### Configuration File Example (`config.ini`)

```ini
[DEFAULT]
main_directory: /path/to/your/project/

[DataSources]
number_of_datasets: 1
output_folder: /path/to/output/
all_in_one_file: yes
remove_duplicate: yes
enrichment: no
name: dataset1
mapping: /path/to/generated_METEOSTA001_W1.rml.ttl
```

#### Command

```bash
python -m rdfizer -c config.ini
```

#### What it does:

- ✅ Reads CSV data and RML mappings
- ✅ Generates RDF triples in Turtle format
- ✅ Creates knowledge graph representations

#### Output

Creates RDF files:
- `knowledge_graph_METEOSTA001_W1.ttl`
- `knowledge_graph_INVERTER01_W1.ttl`

### Step 3: Load

Load and query the generated knowledge graphs using GraphDB.

#### Setup GraphDB

1. Install and start GraphDB
2. Create a new repository (e.g., "EnergyDataKG")
3. Import the generated RDF files

#### Usage

```python
from GraphDBConnector import GraphDBConnector

# Initialize connector
graphdb = GraphDBConnector("http://localhost:7200", "EnergyDataKG")

# Example query
query = """
PREFIX prop: <https://w3id.org/omega-x/ontology/Property/>
PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>

SELECT ?dataPoint ?dataTime ?dataValue ?property ?unit
WHERE {
    ?dataPoint rdf:type ets:DataPoint ;
               ets:dataTime ?dataTime ;
               ets:hasDataValue ?dataValue ;
               prop:isAboutProperty ?property ;
               prop:hasUnit ?unit .
}
LIMIT 100
"""

# Execute and display results
results = graphdb.execute_query(query)
graphdb.print_query_results(results)
```

#### What it does:

- ✅ Connects to GraphDB repositories
- ✅ Executes SPARQL queries
- ✅ Formats and displays results
- ✅ Handles connection errors gracefully

## Resources

### CSV_Header_Dictionary.py

Contains property definitions and unit mappings:

```python
MEASUREMENTS = {
    "temp": {
        "description": "Temperature measurement",
        "qudt_unit": "http://qudt.org/vocab/unit/DEG_C",
    },
    "pow": {
        "description": "Power measurement", 
        "qudt_unit": "http://qudt.org/vocab/unit/W"
    }
    # Add more measurements as needed
}
```

### Jinja2 Template

The RML template defines the mapping structure. Customize it based on your ontology requirements.

## 📊 Performance Monitoring

The pipeline includes comprehensive performance monitoring:

- **Execution time** for each processing step
- **Memory usage** tracking
- **CPU and disk I/O** monitoring
- **Progress bars** for long-running operations
- **Detailed logging** with timestamps

##  Troubleshooting

### Common Issues

1. **CSV Parsing Errors**
   - Check for misaligned columns
   - Verify delimiter (comma vs semicolon)
   - Use `--on-bad-lines=skip` option

2. **Memory Issues with Large Files**
   - Process files in chunks
   - Monitor RAM usage
   - Close unused file handles

3. **RML Generation Failures**
   - Check Jinja2 template syntax
   - Ensure proper file paths

4. **GraphDB Connection Issues**
   - Verify GraphDB is running
   - Check repository name and URL
   - Confirm network connectivity

### Logging

Check log files in the `logs/` directory for detailed error information:
- `csv_splitter_YYYYMMDD_HHMMSS.log`

## 🤝 Contributing

To extend the pipeline:

1. Add new measurement types to `CSV_Header_Dictionary.py`
2. Customize the Jinja2 template for different ontologies
3. Extend device name extraction patterns
4. Add new CSV format support

## License

This project is licensed under the MIT License. See the [LICENSE](./License) file for details.

## Acknoweldgment
[Electricité De France (EDF)](https://www.edf.fr/) team and partners 
[Ecole des mines de Saint-Etienne](https://www.mines-stetienne.fr/)
The European projetc Omega-X [Omega-X website](https://omega-x.eu/)
