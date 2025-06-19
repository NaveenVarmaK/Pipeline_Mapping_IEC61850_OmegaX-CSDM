# Energy Dataset Processing Pipeline

A comprehensive pipeline for creating Knowledge Graphs from CSV files tagged with IEC 61850 standard, featuring automated evaluation and performance monitoring.

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
python Pipelilne_CSV_RML_KG.py input_data.csv

# Run with comprehensive evaluation
python Pipeline_CSV_RML_KG.py input_data.csv --evaluate

# Run with GraphDB import
python Pipeline_CSV_RML_KG.py input_data.csv --import-to-graphdb --graphdb-repo my-repo-id
```

## Pipeline Overview

The enhanced pipeline consists of five main steps with integrated evaluation:

1. **Extract** - Convert time to UTC, extract device list, and split CSV files by device
2. **Transform** - Generate RML mapping files using Jinja templates
3. **Validate** - Verify RML file paths and fix issues automatically
4. **Load** - Convert CSV data to RDF knowledge graphs using SDM-RDFizer
5. **Import** - Optionally import to GraphDB repository
6. **Evaluate** - Comprehensive performance and quality assessment

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
- `--prefix`: Ontology prefix URL
- `--wid`: Window ID (default: `W1`)
- `--timestamp-column`: Name of timestamp column for RML

### Knowledge Graph Options

- `--kg-format`: Output format (`turtle`, `n-triples`, `rdf-xml`)
- `--remove-duplicates/--no-remove-duplicates`: Control duplicate removal
- `--all-in-one`: Generate all datasets in one file
- `--no-enrichment`: Disable enrichment
- `--no-ordered`: Disable ordered processing

### GraphDB Import Options

- `--import-to-graphdb`: Enable GraphDB import
- `--graphdb-url`: GraphDB instance URL (default: `http://localhost:7200`)
- `--graphdb-repo`: Repository ID (required for import)
- `--graphdb-user`: Username for authentication
- `--graphdb-password`: Password for authentication

### Evaluation Options

- `--evaluate`: Run comprehensive evaluation after pipeline completion

### General Options

- `--log-level`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `--verbose`: Enable verbose output

## Examples

### Basic Pipeline Execution

```bash
# Simple run with default settings
python Pipeline_CSV_RML_KG.py energy_data.csv

# Custom output directory with evaluation
python Pipeline_CSV_RML_KG.py energy_data.csv --output-dir ./results --evaluate
```

### Advanced Configuration

```bash
# Full pipeline with custom settings
python Pipeline_CSV_RML_KG.py energy_data.csv \
  --evaluate \
  --prefix "https://example.org/ontology" \
  --remove-duplicates
```

### GraphDB Integration

```bash
# Pipeline with GraphDB import
python Pipeline_CSV_RML_KG.py energy_data.csv \
  --evaluate \
  --import-to-graphdb \
  --graphdb-repo energy-kg \
  --graphdb-url http://localhost:7200 \
  --graphdb-user admin \
  --graphdb-password password
```

## Evaluation Features

The integrated evaluation system provides comprehensive analysis:

### Performance Metrics
- **Total pipeline execution time**
- **Per-stage timing breakdown**
- **Throughput (triples per second)**
- **Resource usage monitoring** (CPU, memory)

### Knowledge Graph Analysis
- **Accurate triple counting** using rdflib
- **File size analysis**
- **Format distribution**
- **Quality assessment**

### Output Reports
- **JSON evaluation reports** with detailed metrics
- **Console summary** with key statistics
- **Timestamped logs** for debugging

## Output Structure

Each pipeline run creates a timestamped directory containing:

```
pipeline_output_20250614_163000/
├── split_csvs/                    # Device-separated CSV files
│   ├── METEOSTA001_W1.csv
│   └── INVERTER01_W1.csv
├── rml_files/                     # Generated RML mappings
│   ├── generated_METEOSTA001_W1.rml.ttl
│   └── generated_INVERTER01_W1.rml.ttl
├── knowledge_graph/               # Generated RDF files
│   ├── knowledge_graph_METEOSTA001_W1.ttl
│   └── knowledge_graph_INVERTER01_W1.ttl
├── config/                        # SDM-RDFizer configuration
│   └── rdfizer_config.ini
├── logs/                          # Detailed execution logs
│   └── pipeline_20250614_163000.log
└── evaluation/                    # Performance reports
    ├── evaluation_20250614_163000.log
    └── evaluation_report_20250614_163000.json
```

## Individual Components

### CSV Device Separator

```bash
python CSV_Device_Seperator_With_TimeFormat.py input.csv [options]
```

**Features:**
- Automatic CSV format detection
- Multiple timestamp format support
- Device extraction from headers or columns
- Performance monitoring
- Detailed logging

### RML Generator

```bash
python RML_Generation.py csv_path [options]
```

**Features:**
- Flexible command-line configuration
- Jinja2 template system
- QUDT-compliant unit mappings
- Semantic property mapping
- Execution profiling

### Pipeline Evaluator

```bash
python Pipeline_CSV_RML_KG.py --evaluate
```

**Features:**
- Accurate triple counting with rdflib
- Performance timing analysis
- Resource usage monitoring
- Comprehensive reporting

## Configuration Files

### RDFizer Configuration

The pipeline automatically generates `rdfizer_config.ini`:

```ini
[default]
main_directory = /path/to/pipeline/output

[datasets]
number_of_datasets = 1
output_folder = /path/to/knowledge_graph
remove_duplicate = yes
all_in_one_file = no
enrichment = yes
ordered = yes
output_format = turtle

[dataset1]
name = METEOSTA001_W1
mapping = /path/to/generated_METEOSTA001_W1.rml.ttl
```

### Measurement Dictionary

Customize `Resources/CSV_Header_Dictionary.py`:

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
}
```

## Performance Monitoring

The enhanced pipeline includes comprehensive monitoring:

- **Real-time resource tracking** (CPU, RAM, disk I/O)
- **Per-stage execution timing**
- **Progress indicators** for long operations
- **Memory usage optimization**
- **Detailed performance reports**


## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **SDM-RDFizer Installation**
   ```bash
   python3 -m pip install rdfizer
   ```

3. **Memory Issues with Large Files**
   - Use `--no-all-in-one` for separate files
   - Monitor with `--evaluate` flag
   - Process in smaller batches

4. **GraphDB Connection Issues**
   - Verify GraphDB is running: `http://localhost:7200`
   - Check repository exists
   - Validate credentials

5. **RML Path Issues**
   - Pipeline automatically fixes relative paths
   - Check logs for validation results
   - Ensure CSV files are accessible

### Logging and Debugging

- **Verbose output**: Use `--verbose` flag
- **Debug logging**: Use `--log-level DEBUG`
- **Check logs**: Review files in `logs/` directory
- **Evaluation reports**: Examine `evaluation/` directory

## Contributing

To extend the pipeline:

1. **Add measurement types** to `CSV_Header_Dictionary.py`
2. **Customize RML templates** for different ontologies
3. **Extend device extraction** patterns
4. **Add new output formats**
5. **Enhance evaluation metrics**

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Electricité De France (EDF)](https://www.edf.fr/) team and partners
- [École des mines de Saint-Étienne](https://www.mines-stetienne.fr/)
- The European project [Omega-X](https://omega-x.eu/)
