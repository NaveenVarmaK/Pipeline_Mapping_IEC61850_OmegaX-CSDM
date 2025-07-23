# Word Document Data Object Extractor

A sophisticated Python script designed to automatically extract and process data objects from Word documents containing structured tables. This tool uses AI-powered language models to convert raw table data into structured JSON format, which is essential resource for the ETL-Pipeline.

## Key Features

- **Automatic Table Detection**: Intelligently identifies "Data Object" tables in Word documents
- **AI-Powered Processing**: Uses LLM (Large Language Model) to convert data into structured JSON
- **De-duplication**: Prevents processing the same Data Object multiple times
- **Performance Monitoring**: Tracks CPU usage, memory consumption, and processing times
- **Few-Shot Learning**: Employs contextual examples for improved accuracy
- **Comprehensive Reporting**: Detailed performance and processing statistics


## Performance Results

Based on processing a comprehensive EDF OmegaX library document:

- **Tables Processed**: ~40 data object tables (excluding logical node and data attribute tables)
- **Unique Data Objects**: 247 successfully processed
- **Duplicates Skipped**: 353 duplicate data objects automatically filtered
- **Total Processing Time**: 2,229.59 seconds (~37 minutes)
- **Average LLM Response Time**: 9.02 seconds per prompt
- **Model Used**: Google Gemma 3-4B-IT via LM Studio (131K context length)


## Prerequisites

### Software Requirements

1. **Python Dependencies**:

```bash
pip install python-docx openai psutil lxml
```

2. **LM Studio Setup**:
    - Install and run [LM Studio](https://lmstudio.ai/)
    - Load the Google Gemma 3-4B-IT model
    - Configure server to run on `http://localhost:1234`
    - Set context length to 131,000 tokens
3. **Required Files**:
    - A Word document containing data object tables
    - An editable `CSV_Header_Dictionary.py` file (auto-created if missing)

## File Structure

```
LLM_Dictionary/
├── LLM_DO_Extractor.py              # Main script
├── CSV_Header_Dictionary.py   # Output dictionary file (this is result,Actually it is designed to automatically updates the CSV_Header_Dictionary.py in the ETL-Pipeline Folder)
├── [Word Document].docx       # Input document
└── README.md                      # This file
```


## Usage

### Basic Usage

```bash
python word_extractor.py
```


### Advanced Options

```bash
python word_extractor.py --word-file "path/to/document.docx" \
                         --llm-url "http://localhost:1234/v1" \
                         --csv-dict "output/dictionary.py" \
                         --dry-run
```


### Command Line Arguments

| Argument | Short | Description | Default |
| :-- | :-- | :-- | :-- |
| `--word-file` | `-w` | Path to Word document | Pre-configured path |
| `--llm-url` | `-l` | LLM server URL | `http://localhost:1234/v1` |
| `--csv-dict` | `-c` | Output dictionary file | `Resources/CSV_Header_Dictionary.py` |
| `--dry-run` | `-d` | Preview mode (no file changes) | False |

## How It Works

### 1. Table Detection

The script scans Word documents for tables containing data object information by:

- Analyzing preceding text for keywords like "data object", "dataobject"
- Examining table headers for expected columns: "Data Object (DO)", "Type", "Description", "M/O in standard"


### 2. Data Extraction

- Extracts structured data from identified tables
- Maintains original formatting and relationships


### 3. AI Processing

- Sends each data object to the LLM with comprehensive context
- Uses few-shot learning with detailed examples
- Converts descriptions to structured JSON with proper units and classifications


### 4. De-duplication

- Tracks processed Data Object names
- Automatically skips duplicate entries
- Provides detailed statistics on duplicates found


### 5. Output Generation

- Updates or creates a Python dictionary file
- Maintains existing data while adding new entries
- Provides comprehensive performance reporting


## 📄 Sample Input/Output

### Input (Word Table Row)

```
Data Object (DO): SnwFll
Type: MV-STD_MV
Description: Snowfall (typically in mm length SIUnit [m]).
M/O in standard: O
```


### Output (JSON Structure)

```json
{
    "snwfll": {
        "description": "Snowfall (typically in mm - length SIUnit [m])",
        "unit": "MilliM",
        "enum_kind": "MV_STD",
        "property": "Snowfall"
    }
}
```


## Context Preservation Strategy

The script maintains LLM accuracy by:

- Sending the complete prompt with examples for every data object
- Preventing context drift during long processing sessions
- Using consistent few-shot examples for reliable output format


## Performance Monitoring

The script provides comprehensive monitoring including:

- **Timing Statistics**: Total processing time, extraction time, LLM response times
- **Resource Usage**: CPU utilization, memory consumption
- **Processing Statistics**: Success/failure rates, duplicate detection counts
- **Detailed Reporting**: Per-operation performance metrics


## Configuration

Default configurations can be modified in the script:

```python
DEFAULT_WORD_FILE = "path/to/your/document.docx"
DEFAULT_LLM_URL = "http://localhost:1234/v1"
DEFAULT_CSV_DICT_FILE = "Resources/CSV_Header_Dictionary.py"
```
## Conclusion
This tool automates the extraction and structuring of data objects from Word documents, significantly reducing manual effort and improving accuracy in ontology engineering tasks. By leveraging AI-powered language models, it transforms raw data into a structured format ready for integration into ETL-Pipeline or other semantic applications.