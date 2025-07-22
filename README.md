# ETL Processing Pipeline

A Pipeline for creating Knowledge Graphs from CSV files tagged with IEC 61850 standard, featuring automated evaluation and performance monitoring. This pipeline follows the **Omega-X ontology** pattern for energy data modeling and semantic interoperability.

## Omega-X Pattern for Energy data Modeling

The pipeline processes IEC 61850 energy data following the Omega-X ontology pattern, which defines the semantic relationships between energy datasets, data collections, and market participants:

<img width="1321" height="471" alt="Diagram Metodology-pattern-new drawio" src="https://github.com/user-attachments/assets/dd8f6eba-1b93-4da0-ba38-55f643d88d83" />

## IEC 61850 Device Modeling

The pipeline processes IEC 61850 compliant energy devices, mapping their logical structure to semantic representations:

![iectags](https://github.com/user-attachments/assets/cc1b84cf-f901-484b-9def-7874f9dc0943)


**Device Hierarchy Processing:**
- **Physical Device**: Top-level device identifier (e.g., PARK)
- **Logical Device**: Specific device instance (e.g., ECP001_S3_SHL001_Inverter01)
- **Logical Nodes**: Functional components (sddinv1, MMXU1)
- **Data Attributes**: Measurement properties (heatsinktmp, encltmp, TotW, W)

The pipeline automatically extracts and maps these hierarchical relationships to create semantically rich knowledge graphs compatible with the Omega-X energy ontology.

## Pipeline Overview

The enhanced pipeline consists of five main steps with integrated evaluation, all following the Omega-X ontology specifications:

1. **Extract** - Convert time to **ISO 8601**, extract device list, and split CSV files by device using **regex**
2. **Transform** - Generate RML mapping files using **Jinja2** template and creates knowledge graph using **SDM-RDFizer**
3. **Load** - Import to running **GraphDB** repository to store and query the knowledge graph

## Omega-X Ontology Integration

The pipeline is specifically designed to work with the **Omega-X ontology** for energy data interoperability:

### Semantic Mapping Features
- **Automatic IEC 61850 tag parsing** and mapping to Omega-X classes
- **Energy device hierarchy preservation** in RDF structure
- **Standardized property mappings** using QUDT units
- **Market participant role assignments** 
- **Time series data modeling** following ETS (EventsTimeSeries) patterns

### Ontology Compliance
- All generated RDF follows Omega-X namespace conventions
- Device properties are mapped to appropriate ontology classes
- Temporal data is structured according to ETS specifications
- Energy roles and market participant relationships are preserved


## Prerequisites

### Required Dependencies

```bash
pip install pandas
pip install python-dateutil
pip install tqdm
pip install psutil
pip install jinja2
pip install requests
pip install rdflib
```

### External Tools

- **SDM-RDFizer**: Automatically installed by the pipeline, or install manually from [SDM-RDFizer GitHub](https://github.com/SDM-TIB/SDM-RDFizer)
- **GraphDB**: Install GraphDB for knowledge graph storage and querying (optional)

### Directory Structure

The pipeline automatically creates the following structure:

```
pipeline_output_YYYYMMDD_HHMMSS/
├── split_csvs/
├── rml_files/
├── knowledge_graph/
├── config/
├── logs/
└── evaluation/
```

## Quick Start

### Basic Usage

```bash
# Run the complete pipeline with timestamped output
python Pipeline_CSV_RML_KG.py input_data.csv

# Run with evaluation
python Pipeline_CSV_RML_KG.py input_data.csv --evaluate

# Run with GraphDB import
python Pipeline_CSV_RML_KG.py input_data.csv --import-to-graphdb --graphdb-repo my-repo-id
```

## Command Line Usage

### Complete Pipeline Script

```bash
python Pipeline_CSV_RML_KG.py input.csv [options]
```

### Required Arguments

- `input_csv`: Path to the input CSV file to be processed

### Pipeline Output Options

- `--output-dir`: Base output directory (default: `pipeline_output`)
- `--no-timestamp`: Disable timestamped output folders

### CSV Processing Options

- `--time-col`: Name of the time column (default: `Time`)
- `--device-col`: Name of the column with device identifiers
- `--file-id`: ID to append to split CSV filenames

### RML Generation Options

- `--rml-template`: Path to Jinja2 template file (default: `Jinja_RML-Template_PerDevice.j2`)
- `--prefix`: Ontology prefix URL (default: Omega-X namespace)
- `--wid`: Window ID (default: `W1`)
- `--timestamp-column`: Name of timestamp column for RML
- `--source-participant`: Name of the source participant
- `--target-participant`: Name of the target participant

### Knowledge Graph Options

- `--kg-format`: Output format (`turtle`, `n-triples`, `rdf-xml`)
- `--remove-duplicates/--no-remove-duplicates`: Control duplicate removal
- `--all-in-one`: Generate all datasets in one file
- `--no-enrichment`: Disable enrichment
- `--no-ordered`: Disable ordered processing

#### Note: For Now When you try to use arguments --source-participant and --target-participant with --all-in-one you must also use --no-remove-duplicates. If not the generated output KG will not be valid.


### GraphDB Import Options

- `--import-to-graphdb`: Enable GraphDB import
- `--graphdb-url`: GraphDB instance URL (default: `http://localhost:7200`)
- `--graphdb-repo`: Repository ID (required for import)
- `--graphdb-user`: Username for authentication
- `--graphdb-password`: Password for authentication

### Evaluation Options

- `--evaluate`: Run evaluation after pipeline completion

## Examples

### Basic Pipeline Execution

```bash
# Simple run with default settings
python .\Pipeline_CSV_RML_KG.py '.\Input_CSV_Datasets\PARK-2024-09-26_week1.csv' --prefix https://w3id.org/omega-x/ontology/KG/PARK-DataSets --wid W1 --evaluate
```

### Advanced Configuration

```bash
# Full pipeline with custom Omega-X settings
python .\Pipeline_CSV_RML_KG.py '.\Input_CSV_Datasets\PARK-2024-09-26_week1.csv' --prefix https://w3id.org/omega-x/ontology/KG/PARK-DataSets --wid W1 --all-in-one --import-to-graphdb --graphdb-repo PARK-Inverter-W1-2025 --graphdb-user admin --graphdb-password pass12345 --evaluate
```


## Evaluation Features

The integrated evaluation system provides comprehensive analysis of Omega-X compliant knowledge graphs:

### Performance Metrics
- **Total pipeline execution time**
- **Per-stage timing breakdown**
- **Throughput (triples per second)**
- **Resource usage monitoring** (CPU, memory)

### Knowledge Graph Analysis
- **Accurate triple counting** using rdflib
- **Omega-X ontology compliance validation**
- **File size analysis**
- **Format distribution**
- **Quality assessment**

### Output Reports
- **JSON evaluation reports** with detailed metrics
- **Console summary** with key statistics
- **Timestamped logs** for debugging

## Output Structure

Each pipeline run creates a timestamped directory containing Omega-X compliant knowledge graphs:

```
pipeline_output_20250614_163000/
├── split_csvs/                    # Device-separated CSV files
│   ├── METEOSTA001_W1.csv
│   └── INVERTER01_W1.csv
├── rml_files/                     # Generated RML mappings (Omega-X compliant)
│   ├── generated_METEOSTA001_W1.rml.ttl
│   └── generated_INVERTER01_W1.rml.ttl
├── knowledge_graph/               # Generated RDF files (Omega-X format)
│   ├── knowledge_graph_METEOSTA001_W1.ttl
│   └── knowledge_graph_INVERTER01_W1.ttl
├── config/                        # SDM-RDFizer configuration
│   └── rdfizer_config.ini
├── logs/                          # Detailed execution logs
│   └── pipeline_20250614_163000.log
└── evaluation/                    # Performance reports
    └── evaluation_report_20250614_163000.json
```


## License

This project is licensed under the MIT License.

## Acknowledgments

- [Electricité De France (EDF)](https://www.edf.fr/) team and partners
- [École des mines de Saint-Étienne](https://www.mines-stetienne.fr/)
- The European project [Omega-X](https://omega-x.eu/) for ontology specifications and energy data interoperability standards

<img width="851" height="76" alt="image" src="https://github.com/user-attachments/assets/07c6d393-d94b-46cc-a2fc-94fef8cad03b" />

